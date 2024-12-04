import pytest

from taz.pollers.category.converter import CategoryConverter


class TestCategoryConverter:

    @pytest.fixture
    def converter(self):
        return CategoryConverter()

    @pytest.fixture
    def subcategory_database_row(self):
        return [{
            'batch_key': 'SUBXA',
            'category_id': 'XA',
            'category_description': 'Xablau',
            'subcategory_id': 'XAPL',
            'subcategory_description': 'Xablau Xaplex',
            'subcategory_active': 1
        }]

    def test_database_convertion(
        self,
        converter,
        subcategory_database_row
    ):
        expected_transformed_set = {
            'SUBXA': {
                'XAPL': {
                    'id': 'XAPL',
                    'description': 'Xablau Xaplex',
                    'slug': 'xablau-xaplex',
                    'parent_id': 'XA',
                    'active': True
                }
            }
        }

        converter.from_source(subcategory_database_row)

        assert expected_transformed_set == converter.get_items()
