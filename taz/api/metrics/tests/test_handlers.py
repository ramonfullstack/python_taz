import pytest


class TestMetricHandler:

    @pytest.fixture
    def save_catalog_metrics(self, mongo_database):
        metrics = [
            {'total_sellers': 30},
            {'active_sellers': 25},
            {'inactive_sellers': 5},
            {'total_entities': 3}
        ]
        for metric in metrics:
            for metric_name in metric.keys():
                mongo_database.metrics.save({
                    'type': metric_name,
                    'value': metric[metric_name]
                })

    def test_handler_returns_metrics(self, client, save_catalog_metrics):

        result = client.get(
            '/metrics/'
        )

        assert result.status_code == 200

        assert b'taz_total_sellers' in result.content
        assert b'total_sellers' in result.content

        assert b'taz_inactive_sellers' in result.content
        assert b'inactive_sellers' in result.content

        assert b'taz_active_sellers' in result.content
        assert b'active_sellers' in result.content

        assert b'taz_total_entities' in result.content
        assert b'total_entities' in result.content
