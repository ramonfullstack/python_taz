import pytest
from simple_settings.utils import settings_stub

from taz.core.matching.common.algorithms import (
    distance,
    exceptions,
    word_processing
)


def sentence_for_ngram_a():
    return (
        'fogao 4 bocas ative! bf150ar inox grill timer acendimento'
    )


def sentence_for_ngram_b():
    return 'fogao 4 bocas ative! timer grill'


def sentence_ngrams_a():
    return [
        'fogao 4 bocas ative! bf150ar inox grill',
        'fogao 4 bocas ative! bf150ar inox grill',
        'fogao 4 bocas ative! bf150ar inox grill timer',
        'fogao 4 bocas ative! bf150ar inox grill timer acendimento',
        (
            'fogao 4 bocas ative! bf150ar '
            'inox grill timer acendimento automatico'
        ),
        'fogao 4 bocas ative! bf150ar inox grill',
        'fogao 4 bocas ative! bf150ar inox grill acendimento',
        'fogao 4 bocas ative! bf150ar inox grill acendimento automatico',
        'fogao 4 bocas ative! bf150ar inox grill acendimento automatico',
        'fogao 4 bocas ative! bf150ar inox grill',
        'fogao 4 bocas ative! bf150ar inox grill automatico',
        'fogao 4 bocas ative! bf150ar inox grill automatico',
        'fogao 4 bocas ative! bf150ar inox grill automatico'
    ]


def sentence_ngrams_b():
    return [
        'fogao 4 bocas ative! timer grill'
    ]


class TestCosineSimilarity:

    @pytest.fixture
    def cosine(self):
        return distance.CosineSimilarity()

    @pytest.mark.parametrize('sentence_a,sentence_b,expected', [
        (
            'Motorola moto x 2 generation',
            'Motorola moto x 2 generation hdtv',
            True
        ),
        (
            'Motorola moto g 3 generation hdtv',
            'Motorola moto x 2 generation hdtv',
            False
        ),
        (
            'mamao',
            'laranja',
            False
        )
    ])
    def test_similarity(
        self, cosine,
        sentence_a, sentence_b,
        expected
    ):
        assert cosine.are_similar(
            sentence_a,
            sentence_b
        ) is expected

    def test_empty_values_raises_comparison_error(self, cosine):
        with pytest.raises(exceptions.InvalidComparisonError):
            cosine.are_similar(
                None,
                None,
            )

    @pytest.mark.parametrize(
        'sentence_a, sentence_b, ngrams_a, ngrams_b, expected',
        [
            (
                sentence_for_ngram_a(),
                sentence_for_ngram_b(),
                sentence_ngrams_a(),
                sentence_ngrams_b(),
                True
            ),
            (
                sentence_for_ngram_b(),
                sentence_for_ngram_a(),
                sentence_ngrams_b(),
                sentence_ngrams_a(),
                True
            )
        ]
    )
    @settings_stub(ACCEPTABLE_NGRAM_COSINE_THRESHOLD=0.85)
    def test_similarity_using_ngram_algorithm(
        self,
        cosine,
        sentence_a,
        sentence_b,
        ngrams_a,
        ngrams_b,
        expected
    ):

        similarity_threshold = cosine._similarity(
            cosine._group_words(sentence_a),
            cosine._group_words(sentence_b)
        )

        assert cosine.THRESHOLD > similarity_threshold >= 0.7

        are_similar = cosine.are_similar(
            sentence_reference=sentence_a,
            sentence_possibility=sentence_b,
            sentence_references=ngrams_a,
            sentence_possibilities=ngrams_b,
            ngram_threshold=0.85
        )

        assert are_similar

    def test_ngram_without_sentence(
            self,
            cosine
    ):
        are_similar = cosine.are_similar(
            sentence_reference='Product title',
            sentence_possibility='Possible product title',
            sentence_references=None,
            sentence_possibilities=None
        )

        assert not are_similar

    def test_ngram_with_only_reference(
            self,
            cosine
    ):
        are_similar = cosine.are_similar(
            eligible_for_applying_ngram_threshold=0.3,
            sentence_reference='Product title',
            sentence_possibility='Possible product title',
            sentence_references=['first_reference', 'second_reference'],
            sentence_possibilities=None
        )

        assert not are_similar


class TestSyntacticAnalysis:

    @pytest.fixture
    def analyzer(self):
        return word_processing.SyntacticAnalyzer()

    def test_remove_ambiguous_words(self, analyzer):
        assert 'a b c' == analyzer.remove_ambiguous_words('a b c d', ['d'])

    @pytest.mark.parametrize('input_text, expected_text', [
        ('assim xablau', 'xablau'),
        ('desde que tenha um xablau', 'tenha um xablau'),
        ('desde maneira que', 'desde maneira'),
    ])
    def test_remove_conjunctions(self, analyzer, input_text, expected_text):
        assert expected_text == analyzer.remove_conjunctions(input_text)

    @pytest.mark.parametrize('input_text, expected_text', [
        ('a opa ei', 'opa ei'),
        ('de vez em quando', 'vez quando'),
        ('por enquanto', 'enquanto'),
    ])
    def test_remove_prepositions(self, analyzer, input_text, expected_text):
        assert expected_text == analyzer.remove_prepositions(input_text)

    @pytest.mark.parametrize('input_text, expected_text', [
        ('fi duma egua', 'fi egua'),
        ('um cabrito', 'cabrito'),
    ])
    def test_remove_articles(self, analyzer, input_text, expected_text):
        assert expected_text == analyzer.remove_articles(input_text)
