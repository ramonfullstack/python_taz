import pytest

from taz.consumers.rebuild.scopes.matching_omnilogic import (
    RebuildMatchingOmnilogic
)


class TestRebuildMatchingOmnilogic:

    @pytest.fixture
    def rebuild(self):
        return RebuildMatchingOmnilogic()

    @pytest.fixture
    def product(self):
        return {
            'sku': '11673',
            'entity': 'Livro',
            'metadata': {
                'ISBN-13': '9788572885546',
                'ISBN-10': '8572885544',
                'Gênero': 'Física'
            },
            'seller_id': 'florencedistdelivrosltda',
            'navigation_id': '5939158',
            'category_id': 'LI',
            'subcategory_ids': ['LFIK', 'LIEX'],
            'product_hash': 'a2db8097e5b1eeabf0d33a182340c9be',
            'product_name': 'Livro - Mecânica Ortodôntica Corretiva em Typodont - Classe II- Vedovello - Santos',  # noqa
            'product_matching_metadata': ['ISBN-10', 'ISBN-13'],
            'product_name_metadata': ['ISBN-10', 'ISBN-13', 'Gênero'],
            'sku_metadata': [],
            'filters_metadata': ['ISBN-10', 'ISBN-13', 'Gênero', 'Autor', 'Tipo de Edição', 'Volume', 'Editora', 'Edição'],  # noqa
            'source': 'magalu',
            'timestamp': 1583874972.0727918
        }

    def test_rebuild_returns_not_found(self, rebuild, patch_publish_manager):
        data = {'entity': 'Livro'}

        with patch_publish_manager as mock_pubsub:
            rebuild.rebuild('update', data)

        assert mock_pubsub.call_count == 0

    def test_rebuild_success(
        self,
        rebuild,
        product,
        mongo_database,
        patch_publish_manager
    ):
        mongo_database.enriched_products.save(product)

        data = {'entity': product['entity']}

        with patch_publish_manager as mock_pubsub:
            ret = rebuild.rebuild('update', data)

        assert mock_pubsub.call_count == 1
        assert ret is True
