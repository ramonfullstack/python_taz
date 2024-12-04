from typing import Dict, List


class ConsumerException(Exception):
    pass


class InvalidAcmeResponseException(ConsumerException):
    pass


class RequiredFieldException(ConsumerException):

    def __init__(
        self,
        missing_fields: List,
        consumer_scope: str,
        action: str,
        data: Dict
    ):
        self.message = (
            f'Required fields {missing_fields} of scope {consumer_scope} '
            f'is missing for action {action}'
        )

        sku = data.get('sku')
        seller_id = data.get('seller_id')

        if sku and seller_id:
            self.message = (
                f'{self.message} and sku {sku} seller_id {seller_id}'
            )


class RequiredNonEmptyFieldException(ConsumerException):

    def __init__(
        self,
        empty_required_fields: List,
        consumer_scope: str,
        action: str,
        data: Dict
    ):
        self.message = (
            f'Required non empty fields {empty_required_fields} '
            f'of scope {consumer_scope} is empty for action {action}'
        )

        sku = data.get('sku')
        seller_id = data.get('seller_id')

        if sku and seller_id:
            self.message = (
                f'{self.message} and sku {sku} seller_id {seller_id}'
            )


class NotFound(Exception):
    pass


class UndefinedStrategyException(ConsumerException):
    pass


class MaxRetriesException(ConsumerException):
    pass


class NavigationIdNotFound(ConsumerException):
    pass


class BadRequest(Exception):
    pass


class SolrIndexingException(Exception):
    pass


class SolrConverterException(Exception):
    pass


class SolrReaderException(Exception):
    pass


class InvalidScope(ConsumerException):

    def __init__(self, scope_name):
        self.message = f'Unknown scope name:{scope_name}'

    def __str__(self):
        return self.message
