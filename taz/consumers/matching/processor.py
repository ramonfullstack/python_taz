from functools import cached_property
from typing import Dict

from maaslogger import base_logger

from taz.consumers.core.database.mongodb import MongodbMixin
from taz.consumers.core.exceptions import UndefinedStrategyException

logger = base_logger.get_logger(__name__)


class MatchingProcessor(MongodbMixin):

    def __init__(self, *args, **kwargs):
        self.persist_changes = kwargs.get('persist_changes', True)
        self.exclusive_strategy = kwargs.get('exclusive_strategy', True)
        self.strategy = kwargs.get('strategy')

    @cached_property
    def raw_products(self):
        return self.get_collection('raw_products')

    @cached_property
    def unified_objects(self):
        return self.get_collection('unified_objects')

    @cached_property
    def customer_behaviors(self):
        return self.get_collection('customer_behaviors')

    @property
    def assembler(self):
        if not self.strategy:
            raise UndefinedStrategyException()

        return self.strategy.assembler.ProductAssembler(
            persist_changes=self.persist_changes,
            strategy_name=self.strategy.__name__
        )

    @property
    def matcher(self):
        if not self.strategy:
            raise UndefinedStrategyException()

        return self.strategy.matcher.ProductMatcher(
            persist_changes=self.persist_changes,
            exclusive_strategy=self.exclusive_strategy
        )

    def process_message(self, message: Dict):
        """
        This method process a variation by
        finding similar items from other sellers and then
        gathering similar variations, that could compose a
        single product. Better explanation can be found
        on matching internals (ProductMatcher) and its tests.
        """
        variation = self.raw_products.find_one(
            {
                'sku': message['sku'],
                'seller_id': message['seller_id']
            }
        )

        if not variation:
            logger.warning(
                'Requested variation sku:{} seller:{}" '
                'not found for matching. Postponing matching.'.format(
                    message['sku'],
                    message['seller_id'],
                ),
                detail={
                    "sku": message['sku'],
                    "seller_id": message['seller_id'],
                }
            )
            return False, False

        logger.debug(
            'Found raw variation sku:{} seller_id:{}'.format(
                message['sku'],
                message['seller_id'],
            ),
            detail={
                "sku": message['sku'],
                "seller_id": message['seller_id'],
            }
        )

        discarded = None

        if variation['disable_on_matching']:
            product = self._process_delete(message)

            if not product:
                logger.debug(
                    'Removing product sku:{} seller:{} from matching queue, '
                    'because it does not exist in raw_product'.format(
                        message['sku'],
                        message['seller_id']
                    ),
                    detail={
                        "sku": message['sku'],
                        "seller_id": message['seller_id'],
                    }
                )
                return True, discarded

            logger.debug(
                'Successfully deleted matching of sku:{} seller_id:{} '
                'persist_changes:{}'.format(
                    message['sku'], message['seller_id'], self.persist_changes
                ),
                detail={
                    "sku": message['sku'],
                    "seller_id": message['seller_id'],
                }
            )
        else:
            product, discarded = self._process_creation(variation)

            if not product:
                logger.warning(
                    'Removing product sku:{} seller:{} from matching queue, '
                    'because couldn\'t finish the assemble'.format(
                        message['sku'],
                        message['seller_id']
                    ),
                    detail={
                        "sku": message['sku'],
                        "seller_id": message['seller_id'],
                    }
                )
                return True, discarded

            logger.debug(
                'Successfully created matching of sku:{} seller_id:{} '
                'persist_changes:{}'.format(
                    message['sku'], message['seller_id'], self.persist_changes
                ),
                detail={
                    "sku": message['sku'],
                    "seller_id": message['seller_id'],
                }
            )

        if len(product.get('variations') or []) == 0:
            logger.warning(
                'Product {product_id} is without any variations sku:{sku} '
                'seller_id:{seller_id}'.format(
                    product_id=product['id'],
                    sku=message['sku'],
                    seller_id=message['seller_id']
                ),
                detail={
                    "product_id": product['id'],
                    "sku": message['sku'],
                    "seller_id": message['seller_id'],
                }
            )

        return product, discarded

    def _process_delete(self, message: Dict) -> Dict:
        unified_product = self.assembler.disassemble(message)
        return unified_product

    def _process_creation(self, unified_variation: Dict):
        matched_variations = self.matcher.match_variations(unified_variation)
        assembled_product, discarded = self.assembler.assemble(
            matched_variations
        )

        return assembled_product, discarded
