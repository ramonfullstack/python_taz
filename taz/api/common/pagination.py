import json
import math


class Pagination:

    def __init__(self, collection):
        self.collection = collection

    def paginate(
        self,
        criteria,
        page_number,
        offset,
        sort_by=None,
        fields=None
    ):
        total_documents = self._get_count_documents(criteria)
        total_pages = 0
        response = None
        page_number = int(page_number)
        offset = int(offset)
        fields = fields or {}
        fields.update({'_id': 0})

        if total_documents > 0 and offset > 0:
            skip = (page_number - 1) * offset if page_number > 0 else 0
            response = self.collection.objects(
                __raw__=criteria
            ).order_by(sort_by).skip(skip).limit(offset).fields(**fields)

            total_pages = self._get_total_pages(total_documents, offset)

        isvalid_response = response is not None
        records = json.loads(response.to_json()) if isvalid_response else []

        return {
            'records': records,
            'offset': offset,
            'page_number': page_number,
            'total_documents': total_documents,
            'total_pages': total_pages
        }

    def _get_count_documents(self, criteria):
        if not criteria:
            return self.collection.objects.count()

        return self.collection.objects(__raw__=criteria).count()

    def _get_total_pages(self, count, offset):
        if not any([count, offset]):
            return 0

        return math.ceil(count / offset) if offset != 0 else 1
