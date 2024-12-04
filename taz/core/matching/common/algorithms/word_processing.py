import re

from taz import constants
from taz.utils import diacriticless


class SyntacticAnalyzer:

    def __init__(self):
        self.diacriticless_keywords = {
            'conjunctions': [
                diacriticless(w)
                for w in constants.CONJUNCTIONS
            ],
            'prepositions': [
                diacriticless(w)
                for w in constants.PREPOSITIONS
            ],
            'articles': [
                diacriticless(w)
                for w in constants.ARTICLES
            ]
        }

    def remove_ambiguous_words(
        self, sentence, words,
        custom_beginning='\\s?', custom_ending='\\s?'
    ):
        parametrized_expression = r'{beginning}({{}}){ending}'.format(
            beginning=custom_beginning,
            ending=custom_ending,
        )
        match_expression = parametrized_expression.format(
            '|'.join(
                [
                    diacriticless(re.escape(w))
                    for w in words
                ]
            )
        )

        clear_sentence = re.sub(match_expression, ' ', diacriticless(sentence))

        return re.sub(r'[-|_|\\|\\\|\/]', '', clear_sentence).strip()

    def remove_conjunctions(self, sentence):
        return self._remove_keywords_by_context(sentence, 'conjunctions')

    def remove_prepositions(self, sentence):
        return self._remove_keywords_by_context(sentence, 'prepositions')

    def remove_articles(self, sentence):
        return self._remove_keywords_by_context(sentence, 'articles')

    def _remove_keywords_by_context(self, sentence, context):
        return self.remove_ambiguous_words(
            sentence,
            self.diacriticless_keywords[context],
            custom_beginning='(^|\\.|\\!|\\?|\\s)',
            custom_ending='(\\.|\\!|\\?|\\s|$)'
        )
