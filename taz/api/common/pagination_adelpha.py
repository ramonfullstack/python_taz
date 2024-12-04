class Pagination:

    def __init__(self, collection, path):
        self.collection = collection
        self.path = path

    def paginate(self, criteria, fields, offset, limit):
        if fields:
            fields.update({'_id': 0})
        else:
            fields = {'_id': 0}
        cursor = self.collection.find(
            criteria,
            fields
        ).limit(limit).skip(offset)

        results = list(cursor)
        count = len(results)

        page = {
            **criteria,
            '_count': count,
            '_offset': offset,
            '_limit': limit
        }

        return {
            'meta': {
                'page': {
                    'limit': limit,
                    'offset': offset,
                    'count': count
                },
                'links': {
                    'previous_page': self.__build_previous(page),
                    'next_page': self.__build_next(page)
                }
            },
            'results': results
        }

    def __build_next(self, pagination):
        if pagination['_count'] < pagination['_limit']:
            return ''

        next_page = pagination.copy()
        next_page['_offset'] += next_page['_count']
        next_page.pop('_count', None)
        return self.__build_query_str(next_page)

    def __build_previous(self, pagination):
        if pagination['_offset'] == 0:
            return ''

        offset = max(0, pagination['_offset'] - pagination['_limit'])
        previous_page = pagination.copy()
        previous_page.update(_offset=offset)
        previous_page.pop('_count', None)
        return self.__build_query_str(previous_page)

    def __build_query_str(self, query_params):
        query_str = '?'
        for key, value in query_params.items():
            if value is not None:
                query_str = '{query_str}{key}={value}&'.format(
                    query_str=query_str,
                    key=key,
                    value=value
                )

        return self.path + query_str[:-1] if self.path else query_str[:-1]
