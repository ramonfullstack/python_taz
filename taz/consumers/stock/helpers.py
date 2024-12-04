import logging

from taz import constants

logger = logging.getLogger(__name__)


def get_type(value):
    if value in constants.STOCK_TYPES:
        return constants.STOCK_TYPES[value]

    logger.error('Invalid value for "{}"'.format(value))
    raise ValueError('Invalid value')


def get_availability(branch_id):
    if int(branch_id) in constants.NATIONAL_DISTRIBUTION_CENTERS:
        return constants.AVAILABILITY_NATIONWIDE

    return constants.AVAILABILITY_REGIONAL
