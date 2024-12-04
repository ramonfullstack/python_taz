import math

from simple_settings import settings

from .exceptions import InvalidComparisonError


class CosineSimilarity:

    THRESHOLD = settings.COSINE_THRESHOLD
    NGRAM_THRESHOLD = settings.NGRAM_COSINE_THRESHOLD
    ACCEPTABLE_NGRAM_THRESHOLD = settings.ACCEPTABLE_NGRAM_COSINE_THRESHOLD

    def _similarity(self, a, b):
        """
        Computes the cosine based on a intersection o values
        A and B
        """
        intersection = set.intersection(
            set(a.keys()),
            set(b.keys())
        )

        scalar = 0
        norm1 = 0
        norm2 = 0

        for i in intersection:
            scalar += a.get(i) * b.get(i)

        for v in a.values():
            norm1 += math.pow(v, 2)

        for v in b.values():
            norm2 += math.pow(v, 2)

        return scalar / math.sqrt(norm1 * norm2)

    def are_similar(
        self, sentence_reference, sentence_possibility,
        sentence_references=None,
        sentence_possibilities=None,
        threshold=THRESHOLD,
        eligible_for_applying_ngram_threshold=NGRAM_THRESHOLD,
        ngram_threshold=settings.ACCEPTABLE_NGRAM_COSINE_THRESHOLD
    ):
        """
        Computes the similarity between two given sentences
        based on COSINE_THRESHOLD set on settings file
        """
        if not sentence_reference and not sentence_possibility:
            raise InvalidComparisonError(
                'Both values must be valid'
            )

        score = self._similarity(
            self._group_words(sentence_reference),
            self._group_words(sentence_possibility),
        )

        if score >= threshold:
            return True

        if score >= eligible_for_applying_ngram_threshold:
            if sentence_references:
                ngram_score_for_sentence_references = max([
                    self._similarity(
                        self._group_words(sentence),
                        self._group_words(sentence_possibility),
                    ) for sentence in sentence_references
                ])

                if ngram_score_for_sentence_references >= ngram_threshold:
                    return True

            if sentence_possibilities:
                ngram_score_fore_possible_references = max([
                    self._similarity(
                        self._group_words(sentence),
                        self._group_words(sentence_reference),
                    ) for sentence in sentence_possibilities
                ])

                return ngram_score_fore_possible_references >= ngram_threshold

        return False

    def _group_words(self, sentence):
        """
        This method group words and counts how many times
        a word is used on a given sentence
        """
        if not sentence:
            return 0

        word_groups = {}

        for word in sentence.split():
            occurrence_counter = word_groups.get(word, 0)
            word_groups[word] = occurrence_counter + 1.0

        return word_groups
