import logging
from typing import Dict, List

from slugify import slugify

from taz.constants import SPECIFICATIONS_TYPE_BY_LABEL as SPECIFICATIONS

logger = logging.getLogger(__name__)


def normalize_attributes(original_attributes: dict) -> List[Dict]:
    attributes = []
    for metadata, value in original_attributes.items():
        if not value:
            continue
        try:
            _type = SPECIFICATIONS.get(metadata) or slugify(metadata)
            attributes.append({'type': _type, 'value': value})
        except Exception:
            logger.warning(f'Attribute not found, metadata:{metadata}')
    logger.debug(f'Attributes {attributes} normalized')
    return attributes
