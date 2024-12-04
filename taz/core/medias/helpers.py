import re

from taz.constants import NON_DOWNLOADABLE_MEDIA_TYPES


class MediaHelper:

    @staticmethod
    def get_media_extension(media_type: str, url: str) -> str:
        if (
            media_type in NON_DOWNLOADABLE_MEDIA_TYPES or
            not url
        ):
            return ''

        re_query = re.compile(r'\?.*$', re.IGNORECASE)
        re_port = re.compile(r':[0-9]+', re.IGNORECASE)
        re_ext = re.compile(r'(\.[A-Za-z\d]+$)', re.IGNORECASE)

        url = re_query.sub('', url)
        url = re_port.sub('', url)

        matches = re_ext.search(url)
        if matches:
            return matches.group(1)

        return '.jpg'

    @staticmethod
    def video_url_validation(url: str) -> any:
        regex = re.findall(
            '(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/ ]{11})',  # noqa
            url
        )
        return any(regex)
