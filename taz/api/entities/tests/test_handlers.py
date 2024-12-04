import pytest


class TestEntitiesHandler:

    @pytest.fixture
    def save_enriched_products(
        self,
        mongo_database
    ):
        for entity in ('Celular', 'Fritadeira Elétrica'):
            mongo_database.enriched_products.save(
                {'entity': entity}
            )

    def test_get_entities_should_return_entities(
        self,
        client,
        save_enriched_products
    ):
        response = client.get('/entity/list')

        assert response.status_code == 200
        assert response.json == {'data': ['Celular', 'Fritadeira Elétrica']}

    def test_get_without_entities_should_return_empty_list(self, client):
        response = client.get('/entity/list')

        assert response.status_code == 200
        assert response.json == {'data': []}
