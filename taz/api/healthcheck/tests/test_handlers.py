from taz.api.version import __version__


class TestHealthCheck:

    def test_return_ok_for_health_check(self, client):
        result = client.simulate_get('/healthcheck')

        assert result.json['status'] == 'OK'
        assert result.json['version'] == __version__
        assert 'host' in result.json
