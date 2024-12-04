from taz.consumers.core.exceptions import ConsumerException


class MediaWithoutContentType(ConsumerException):

    def __init__(self, media):
        self.media = media

    def __str__(self):
        return (
            'Cannot determine content-type of media sku:{m.sku} '
            'seller_id:{m.seller} type:{m.media_type} '
            'url:{m.url}'.format(m=self.media)
        )


class MediaException(ConsumerException):
    def __init__(self, media):
        self.media = media
        self.message = (
            'Could not process the media sku:{m.sku} seller_id:{m.seller} '
            'type:{m.media_type} url:{m.url}'.format(m=self.media)
        )
