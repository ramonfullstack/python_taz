import pytest

from taz.api.scores.common.samples import ScoreSamples


@pytest.fixture
def save_scores(mongo_database):
    mongo_database.get_collection('scores').save(
        ScoreSamples.score_a()
    )
    mongo_database.get_collection('scores').save(
        ScoreSamples.score_b()
    )
    mongo_database.get_collection('scores').save(
        ScoreSamples.score_c()
    )
    mongo_database.get_collection('scores').save(
        ScoreSamples.score_d()
    )
    mongo_database.get_collection('scores').save(
        ScoreSamples.score_e()
    )


@pytest.fixture
def save_inactive_score(mongo_database):
    score = ScoreSamples.score_a()
    score['active'] = False
    score['version'] = 'v0_0_0'
    score['final_score'] = 50.0
    for source in score['sources']:
        source['points'] = 50.0

    mongo_database.get_collection('scores').save(score)


@pytest.fixture
def save_other_seller_score(mongo_database):
    score = ScoreSamples.score_a()
    score['sku'] = '987654321'
    score['seller_id'] = 'madeiramadeira'

    mongo_database.get_collection('scores').save(score)
