from maaslogger import base_logger

from taz.consumers.core.database.mongodb import MongodbMixin

logger = base_logger.get_logger(__name__)


class ProductScoresCollection(MongodbMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.product_scores = self.get_collection('product_scores')

    def save(self, data):
        criteria = {
            'sku': data['sku'],
            'seller_id': data['seller_id'],
            'type': data['type']
        }

        logger.debug(
            'Request created Product Score data with payload:{}'.format(
                data
            )
        )

        self.product_scores.remove(criteria)
        self.product_scores.update(criteria, {'$set': data}, upsert=True)

        logger.info(
            'Successfully created Product Score to sku:{}'.format(
                data['sku']
            )
        )

    def delete(self, data):
        criteria = {
            'sku': data['sku'],
            'seller_id': data['seller_id'],
            'type': data['type']
        }

        logger.debug(
            'Request deleted Product Score with payload:{}'.format(data)
        )

        self.product_scores.remove(criteria)

        logger.info(
            'Successfully deleted Product Score to sku:{}'.format(
                data['sku']
            )
        )
