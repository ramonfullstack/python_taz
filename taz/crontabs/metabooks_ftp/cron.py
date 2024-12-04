import datetime
import logging
import os
import re
import zipfile
from concurrent.futures import ThreadPoolExecutor, wait
from ftplib import FTP
from functools import cached_property
from typing import List
from xml.dom import minidom

from redis import Redis
from simple_settings import settings

from taz.constants import SOURCE_METABOOKS
from taz.consumers.core.google.stream import StreamPublisherManager
from taz.crontabs.base import CronBase

logger = logging.getLogger(__name__)


class MetabooksFtpCrontab(CronBase):

    cron_name = 'MetabooksFtpCrontab'

    LOCAL_FOLDER_NAME = 'files'
    BASE_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)))
    MAX_WORKERS = 5

    def __init__(self, *args, **kwargs):
        self.date_format = '{year}{month}{day}{hour}{minute}'
        self.filename = f'MetabooksOnix30_{self.date_format}.zip'
        self.ftp_remote_path = '/public/onix30/hourlyexport'
        self.local_folder = f'{self.BASE_PATH}/{self.LOCAL_FOLDER_NAME}'

        self.cache = Redis(
            host=settings.REDIS_LOCK_SETTINGS['host'],
            port=settings.REDIS_LOCK_SETTINGS['port'],
            password=settings.REDIS_LOCK_SETTINGS.get('password')
        )

        self.cache_key = 'metabooksftpcron-hourly'
        self.datetime_format = '%Y/%m/%d %H:%M:%S'

        if not self.cache.get(self.cache_key):
            hours_retroactive = int(
                settings.METABOOKS_FTP_CRON_HOURS_RETROACTIVE
            )
            current_datetime = datetime.datetime.utcnow()
            current_datetime -= datetime.timedelta(hours=hours_retroactive)

            self.cache.set(
                self.cache_key,
                current_datetime.strftime(self.datetime_format)
            )

    @cached_property
    def pubsub(self):
        return StreamPublisherManager()

    def run(self):
        hour_processed = self.cache.get(self.cache_key)

        if not hour_processed:
            logger.error(
                'Last processing hour not found '
                f'cron:{self.cron_name}'
            )
            return False

        hour_processed = str(hour_processed, 'utf-8')
        hour_processed = datetime.datetime.strptime(
            hour_processed,
            self.datetime_format
        )
        hour_processed += datetime.timedelta(hours=1)
        isbn_count = 0

        ftp_files = self._get_ftp_files()
        if not ftp_files:
            return False

        files = self._find_file(ftp_files, hour_processed)

        for filename in files:
            logger.info(
                f'Starting processing cron:{self.cron_name} '
                f'file:{filename}'
            )

            local_file = f'{self.BASE_PATH}/{self.LOCAL_FOLDER_NAME}/{filename}' # noqa
            try:
                self._download_file(
                    filename,
                    local_file
                )
            except Exception as e:
                logger.error(
                    'There was an error downloading '
                    f'the file with error:{e}'
                )
                return

            files = self._unzip_file(local_file, self.local_folder)
            files = self._get_files(files)
            isbns = self._get_isbns(files)
            isbn_count += len(isbns)

            with ThreadPoolExecutor(
                max_workers=self.MAX_WORKERS
            ) as executor:
                futures = [
                    executor.submit(self._notify, isbn)
                    for isbn in isbns
                ]

            wait(futures)

            hour_processed = filename.replace('MetabooksOnix30_', '')
            hour_processed = hour_processed.replace('.zip', '')
            hour_processed = datetime.datetime.strptime(
                hour_processed,
                '%Y%m%d%H%M'
            )
            hour_processed = hour_processed.strftime(self.datetime_format)
            self.cache.set(self.cache_key, hour_processed)

        logger.info(f'Finish, sent to queue {isbn_count} ISBN')

    def _get_ftp_files(self):
        with FTP(host=settings.METABOOKS_HOST) as ftp:
            try:
                ftp.login(
                    settings.METABOOKS_USER,
                    settings.METABOOKS_PASSWORD
                )

                ftp.cwd(self.ftp_remote_path)
                return ftp.nlst()
            except Exception as e:
                logger.error(
                    'There was an error listing the '
                    f'files with error:{e}'
                )
                return False

    def _find_file(self, files: List, hour_processed: datetime) -> List:
        regex_pattern = ''
        current_datetime = datetime.datetime.utcnow()

        while hour_processed <= current_datetime:
            regex_pattern += self.date_format.format(
                year=hour_processed.year,
                month='{:02d}'.format(hour_processed.month),
                day='{:02d}'.format(hour_processed.day),
                hour='{:02d}'.format(hour_processed.hour),
                minute='.*'
            )
            regex_pattern += '|'
            hour_processed += datetime.timedelta(hours=1)

        regex_pattern = regex_pattern.strip('|')
        regex_pattern = '{file_prefix}({regex_pattern}).zip'.format(
            file_prefix='MetabooksOnix30_',
            regex_pattern=regex_pattern
        )

        return [file for file in files if re.search(regex_pattern, file)]

    def _download_file(self, filename: str, local_file: str) -> None:
        logger.info('Starting download file in FTP from Metabooks')

        with FTP(host=settings.METABOOKS_HOST) as ftp:
            ftp.login(
                settings.METABOOKS_USER,
                settings.METABOOKS_PASSWORD
            )

            ftp.cwd(self.ftp_remote_path)

            if not os.path.exists(self.local_folder):
                os.makedirs(self.local_folder)

            ftp.retrbinary(f'RETR {filename}', open(local_file, 'wb').write)

        logger.info(f'File {local_file} saved successfully')

    @staticmethod
    def _unzip_file(local_file: str, local_folder: str) -> List:
        try:
            with zipfile.ZipFile(local_file, 'r') as zip_ref:
                zip_ref.extractall(local_folder)

                return zip_ref.namelist()
        except FileNotFoundError as e:
            logger.error(
                'There was an error downloading '
                f'the file with error:{e}'
            )
            return []

    def _get_files(self, files_enzip: List) -> List:
        file_types = ['New', 'Upd']
        files = [
            f for f in files_enzip
            if any(_type in f for _type in file_types)
        ]

        files = [f'{self.local_folder}/{f}' for f in files]
        return files

    @staticmethod
    def _get_isbns(files: List) -> List:
        isbns = []
        for filename in files:
            logger.info(f'Processing the file {filename}')

            document = minidom.parse(filename)
            products = document.getElementsByTagName('product')

            for product in products:
                product_identifiers = product.getElementsByTagName(
                    'productidentifier'
                )

                for product_identifier in product_identifiers:
                    if product_identifier.childNodes[1].firstChild.data != '03':  # noqa
                        continue

                    isbn = product_identifier.childNodes[3].firstChild.data
                    isbns.append(isbn)

        return isbns

    def _notify(self, value):
        message = {
            'identified': value,
            'source': SOURCE_METABOOKS
        }

        self.pubsub.publish(
            topic_name=settings.PUBSUB_METADATA_INPUT_TOPIC_NAME,
            project_id=settings.GOOGLE_PROJECT_ID,
            content=message
        )

        logger.info(
            f'ISBN {value} sent to topic:'
            f'{settings.PUBSUB_METADATA_INPUT_TOPIC_NAME}'
        )


if __name__ == '__main__':  # pragma: no cover
    crontab = MetabooksFtpCrontab()
    crontab.start()
