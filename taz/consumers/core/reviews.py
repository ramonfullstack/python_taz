from functools import cached_property

from taz.consumers.core.database.mongodb import MongodbMixin


class Reviews(MongodbMixin):

    @cached_property
    def customer_behaviors(self):
        return self.get_collection('customer_behaviors')

    def get_customer_behavior(
        self,
        navigation_id: str,
        behavior_type: str
    ):

        data = self.customer_behaviors.find_one(
            {
                'product_id': navigation_id,
                'type': behavior_type
            },
            {
                '_id': 0,
                'value': 1
            }
        )

        if 'review' in behavior_type:
            return (data.get('value') or 0) if data else 0
        elif 'rating' in behavior_type:
            return float(data.get('value') or 0) if data else float(0)
