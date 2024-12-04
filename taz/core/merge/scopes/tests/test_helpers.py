from taz.core.merge.scopes.helpers import normalize_attributes


class TestNormalizeAttributes:

    def test_when_normalize_attributes_then_return_all_attributes_normalized(  # noqa
        self
    ):
        assert normalize_attributes({'Cor': 'Preto'}) == [{
            'type': 'color',
            'value': 'Preto'
        }]

    def test_when_normalize_attributes_not_mapped_then_return_all_attributes_normalized(  # noqa
        self
    ):
        assert normalize_attributes({'Seletor': 'Preto'}) == [{
            'type': 'seletor',
            'value': 'Preto'
        }]

    def test_when_normalize_attributes_without_value_then_remove_attribute(  # noqa
        self
    ):
        assert normalize_attributes({'Seletor': ''}) == []
