import datetime
import os
from ftplib import FTP
from unittest.mock import Mock, mock_open, patch

import pytest
from redis import Redis
from simple_settings import settings
from simple_settings.utils import settings_stub

from taz.crontabs.metabooks_ftp.cron import MetabooksFtpCrontab


class TestMetabooksFtpCrontab:

    LOCAL_FOLDER_NAME = 'files'
    BASE_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)))

    @pytest.fixture
    def crontab(self):
        return MetabooksFtpCrontab()

    @pytest.fixture
    def patch_download_file(self):
        return patch.object(MetabooksFtpCrontab, '_download_file')

    @pytest.fixture
    def patch_get_ftp_files(self):
        return patch.object(MetabooksFtpCrontab, '_get_ftp_files')

    @pytest.fixture
    def patch_find_file(self):
        return patch.object(MetabooksFtpCrontab, '_find_file')

    @pytest.fixture
    def patch_unzip_file(self):
        return patch.object(MetabooksFtpCrontab, '_unzip_file')

    @pytest.fixture
    def patch_get_files(self):
        return patch.object(MetabooksFtpCrontab, '_get_files')

    @pytest.fixture
    def patch_get_isbns(self):
        return patch.object(MetabooksFtpCrontab, '_get_isbns')

    @pytest.fixture
    def local_folder(self):
        return f'{self.BASE_PATH}/{self.LOCAL_FOLDER_NAME}'

    @pytest.fixture
    def patch_redis_get(self):
        return patch.object(Redis, 'get')

    @pytest.fixture
    def isbns(self):
        return ['6555860197']

    @pytest.fixture
    def current_datetime(self):
        return datetime.datetime(2021, 5, 19, 5, 0, 0)

    @pytest.fixture
    def hour_processed(self, current_datetime):
        return current_datetime - datetime.timedelta(hours=1)

    @pytest.fixture
    def ftp_files(self):
        date_time = datetime.datetime(2018, 1, 1, 0, 0, 0)
        current_datetime = datetime.datetime(2021, 5, 20, 10, 0, 0)
        files = []
        randminute = 0
        while date_time <= current_datetime:
            minute = date_time.minute + randminute % 60
            files.append(
                'MetabooksOnix30_{year}{month}{day}{hour}{minute}.zip'.format(
                    year=date_time.year,
                    month='{:02d}'.format(date_time.month),
                    day='{:02d}'.format(date_time.day),
                    hour='{:02d}'.format(date_time.hour),
                    minute='{:02d}'.format(minute)
                )
            )
            date_time += datetime.timedelta(hours=1)
            randminute += 1

        return files

    @pytest.fixture
    def local_files(self):
        return [
            'MetabooksOnix30_202105190440.zip',
            'MetabooksOnix30_202105190541.zip'
        ]

    @pytest.mark.parametrize(
        'current_datetime,hours_retroactive',
        [
            (datetime.datetime(2021, 5, 19, 0, 0, 0), 24),
            (datetime.datetime(2021, 5, 19, 0, 0, 0), 720)
        ]
    )
    def test_run_crontab_metabooksftp_setup_success(
        self,
        current_datetime,
        hours_retroactive
    ):
        with patch.object(
            datetime, 'datetime', Mock(wraps=datetime.datetime)
        ) as mock_datetime:
            with settings_stub(
                METABOOKS_FTP_CRON_HOURS_RETROACTIVE=hours_retroactive
            ):
                mock_datetime.utcnow.return_value = current_datetime

                crontab = MetabooksFtpCrontab()

                hour_processed = crontab.cache.get(crontab.cache_key)
                hour_processed = str(hour_processed, 'utf-8')
                hour_processed = datetime.datetime.strptime(
                    hour_processed,
                    crontab.datetime_format
                )

                current_datetime -= datetime.timedelta(hours=hours_retroactive)
                assert hour_processed == current_datetime

    def test_run_crontab_metabooksftp_with_file_success(
        self,
        crontab,
        patch_get_ftp_files,
        patch_download_file,
        patch_publish_manager,
        local_folder,
        patch_redis_get,
        local_files,
        current_datetime,
        hour_processed
    ):
        crontab.BASE_PATH = self.BASE_PATH
        crontab.local_folder = local_folder

        with patch.object(
            datetime, 'datetime', Mock(wraps=datetime.datetime)
        ) as mock_datetime:
            with patch_get_ftp_files as mock_ftp_files:
                with patch_download_file as mock_ftp:
                    with patch_publish_manager as mock_pubsub:
                        with patch_redis_get as mock_redis:
                            mock_ftp_files.return_value = local_files
                            mock_datetime.utcnow.return_value = current_datetime  # noqa
                            mock_redis.return_value = hour_processed.strftime(
                                crontab.datetime_format
                            ).encode('utf-8')
                            crontab.run()

        assert mock_ftp.called
        mock_pubsub.assert_called_with(
            topic_name=settings.PUBSUB_METADATA_INPUT_TOPIC_NAME,
            project_id=settings.GOOGLE_PROJECT_ID,
            content={'identified': '9788538092162', 'source': 'metabooks'}
        )

    def test_run_crontab_metabooksftp_with_multiple_files_sucess(
        self,
        crontab,
        patch_get_ftp_files,
        patch_download_file,
        patch_publish_manager,
        local_folder,
        patch_redis_get,
        local_files,
        current_datetime
    ):
        crontab.BASE_PATH = self.BASE_PATH
        crontab.local_folder = local_folder

        hour_processed = current_datetime - datetime.timedelta(hours=2)

        with patch.object(
            datetime, 'datetime', Mock(wraps=datetime.datetime)
        ) as mock_datetime:
            with patch_get_ftp_files as mock_ftp_files:
                with patch_download_file as mock_ftp:
                    with patch_publish_manager as mock_pubsub:
                        with patch_redis_get as mock_redis:
                            mock_ftp_files.return_value = local_files
                            mock_datetime.utcnow.return_value = current_datetime  # noqa
                            mock_redis.return_value = hour_processed.strftime(
                                crontab.datetime_format
                            ).encode('utf-8')
                            crontab.run()

        assert mock_ftp.call_count == 2
        assert mock_pubsub.called

    def test_run_crontab_metabooksftp_with_file_failed(
        self,
        crontab,
        patch_get_ftp_files,
        patch_download_file,
        patch_publish_manager,
        local_folder,
        patch_redis_get,
        local_files
    ):
        crontab.BASE_PATH = self.BASE_PATH
        crontab.local_folder = local_folder

        current_datetime = datetime.datetime(2021, 5, 19, 6, 0, 0)
        hour_processed = current_datetime - datetime.timedelta(hours=1)

        with patch.object(
            datetime, 'datetime', Mock(wraps=datetime.datetime)
        ) as mock_datetime:
            with patch_get_ftp_files as mock_ftp_files:
                with patch_download_file as mock_ftp:
                    with patch_publish_manager as mock_pubsub:
                        with patch_redis_get as mock_redis:
                            mock_ftp_files.return_value = local_files
                            mock_datetime.utcnow.return_value = current_datetime  # noqa
                            mock_redis.return_value = hour_processed.strftime(
                                crontab.datetime_format
                            ).encode('utf-8')
                            crontab.run()

        assert not mock_ftp.called
        assert not mock_pubsub.called

    @pytest.mark.parametrize('current_datetime', [
        (datetime.datetime(2021, 5, 19, 0, 0, 0)),
        (datetime.datetime(2021, 5, 20, 10, 10, 0))
    ])
    def test_run_crontab_metabooksftp_sucess(
        self,
        crontab,
        patch_get_ftp_files,
        patch_download_file,
        patch_unzip_file,
        patch_get_files,
        patch_get_isbns,
        patch_publish_manager,
        local_folder,
        patch_redis_get,
        current_datetime,
        ftp_files,
        isbns,
        logger_stream
    ):
        crontab.BASE_PATH = self.BASE_PATH
        crontab.local_folder = local_folder

        hour_processed = current_datetime - datetime.timedelta(hours=1)

        with patch.object(
            datetime, 'datetime', Mock(wraps=datetime.datetime)
        ) as mock_datetime:
            with patch_get_ftp_files as mock_get_ftp_files:
                with patch_download_file, patch_unzip_file, patch_get_files, patch_get_isbns as mock_get_isbns:  # noqa
                    with patch_publish_manager as mock_pubsub:
                        with patch_redis_get as mock_redis:
                            mock_get_ftp_files.return_value = ftp_files
                            mock_get_isbns.return_value = isbns
                            mock_datetime.utcnow.return_value = current_datetime  # noqa
                            mock_redis.return_value = hour_processed.strftime(
                                crontab.datetime_format
                            ).encode('utf-8')
                            crontab.run()

        filename = crontab.filename.format(
            year=current_datetime.year,
            month='{:02d}'.format(current_datetime.month),
            day='{:02d}'.format(current_datetime.day),
            hour='{:02d}'.format(current_datetime.hour),
            minute=''
        ).replace('.zip', '')

        assert mock_pubsub.called
        assert (
            f'Starting processing cron:MetabooksFtpCrontab file:{filename}'
            in logger_stream.getvalue()
        )

    def test_run_crontab_metabooksftp_failed(
        self,
        crontab,
        patch_get_ftp_files,
        patch_download_file,
        patch_unzip_file,
        patch_get_files,
        patch_get_isbns,
        patch_publish_manager,
        local_folder,
        patch_redis_get,
        ftp_files,
        logger_stream
    ):
        crontab.BASE_PATH = self.BASE_PATH
        crontab.local_folder = local_folder

        current_datetime = datetime.datetime(2021, 5, 19, 13, 0, 0)
        hour_processed = current_datetime - datetime.timedelta(hours=1)

        with patch.object(
            datetime, 'datetime', Mock(wraps=datetime.datetime)
        ) as mock_datetime:
            with patch_get_ftp_files as mock_get_ftp_files:
                with patch_download_file, patch_unzip_file, patch_get_files, patch_get_isbns:  # noqa
                    with patch_publish_manager as mock_pubsub:
                        with patch_redis_get as mock_redis:
                            mock_get_ftp_files.return_value = ftp_files
                            mock_datetime.utcnow.return_value = current_datetime  # noqa
                            mock_redis.return_value = hour_processed.strftime(
                                crontab.datetime_format
                            ).encode('utf-8')
                            crontab.run()

        filename = crontab.filename.format(
            year=hour_processed.year,
            month='{:02d}'.format(hour_processed.month),
            day='{:02d}'.format(hour_processed.day),
            hour='{:02d}'.format(hour_processed.hour),
            minute=''
        ).replace('.zip', '')

        assert not mock_pubsub.called
        assert (
            f'Starting processing cron:MetabooksFtpCrontab file:{filename}'
            not in logger_stream.getvalue()
        )

        assert 'Finish, sent to queue 0 ISBN' in logger_stream.getvalue()

    @pytest.mark.parametrize('current_datetime,hour_processed', [
        (
            datetime.datetime(2021, 5, 19, 0, 0, 0),
            datetime.datetime(2021, 5, 18, 22, 0, 0)
        ),
        (
            datetime.datetime(2021, 5, 20, 10, 10, 0),
            datetime.datetime(2021, 5, 20, 8, 0, 0)
        )
    ])
    def test_run_crontab_metabooksftp_retroactive_sucess(
        self,
        crontab,
        patch_get_ftp_files,
        patch_download_file,
        patch_unzip_file,
        patch_get_files,
        patch_get_isbns,
        patch_publish_manager,
        local_folder,
        patch_redis_get,
        current_datetime,
        hour_processed,
        ftp_files,
        logger_stream
    ):
        crontab.BASE_PATH = self.BASE_PATH
        crontab.local_folder = local_folder

        with patch.object(
            datetime, 'datetime', Mock(wraps=datetime.datetime)
        ) as mock_datetime:
            with patch_get_ftp_files as mock_get_ftp_files:
                with patch_download_file, patch_unzip_file, patch_get_files, patch_get_isbns:  # noqa
                    with patch_publish_manager:
                        with patch_redis_get as mock_redis:
                            mock_get_ftp_files.return_value = ftp_files
                            mock_datetime.utcnow.return_value = current_datetime  # noqa
                            mock_redis.return_value = hour_processed.strftime(
                                crontab.datetime_format
                            ).encode('utf-8')
                            crontab.run()

        hour_processed += datetime.timedelta(hours=1)
        while hour_processed <= current_datetime:
            filename = crontab.filename.format(
                year=hour_processed.year,
                month='{:02d}'.format(hour_processed.month),
                day='{:02d}'.format(hour_processed.day),
                hour='{:02d}'.format(hour_processed.hour),
                minute=''
            ).replace('.zip', '')

            assert 'Starting processing cron:MetabooksFtpCrontab file:{filename}'.format(  # noqa
                filename=filename
            ) in logger_stream.getvalue()
            hour_processed += datetime.timedelta(hours=1)

    def test_run_crontab_metabooksftp_not_hour_processed_failed(
        self,
        crontab,
        patch_get_ftp_files,
        patch_download_file,
        patch_unzip_file,
        patch_get_files,
        patch_get_isbns,
        patch_publish_manager,
        local_folder,
        patch_redis_get,
        logger_stream
    ):
        crontab.BASE_PATH = self.BASE_PATH
        crontab.local_folder = local_folder

        with patch.object(
            datetime, 'datetime', Mock(wraps=datetime.datetime)
        ) as mock_datetime:
            with patch_get_ftp_files:
                with patch_download_file, patch_unzip_file, patch_get_files, patch_get_isbns:  # noqa
                    with patch_publish_manager:
                        with patch_redis_get as mock_redis:
                            mock_redis.return_value = None
                            mock_datetime.utcnow.return_value = datetime.datetime(2021, 5, 19, 5, 0, 0)  # noqa
                            result = crontab.run()

        assert 'Last processing hour not found cron:{}'.format(
            crontab.cron_name
        ) in logger_stream.getvalue()
        assert result is not None

    def test_run_crontab_metabooksftp_get_ftp_files_failed_with_alert(
        self,
        crontab,
        patch_find_file,
        local_folder,
        patch_redis_get,
        current_datetime,
        hour_processed,
        logger_stream
    ):
        crontab.BASE_PATH = self.BASE_PATH
        crontab.local_folder = local_folder

        with patch.object(
            datetime, 'datetime', Mock(wraps=datetime.datetime)
        ) as mock_datetime:
            with patch_find_file as mock_find_file:
                with patch_redis_get as mock_redis:
                    with patch.object(FTP, 'login') as mock_ftp:
                        mock_datetime.utcnow.return_value = current_datetime
                        mock_redis.return_value = hour_processed.strftime(
                            crontab.datetime_format
                        ).encode('utf-8')
                        mock_ftp.side_effect = Exception('Connection error')
                        result = crontab.run()

        assert not mock_find_file.called
        assert result is not None
        assert 'There was an error listing the files with error:Connection error' in logger_stream.getvalue()  # noqa

    def test_run_crontab_metabooksftp_download_file_failed_without_alert(
        self,
        crontab,
        patch_get_ftp_files,
        patch_unzip_file,
        local_folder,
        patch_redis_get,
        local_files,
        current_datetime,
        hour_processed,
        logger_stream
    ):
        crontab.BASE_PATH = self.BASE_PATH
        crontab.local_folder = local_folder

        with patch.object(
            datetime, 'datetime', Mock(wraps=datetime.datetime)
        ) as mock_datetime:
            with patch_get_ftp_files as mock_ftp_files:
                with patch.object(FTP, 'login'), patch.object(FTP, 'cwd'):
                    with patch(
                        'builtins.open', mock_open()
                    ) as mock_ftp_download:
                        with patch_unzip_file as mock_unzip_file:
                            with patch_redis_get as mock_redis:
                                mock_datetime.utcnow.return_value = current_datetime  # noqa
                                mock_redis.return_value = hour_processed.strftime( # noqa
                                    crontab.datetime_format
                                ).encode('utf-8')
                                mock_ftp_files.return_value = local_files

                                mock_ftp_download.side_effect = Exception(
                                    'No such file or directory'
                                )
                                result = crontab.run()

        assert result is None
        assert not mock_unzip_file.called
        assert (
            'Starting download file in FTP from Metabooks'
            in logger_stream.getvalue()
        )
        assert (
            'There was an error downloading the file with error:'
            'No such file or directory' in logger_stream.getvalue()
        )
