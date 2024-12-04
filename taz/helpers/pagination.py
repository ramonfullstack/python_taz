from typing import Dict, Optional


class Pagination:

    def __init__(self, collection):
        self.collection = collection

    def _paginate_keyset(
        self,
        criteria: Dict,
        limit_size: int,
        sort: Optional[Dict],
        fields: Dict,
        field_offset: Optional[str] = None,
        offset: Optional[int] = None,
        no_cursor_timeout: bool = True
    ):
        if field_offset and offset:
            criteria.update({field_offset: {'$gt': offset}})

        return self.collection.find(
            criteria,
            fields,
            no_cursor_timeout=no_cursor_timeout is not False
        ).sort(sort).limit(limit_size)
