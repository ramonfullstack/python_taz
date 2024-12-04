import pytest


class TestStockListHandler:

    @pytest.fixture
    def sku(self):
        return '123456'

    @pytest.fixture
    def seller_id(self):
        return 'murcho'

    @pytest.fixture
    def mock_url(self):
        return '/stocks/seller/{seller}/sku/{sku}'

    @pytest.fixture
    def save_stocks(self, mongo_database, sku, seller_id):
        payloads = [{
            'branch_id': 300,
            'seller_id': seller_id,
            'sku': sku,
            'latitude': -23.131369,
            'longitude': -46.95137,
            'type': 'DC',
            'position': {
                'physic': {
                    'amount': 185,
                    'reserved': 0,
                    'available': 185
                },
                'logic': {
                    'amount': 0,
                    'reserved': 0,
                    'available': 0
                }
            },
            'delivery_availability': 'nationwide',
            'navigation_id': sku,
            'last_updated_at': '2020-12-21T12:26:29.205190'
        }, {
            'branch_id': 595,
            'seller_id': seller_id,
            'sku': sku,
            'latitude': -23.519995,
            'longitude': -46.613525,
            'type': 'STORE',
            'position': {
                'physic': {
                    'amount': 4,
                    'reserved': 0,
                    'available': 4
                },
                'logic': {
                    'amount': 0,
                    'reserved': 0,
                    'available': 0
                }
            },
            'delivery_availability': 'regional',
            'navigation_id': sku,
            'last_updated_at': '2020-12-03T22:00:30.857776'
        }]

        for payload in payloads:
            mongo_database.stocks.save(payload)

    def test_get_stocks_returns_not_found(
        self,
        client,
        sku,
        seller_id,
        mock_url
    ):
        response = client.get(mock_url.format(sku=sku, seller=seller_id))

        assert response.status_code == 404

    def test_get_stocks_returns_list(
        self,
        client,
        sku,
        seller_id,
        mock_url,
        save_stocks
    ):
        response = client.get(mock_url.format(sku=sku, seller=seller_id))

        assert response.status_code == 200
        assert len(response.json) == 2
