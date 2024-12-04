from io import BytesIO

from taz.core.medias.media import (
    MediaDownloadInput,
    MediaDownloadOutput,
    MediaType
)


class TestMediaDownloadInput:

    def test_when_create_media_download_input_then_return_instance(
        self,
        mock_bucket_img_internal_url: str
    ):
        media_input = MediaDownloadInput(
            url=mock_bucket_img_internal_url,
            media_type=MediaType.images.value
        )

        assert media_input.url == mock_bucket_img_internal_url
        assert media_input.media_type == 'images'
        assert media_input.extension == '.jpg'


class TestMediaDownloadOutput:

    def test_when_create_none_data_media_download_output_then_return_instance(
        self,
        mock_bucket_img_internal_url: str
    ):
        media_output = MediaDownloadOutput(
            url=mock_bucket_img_internal_url,
            media_type=MediaType.images.value,
            data=None,
            content_type=None
        )

        assert media_output.url == mock_bucket_img_internal_url
        assert media_output.media_type == 'images'
        assert media_output.extension == '.jpg'
        assert media_output.data is None
        assert media_output.content_type is None
        assert media_output.md5 is None
        assert media_output.width is None
        assert media_output.height is None
        assert media_output.is_empty()
        assert media_output.mount_file_name() == ''

    def test_when_create_empty_data_media_download_output_then_return_instance(
        self,
        mock_bucket_img_internal_url: str
    ):
        md5: str = 'd41d8cd98f00b204e9800998ecf8427e'
        media_output = MediaDownloadOutput(
            url=mock_bucket_img_internal_url,
            media_type=MediaType.images.value,
            data=BytesIO(b''),
            content_type=None
        )

        assert media_output.url == mock_bucket_img_internal_url
        assert media_output.media_type == 'images'
        assert media_output.extension == '.jpg'
        assert media_output.data.getbuffer() == b''
        assert media_output.content_type is None
        assert media_output.md5 == md5
        assert media_output.width is None
        assert media_output.height is None
        assert media_output.is_empty()
        assert not media_output.is_image_png()
        assert media_output.mount_file_name() == f'{md5}.jpg'

    def test_when_create_text_media_download_output_then_return_instance(
        self,
        mock_bucket_img_internal_url: str
    ):
        data: bytes = b'data'
        media_output = MediaDownloadOutput(
            url=mock_bucket_img_internal_url,
            media_type=MediaType.videos.value,
            data=BytesIO(data),
            content_type='plain/text'
        )

        assert media_output.url == mock_bucket_img_internal_url
        assert media_output.media_type == 'videos'
        assert media_output.extension == ''
        assert media_output.data.getbuffer() == data
        assert media_output.content_type == 'plain/text'
        assert media_output.md5 == '8d777f385d3dfec8815d20f7496026dc'
        assert media_output.width is None
        assert media_output.height is None
        assert not media_output.is_empty()
        assert not media_output.is_image_png()
        assert media_output.mount_file_name() == ''

    def test_when_create_image_media_download_output_then_return_instance(
        self,
        mock_image_data: bytes,
        mock_content_type_png: str,
        mock_image_md5: str
    ):
        url: str = 'https://img/test.png'
        media_output = MediaDownloadOutput(
            url=url,
            media_type=MediaType.images.value,
            data=BytesIO(mock_image_data),
            content_type=mock_content_type_png,
            width=1,
            height=1
        )

        assert media_output.url == url
        assert media_output.media_type == 'images'
        assert media_output.extension == '.png'
        assert media_output.data.getbuffer() == mock_image_data
        assert media_output.content_type == mock_content_type_png
        assert media_output.md5 == mock_image_md5
        assert media_output.width == 1
        assert media_output.height == 1
        assert not media_output.is_empty()
        assert media_output.is_image_png()
        assert media_output.mount_file_name() == f'{mock_image_md5}.png'

    def test_when_change_image_data_then_calculate_new_md5(
        self,
        mock_image_data: bytes,
        mock_content_type_png: str,
        mock_image_md5: str
    ):
        url: str = 'https://img/test.png'
        media_output = MediaDownloadOutput(
            url=url,
            media_type=MediaType.images.value,
            data=BytesIO(mock_image_data),
            content_type=mock_content_type_png,
            width=1,
            height=1
        )

        old_file_name: str = media_output.mount_file_name()

        assert media_output.md5 == mock_image_md5
        assert media_output.width == 1
        assert media_output.height == 1

        new_data: bytes = b'new image'
        md5 = '29d2893f5a129397809927e3ef0c85d6'
        media_output.change_image_data(
            data=BytesIO(new_data),
            width=2,
            height=2
        )

        assert media_output.url == url
        assert media_output.media_type == 'images'
        assert media_output.extension == '.png'
        assert media_output.data.getbuffer() == new_data
        assert media_output.content_type == mock_content_type_png
        assert media_output.md5 == md5
        assert media_output.width == 2
        assert media_output.height == 2
        assert not media_output.is_empty()
        assert media_output.is_image_png()
        assert media_output.mount_file_name() == f'{md5}.png'
        assert media_output.mount_file_name() != old_file_name
