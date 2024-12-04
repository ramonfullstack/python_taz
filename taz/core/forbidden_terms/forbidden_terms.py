from functools import cached_property
from typing import Dict, List, Tuple

from redis.client import Redis
from simple_settings import settings

from taz.constants import REDIS_KEY_FORBIDDEN_TERMS
from taz.consumers.core.database.mongodb import MongodbMixin
from taz.helpers.json import json_dumps, json_loads
from taz.utils import diacriticless

PUNCTUATION_MARKS = ['.', ',', ';', ':', '?', '!', '...']


class ForbiddenTerms(MongodbMixin):

    def __init__(self):
        self.__redis = Redis(
            host=settings.REDIS_LOCK_SETTINGS['host'],
            port=settings.REDIS_LOCK_SETTINGS['port'],
            password=settings.REDIS_LOCK_SETTINGS.get('password')
        )
        self.__key = REDIS_KEY_FORBIDDEN_TERMS

    @cached_property
    def forbidden_terms(self):
        return self.get_collection('forbidden_terms')

    def save_redis_terms(self, payload: Dict):
        cache_key = self.__redis.get(self.__key)
        cache_key = json_loads(cache_key) if cache_key else {}

        cache_key.update(payload)

        normalized_payload = {
            diacriticless(key): value
            for (key, value) in cache_key.items()
        }

        self.__redis.set(self.__key, json_dumps(normalized_payload))

    def get_redis_terms(self):
        cache_key = self.__redis.get(self.__key)

        if not cache_key:
            return settings.FORBIDDEN_TERMS

        return json_loads(cache_key)

    def delete_redis_terms(
        self,
        terms: Dict
    ) -> Tuple[bool, List]:
        cache_key = self.__redis.get(self.__key)

        if not cache_key:
            return False, []

        cache_key = json_loads(cache_key)
        normalized_terms = {
            diacriticless(key): value
            for (key, value) in terms.items()
        }

        keys_not_found = []
        for term in normalized_terms.keys():
            try:
                del cache_key[term]
            except Exception:
                keys_not_found.append(term)

        self.__redis.set(self.__key, json_dumps(cache_key))
        return True, keys_not_found

    def save_forbidden_terms(
        self,
        sku: str,
        seller_id: str,
        navigation_id: str,
        new_terms: List
    ) -> None:
        if not new_terms:
            return

        payload = {
            'sku': sku,
            'seller_id': seller_id,
            'navigation_id': navigation_id,
            'forbidden_terms': new_terms
        }

        record = self.forbidden_terms.find_one(
            {'sku': sku, 'seller_id': seller_id},
            {'_id': 0, 'forbidden_terms': 1}
        )

        if record:
            indexes_to_delete = []
            for index, new_term in enumerate(payload['forbidden_terms']):
                for term_database in record['forbidden_terms']:
                    if self.__terms_are_equal(new_term, term_database):
                        indexes_to_delete.append(index)
                        break

            if len(indexes_to_delete) == len(payload['forbidden_terms']):
                return

            indexes_to_delete.sort(reverse=True)
            for index in indexes_to_delete:
                del payload['forbidden_terms'][index]

            payload['forbidden_terms'] += record['forbidden_terms']

        self.forbidden_terms.update_one(
            {'sku': sku, 'seller_id': seller_id},
            {'$set': payload},
            upsert=True
        )

    @staticmethod
    def __terms_are_equal(
        new_term: Dict,
        term_database: Dict
    ) -> bool:
        return (
            new_term['term'] == term_database['term'] and
            new_term['field'] == term_database['field']
        )

    @staticmethod
    def replace_term(
        text: str,
        pattern: str,
        replacement: str
    ) -> Tuple[str, bool]:
        normalize_text = diacriticless(text)
        index = normalize_text.find(pattern)
        should_save = False

        while index != -1:
            should_save = True
            head = text[:index]
            tail = text[index + len(pattern):]
            index = index + len(pattern)

            while index < len(text) and text[index] != ' ':
                if text[index] not in PUNCTUATION_MARKS:
                    tail = tail[1:]
                index += 1

            text = head + replacement + tail
            index = diacriticless(text).find(
                pattern,
                (index + len(replacement)) - len(pattern)
            )

        return text, should_save
