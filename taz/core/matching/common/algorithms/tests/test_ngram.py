import pytest

from taz.core.matching.common.algorithms import ngram


class TestSyntacticAnalysis:

    @pytest.fixture
    def analyzer(self):
        return ngram.ReferenceAnalyzer()

    @pytest.mark.parametrize('reference, expected_ngrams', [
        ('4 bocas inox 220V',
         ['', '4', '4 bocas', '4 bocas inox', 'bocas', 'bocas inox',
          'bocas inox 220V', 'inox', 'inox 220V', '220V']
         ),
        ('com conexao usbmicro sdp2  ph095',
         ['', 'com', 'com conexao', 'com conexao usbmicro', 'conexao',
          'conexao usbmicro', 'conexao usbmicro sdp2', 'usbmicro',
          'usbmicro sdp2', 'usbmicro sdp2 ph095', 'sdp2', 'sdp2 ph095',
          'ph095']
         ),
        ('5 velocidades com filtro inox 500w',
         ['', '5', '5 velocidades', '5 velocidades com', 'velocidades',
          'velocidades com', 'velocidades com filtro', 'com', 'com filtro',
          'com filtro inox', 'filtro', 'filtro inox', 'filtro inox 500w',
          'inox', 'inox 500w', '500w']
         ),
        ('', ['']),
    ])
    def test_should_create_ngrams(self, analyzer, reference, expected_ngrams):
        assert (
            expected_ngrams ==
            analyzer.generate_ngrams_for_variation_reference(reference)
        )
