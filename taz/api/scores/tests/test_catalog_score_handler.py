import pytest

from taz.api.scores.common.samples import ScoreSamples

EXPECTED_LOG = 'Time elapsed to retrieve score aggregation'


class TestCatalogScoreHandler:

    @pytest.fixture
    def mock_url(self):
        return '/score/'

    @pytest.fixture
    def expected_categories(self):
        return [
            {
                'catalog_average_score': 100.0,
                'catalog_score_count': 1,
                'category_description': 'Casa e Serviços',
                'category_id': 'CS'
            }, {
                'catalog_average_score': 60.0,
                'catalog_score_count': 2,
                'category_description': 'Bijuterias e Relógios',
                'category_id': 'BR'
            }
        ]

    @pytest.fixture
    def save_active_scores(self, mongo_database):
        score = ScoreSamples.score_a()
        score['final_score'] = 100.125135453636434634634

        mongo_database.scores.save(score)

        score['_id'] = '5cb49cc32fac84cb2cd187a9'
        score['sku'] = '181160500'
        score['md5'] = '40a70a00979631dac768a14369601713'
        score['final_score'] = 60.543534534543543
        score['sources'][0]['points'] = 60.0
        mongo_database.scores.save(score)

    @pytest.fixture
    def save_inactive_scores(self, mongo_database):
        score = ScoreSamples.score_a()
        score['sku'] = '181160500'
        score['md5'] = '40a70a00979631dac768a14369601714'
        score['active'] = False
        mongo_database.scores.save(score)

    @pytest.fixture
    def save_active_category_scores(self, mongo_database):
        score = ScoreSamples.score_a()
        mongo_database.scores.save(score)

        score['_id'] = '5cb49cc32fac84cb2cd187bb'
        score['sku'] = '181160500'
        score['md5'] = '40a70a00979631dac768a14369601713'
        score['final_score'] = 60.0
        score['sources'][0]['points'] = 60.0
        mongo_database.scores.save(score)

        score['final_score'] = 20.0
        mongo_database.scores.save(score)

        score['_id'] = '5cb49cc32fac84cb2cd187cc'
        score['final_score'] = 100.0
        score['md5'] = '40a70a00979631dac768a14369601714'
        score['category_id'] = 'CS'
        mongo_database.scores.save(score)

        score['sku'] = '111111111'
        score['category_id'] = 'CS'
        score['timestamp'] = '123456'
        mongo_database.scores.save(score)

    @pytest.fixture
    def save_inactive_category_scores(self, mongo_database):
        score = ScoreSamples.score_a()
        score['md5'] = '40a70a00979631dac768a14369601741'
        score['sku'] = '181160500'
        score['active'] = False
        score['final_score'] = 50.0
        score['category_id'] = 'CS'
        score['sources'][0]['points'] = 60.0

        mongo_database.scores.save(score)

    @pytest.fixture
    def save_categories(self, mongo_database, expected_categories):
        mongo_database.categories.save({
            'id': expected_categories[0]['category_id'],
            'description': expected_categories[0]['category_description'],
            'slug': 'casa',
            'parent_id': 'ML'
        })

        mongo_database.categories.save({
            'id': expected_categories[1]['category_id'],
            'description': expected_categories[1]['category_description'],
            'slug': 'bijuterias',
            'parent_id': 'ML'
        })

    @pytest.fixture
    def save_categories_without_description(
        self, mongo_database, expected_categories
    ):
        mongo_database.categories.save({
            'id': expected_categories[0]['category_id'],
            'description': expected_categories[0]['category_description'],
            'slug': 'casa',
            'parent_id': 'ML'
        })

        mongo_database.categories.save({
            'id': expected_categories[1]['category_id'],
            'slug': 'bijuterias',
            'parent_id': 'ML'
        })

    def test_should_calculate_full_catalog_score(
        self,
        client,
        mock_url,
        save_active_scores,
        save_categories,
        logger_stream
    ):
        response = client.get(mock_url)
        log = logger_stream.getvalue()

        assert response.json['data']['catalog_average_score'] == 80.33
        assert response.status_code == 200
        assert EXPECTED_LOG in log

    def test_should_calculate_full_catalog_score_ignoring_not_active_scores(
        self,
        client,
        mock_url,
        save_active_scores,
        save_categories,
        logger_stream
    ):
        response = client.get(mock_url)
        log = logger_stream.getvalue()

        assert response.json['data']['catalog_average_score'] == 80.33
        assert response.status_code == 200
        assert EXPECTED_LOG in log

    def test_should_calculate_full_catalog_score_return_skus_count(
        self,
        client,
        mock_url,
        save_active_scores,
        save_categories,
        logger_stream
    ):
        response = client.get(mock_url)
        log = logger_stream.getvalue()
        assert response.json['data']['catalog_score_count'] == 2
        assert response.status_code == 200
        assert EXPECTED_LOG in log

    def test_should_return_404_in_case_empty_scores_collection(
        self,
        mock_url,
        client
    ):
        response = client.get(mock_url)

        assert response.status_code == 404

    def test_should_calculate_category_catalog_score_and_ignore_items_not_active(  # noqa
        self,
        client,
        mock_url,
        expected_categories,
        save_active_category_scores,
        save_categories,
        logger_stream
    ):
        response = client.get(mock_url)
        log = logger_stream.getvalue()

        assert response.status_code == 200
        assert response.json['data']['categories'] == expected_categories
        assert EXPECTED_LOG in log

    def test_should_use_hyphen_in_category_description_if_does_not_find_description( # noqa
        self,
        client,
        mock_url,
        expected_categories,
        save_active_category_scores,
        save_categories_without_description,
        logger_stream
    ):
        response = client.get(mock_url)
        log = logger_stream.getvalue()

        expected_categories[1]['category_description'] = '-'
        assert response.status_code == 200
        assert response.json['data']['categories'] == expected_categories
        assert EXPECTED_LOG in log
