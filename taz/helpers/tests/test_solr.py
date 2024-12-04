from taz.helpers.solr import convert_id_to_solr_format


class TestSolrHelpers:

    def test_should_convert_to_solr_format(self):
        solr_variation = convert_id_to_solr_format('200161300')
        assert solr_variation == '2001613'

    def test_should_convert_to_solr_format_with_alphanumeric(self):
        solr_variation = convert_id_to_solr_format('jbhdah04ae')
        assert solr_variation == 'jbhdah04ae'
