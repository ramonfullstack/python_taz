import logging

from redis import Redis
from simple_settings import settings
from slugify import slugify

from taz.constants import MAGAZINE_LUIZA_SELLER_ID
from taz.consumers.core.aws.sqs import SQSManager

logger = logging.getLogger(__name__)


class ImageQueuer:

    def __init__(self):
        self.ftp_images_queue = SQSManager(
            settings.FTP_IMAGE_QUEUE_NAME,
            settings.FTP_IMAGE_REGION_NAME
        )

        self.cache = Redis(
            host=settings.REDIS_LOCK_SETTINGS['host'],
            port=settings.REDIS_LOCK_SETTINGS['port'],
            password=settings.REDIS_LOCK_SETTINGS.get('password')
        )
        self.cache_expire = 120
        self.cache_key = 'image_{navigation_id}'

    def process_images(self, product, medias):
        if (
            settings.DISABLE_FTP_IMAGE or
            product['seller_id'] == MAGAZINE_LUIZA_SELLER_ID
        ):
            return

        message = None
        try:
            message = self._build_messages(product, medias)
            if message:
                self.ftp_images_queue.put(message)

                logger.info(
                    'Sending images from product:{} message:{} to FTP'.format(
                        message['acme_id'], message
                    )
                )
        except Exception:
            logger.exception('Error send images to FTP')
            raise

        return message

    def _build_messages(self, product, medias):
        if self.cache.get(self.cache_key.format(
            navigation_id=product['navigation_id']
        )):
            logger.info(
                'Sending image variation:{navigation_id} ignored '
                'because it exists in the cache'.format(
                    navigation_id=product['navigation_id']
                )
            )

            return

        images = medias.get('images') or []
        if not images:
            logger.warning(
                'No images found for product:{} to save on FTP'.format(
                    product['navigation_id']
                )
            )

            return

        message = {
            'action': 'create',
            'acme_id': str(product['navigation_id']),
            'images': self._build_urls(product, images)
        }

        self.cache.set(
            self.cache_key.format(navigation_id=product['navigation_id']),
            True,
            self.cache_expire
        )

        return message

    def _build_urls(self, product, images):
        built_images = []
        for image in images:

            path = '/{w}x{h}/{title}/{seller_id}/{sku}/{image}.jpg'.format(
                h=1500,
                w=1500,
                title=slugify('{title} - {reference}'.format(
                    title=product['title'],
                    reference=product.get('reference')
                )),
                seller_id=product['seller_id'],
                sku=slugify(product['sku']),
                image=image.md5
            )

            url = '{}{}'.format(
                settings.ACME_MEDIA_DOMAIN,
                path.format(h=1500, w=1500)
            )

            built_images.append(url.lower())

        return built_images
