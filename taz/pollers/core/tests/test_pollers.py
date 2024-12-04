from collections import OrderedDict
from decimal import Decimal

import pytest

from taz.pollers.core.base import Poller
from taz.pollers.core.tests.factories import ItemFactory


class TestBasePoller:

    @pytest.fixture
    def poller(self):
        class FakePoller(Poller):
            scope = 'fake'
            data_source = 'fake'

            def poll(self):
                return

            def get_converter(self):
                return

            def get_data_source(self):
                return

            def get_sender(self):
                return

        return FakePoller()

    @pytest.fixture
    def dict_with_nested_objects(self):
        return {
            'c': 1,
            'b': 3,
            'a': [3, 9, 2],
            'd': {
                'y': 0,
                'z': 3,
                'x': 9,
            },
        }

    @pytest.fixture
    def dataset_a(self):
        return {'a': {'x': {'z': 1.09, 'q': 5}}}

    @pytest.fixture
    def dataset_b(self):
        return {'a': {'x': {'q': 5, 'z': Decimal('1.09')}}}

    @pytest.fixture
    def object_with_nested_objects(self):
        return {
            'c': 1,
            'b': 3,
            'a': [3, 9, 2],
            'd': {
                'y': 0,
                'z': 3,
                'x': 9,
            },
        }

    def test_sort_dict(self, poller, object_with_nested_objects):
        sorted_dict = poller.sort_dict(object_with_nested_objects)
        sorted_dict_keys = list(sorted_dict.keys())

        assert sorted_dict_keys[0] == 'a'
        assert sorted_dict_keys[1] == 'b'
        assert sorted_dict_keys[2] == 'c'
        assert sorted_dict_keys[3] == 'd'

        nested_dict_keys = list(sorted_dict['d'].keys())
        assert nested_dict_keys[0] == 'x'
        assert nested_dict_keys[1] == 'y'
        assert nested_dict_keys[2] == 'z'

        nested_list = sorted_dict['a']
        assert nested_list[0] == 2
        assert nested_list[1] == 3
        assert nested_list[2] == 9

    @pytest.mark.parametrize('unsorted_list,expected_sorted_list', [
        (
            [
                {'a': 3}, {'a': 1}, {'a': 2},
                [6, 2, 7, 1],
                'z', 'x',
                9, 1, 3
            ],
            [
                1, 3, 9,
                'x', 'z',
                [1, 2, 6, 7],
                OrderedDict([('a', 1)]),
                OrderedDict([('a', 2)]),
                OrderedDict([('a', 3)])
            ]
        ),
        (
            [
                {
                    'b': 'y',
                    'a': 'x'
                }
            ],
            [
                {
                    'a': 'x',
                    'b': 'y'
                }
            ]
        ),
        (
            [
                {
                    'x': [
                        {
                            'z': '8',
                            'c': '7'
                        },
                        {
                            'a': '1',
                            'b': '2'
                        }
                    ],
                    'z': '2'
                },
                {
                    'x': [
                        {
                            'b': '2',
                            'a': '1'
                        },
                        {
                            'd': '4',
                            'c': '3'
                        }
                    ],
                    'z': '9'
                }
            ],
            [
                {
                    'z': '2',
                    'x': [
                        {
                            'z': '8',
                            'c': '7'
                        },
                        {
                            'a': '1',
                            'b': '2'
                        }
                    ]
                },
                {
                    'x': [
                        {
                            'b': '2',
                            'a': '1'
                        },
                        {
                            'd': '4',
                            'c': '3'
                        }
                    ],
                    'z': '9'
                }
            ]
        )
    ])
    def test_sort_list(self, poller, unsorted_list, expected_sorted_list):
        sorted_list = poller.sort_list(unsorted_list)

        assert sorted_list == expected_sorted_list

    def test_sort_unequal_list_of_dicts_doesnt_sort_at_all(self, poller):
        expected_sorted_list = [{'a': 5}, {'x': 2}, {'q': 78}]
        sorted_list = poller.sort_list(expected_sorted_list)
        assert sorted_list == expected_sorted_list

    def test_strip_dict_from_dict(self, poller, dict_with_nested_objects):
        dicts, dictless = poller.strip_type(
            dict,
            dict_with_nested_objects
        )

        assert len(dicts) == 1
        assert dicts == [dict_with_nested_objects['d']]

        assert len(dictless) == 3
        assert dict_with_nested_objects['d'] not in dictless

    def test_strip_list_from_dict(self, poller, dict_with_nested_objects):
        lists, _ = poller.strip_type(
            list,
            dict_with_nested_objects
        )

        assert len(lists) == 1
        assert lists == [dict_with_nested_objects['a']]

    def test_lists_differ(self, poller):
        list_a_differs = poller.lists_differ([1, 2, 3], [1, 2])
        assert list_a_differs is True

        list_b_differs = poller.lists_differ([1, 2], [1, 2, 3])
        assert list_b_differs is True

        list_b_differs = poller.lists_differ([1, {'a': 2}], [1, 2, 3])
        assert list_b_differs is True

    def test_diff_deleted_sub_item(self, poller):
        base_set = ItemFactory.fake_storage_item()
        deleted_set = ItemFactory.fake_deleted_item()
        del deleted_set['group_a']['item_b']

        deleted = [
            i['attr_value']
            for i in poller.diff_deleted(
                deleted_set,
                base_set,
            )
        ]

        assert len(deleted) == 4
        assert 'item_b' in deleted
        assert 'item_d' in deleted
        assert 'item_e' in deleted
        assert 'item_j' in deleted

    def test_diff_deleted_messages_generation_one_item(self, poller):
        base_set = ItemFactory.fake_storage_item()
        deleted_set = ItemFactory.fake_storage_item()
        del deleted_set['group_a']['item_b']

        deleted = poller.diff_deleted(deleted_set, base_set)

        assert deleted[0]['attr_value'] == 'item_b'

    def test_diff_deleted_messages_generation_hole_scope(self, poller):
        base_set = ItemFactory.fake_storage_item()
        deleted_set = ItemFactory.fake_deleted_item()

        deleted_items = poller.diff_deleted(deleted_set, base_set)
        deleted_keys = [k['attr_value'] for k in deleted_items]

        assert len(deleted_keys) == 3

        assert 'item_d' in deleted_keys
        assert 'item_j' in deleted_keys
        assert 'item_e' in deleted_keys

    def test_diff_inserted_sub_item(self, poller):
        base_set = ItemFactory.fake_storage_item_2()
        inserted_set = ItemFactory.fake_storage_item_2()
        inserted_set['campaign_200_9829']['item_e'] = {
            'absolute_price': Decimal('399.00'),
            'attr_type': 'sku',
            'attr_value': 'item_e',
            'rule_type': 'campaign',
        }

        inserted = [
            i['attr_value']
            for i in poller.diff_inserted(
                inserted_set,
                base_set,
            )
        ]

        assert len(inserted) == 1
        assert 'item_e' in inserted

    def test_diff_inserted_message_generation_one_item(self, poller):
        base_set = ItemFactory.fake_storage_item_2()
        inserted_set = ItemFactory.fake_storage_item_2()
        inserted_set['campaign_200_9829']['item_e'] = {
            'absolute_price': Decimal('399.00'),
            'attr_type': 'sku',
            'attr_value': 'item_e',
            'rule_type': 'campaign',
        }

        inserted = poller.diff_inserted(inserted_set, base_set)

        assert inserted[0]['attr_value'] == 'item_e'

    def test_diff_inserted_message_generation_hole_scope(self, poller):
        base_set = ItemFactory.fake_deleted_item()
        inserted_set = ItemFactory.fake_storage_item()

        inserted_items = poller.diff_inserted(inserted_set, base_set)
        inserted = [k['attr_value'] for k in inserted_items]

        assert len(inserted) == 3
        assert 'item_d' in inserted
        assert 'item_j' in inserted
        assert 'item_e' in inserted

    def test_diff_updated_sub_item(self, poller):
        base_set = ItemFactory.fake_storage_item()
        updated_set = ItemFactory.fake_storage_item()
        updated_set['group_a']['item_b']['absolute_price'] = Decimal('119.90')
        updated_set['group_c']['item_e']['absolute_price'] = Decimal('99.50')

        updated_keys = poller.diff_updated_items(updated_set, base_set)

        scopes = [k for k, id in updated_keys]
        ids = [id for k, id in updated_keys]

        assert 'group_a' in scopes
        assert 'group_c' in scopes

        assert 'item_b' in ids
        assert 'item_e' in ids

    def test_diff_updated(self, poller):
        base_set = ItemFactory.fake_storage_item()
        updated_set = ItemFactory.fake_storage_item()
        updated_set['group_a']['item_b'] = {
            'attr_type': 'sku',
            'attr_value': 'item_b',
            'absolute_price': Decimal('199.00'),
            'rule_type': 'campaign',
        }

        updated_set['group_a']['item_c'] = {
            'attr_type': 'sku',
            'attr_value': 'item_c',
            'rule_type': 'campaign',
            'absolute_price': Decimal('619.90')
        }

        updated = [
            i['attr_value']
            for i in poller.diff_updated(
                updated_set,
                base_set
            )
        ]

        assert 'item_b' in updated
        assert 'item_c' in updated

    def test_diff(self, poller):
        previous_dataset = ItemFactory.fake_diff_previous()
        current_dataset = ItemFactory.fake_diff_current()

        deleted, inserted, updated = poller.diff(
            current_dataset,
            previous_dataset
        )

        assert len(deleted) == 3
        assert len(inserted) == 2
        assert len(updated) == 2

    def test_diff_subdiffs(self, poller):
        previous_dataset = ItemFactory.fake_diff_previous_with_nested()
        current_dataset = ItemFactory.fake_diff_current_with_nested()

        deleted, inserted, updated = poller.diff(
            current_dataset,
            previous_dataset
        )

        assert len(deleted) == 3
        assert len(inserted) == 2
        assert len(updated) == 3

    @pytest.mark.parametrize('dict_a', [
        OrderedDict([('a', []), ('b', ['x']), ('c', [])]),
    ])
    def test_has_nested_type(self, poller, dict_a):
        havent_nested_dicts = poller.has_nested_type(
            dict,
            dict_a
        )
        assert havent_nested_dicts is False

        have_nested_dicts = poller.has_nested_type(
            dict,
            ItemFactory.fake_diff_current_with_nested()
        )
        assert have_nested_dicts is True

    @pytest.mark.parametrize('dict_a,dict_b,expected', [
        (
            OrderedDict([('a', []), ('b', ['x']), ('c', [])]),
            OrderedDict([('a', []), ('b', ['x']), ('c', [])]),
            False
        ),
        (
            OrderedDict([('a', []), ('b', ['x']), ('c', [])]),
            OrderedDict([('a', []), ('b', ['x', 'z']), ('c', [])]),
            True
        ),
        (
            OrderedDict([('a', []), ('b', ['x', 'z']), ('c', [])]),
            OrderedDict([('a', []), ('b', ['x']), ('c', [])]),
            True
        )
    ])
    def test_has_divergent_values(self, poller, dict_a, dict_b, expected):
        has_divergent_values = poller.has_divergent_values(dict_a, dict_b)
        assert has_divergent_values is expected

        assert not poller.has_divergent_values({}, {})

    def test_dataset_diff_must_preserve_types(
        self,
        poller,
        dataset_a,
        dataset_b
    ):
        deleted, inserted, updated = poller.diff(
            dataset_a,
            dataset_b
        )

        assert len(deleted) == 0
        assert len(inserted) == 0
        assert len(updated) == 0
