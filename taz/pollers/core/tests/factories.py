from collections import OrderedDict
from decimal import Decimal


class BaseFactory:

    @classmethod
    def sort_dict(cls, unsorted_dict):
        """
        The dict that the base poller receives
        must be properly sorted. This can be
        ensured by sorting the database query,
        but on tests this must be done manually.
        """

        return OrderedDict(
            sorted(
                unsorted_dict.items(),
                key=lambda k: k[0]
            )
        )


class ItemFactory(BaseFactory):  # pragma: no cover

    @classmethod
    def group_a(cls):
        return {
            'group_a': {
                'item_a': {
                    'absolute_price': Decimal('299.00'),
                    'attr_type': 'sku',
                    'attr_value': 'item_a',
                    'rule_type': 'campaign',
                },
                'item_b': {
                    'absolute_price': Decimal('129.90'),
                    'attr_type': 'sku',
                    'attr_value': 'item_b',
                    'rule_type': 'campaign',
                },
                'item_c': {
                    'absolute_price': Decimal('649.90'),
                    'attr_type': 'sku',
                    'attr_value': 'item_c',
                    'rule_type': 'campaign',
                }
            }
        }

    @classmethod
    def group_c(cls):
        return {
            'group_c': {
                'item_d': {
                    'absolute_price': Decimal('119.90'),
                    'attr_type': 'sku',
                    'attr_value': 'item_d',
                    'rule_type': 'campaign',
                },
                'item_j': {
                    'absolute_price': Decimal('199.90'),
                    'attr_type': 'sku',
                    'attr_value': 'item_j',
                    'rule_type': 'campaign',
                },
                'item_e': {
                    'absolute_price': Decimal('399.00'),
                    'attr_type': 'sku',
                    'attr_value': 'item_e',
                    'rule_type': 'campaign',
                }
            }
        }

    @classmethod
    def fake_storage_item(cls):
        item = cls.group_a()

        item.update(cls.group_c())

        return cls.sort_dict(item)

    @classmethod
    def fake_storage_item_2(cls):
        item = {
            'campaign_200_9829': {
                'item_a': {
                    'absolute_price': Decimal('299.00'),
                    'attr_type': 'sku',
                    'attr_value': 'item_a',
                    'rule_type': 'campaign',
                },
            }
        }

        item.update(cls.group_a())
        item.update(cls.group_c())

        return cls.sort_dict(item)

    @classmethod
    def fake_deleted_item(cls):
        item = cls.group_a()
        return cls.sort_dict(item)

    @classmethod
    def diff_group_a(cls):
        return {
            'group_a': {
                'item_a': {
                    'absolute_price': Decimal('199.00'),
                    'attr_type': 'sku',
                    'attr_value': 'item_a',
                    'rule_type': 'campaign',
                },
                'item_b': {
                    'absolute_price': Decimal('129.90'),
                    'attr_type': 'sku',
                    'attr_value': 'item_b',
                    'rule_type': 'campaign',
                },
                'item_c': {
                    'absolute_price': Decimal('349.90'),
                    'attr_type': 'sku',
                    'attr_value': 'item_c',
                    'rule_type': 'campaign',
                }
            }
        }

    @classmethod
    def diff_group_b(cls):
        return {
            'group_b': {
                'item_g': {
                    'absolute_price': Decimal('399.00'),
                    'attr_type': 'sku',
                    'attr_value': 'item_g',
                    'rule_type': 'campaign',
                },
                'item_h': {
                    'absolute_price': Decimal('399.00'),
                    'attr_type': 'sku',
                    'attr_value': 'item_h',
                    'rule_type': 'campaign',
                }
            }
        }

    @classmethod
    def diff_group_c(cls):
        return {
            'group_c': {
                'item_d': {
                    'absolute_price': Decimal('119.90'),
                    'attr_type': 'sku',
                    'attr_value': 'item_d',
                    'rule_type': 'campaign',
                },
                'item_e': {
                    'absolute_price': Decimal('399.00'),
                    'attr_type': 'sku',
                    'attr_value': 'item_e',
                    'rule_type': 'campaign',
                },
                'item_f': {
                    'absolute_price': Decimal('399.00'),
                    'attr_type': 'sku',
                    'attr_value': 'item_f',
                    'rule_type': 'campaign',
                }
            }
        }

    @classmethod
    def diff_group_d(cls):
        return {
            'group_d': {
                'item_i': {
                    'absolute_price': Decimal('399.00'),
                    'attr_type': 'sku',
                    'attr_value': 'item_i',
                    'rule_type': 'campaign',
                }
            }
        }

    @classmethod
    def fake_diff_previous(cls):
        item = cls.diff_group_a()

        item.update(cls.diff_group_b())
        item.update(cls.diff_group_c())

        return cls.sort_dict(item)

    @classmethod
    def fake_diff_current(cls):
        item = cls.group_a()

        item.update(cls.diff_group_d())
        item.update(cls.group_c())

        return cls.sort_dict(item)

    @classmethod
    def fake_diff_current_with_nested(cls):
        item = {
            'group_a': {
                'item_a': {
                    'absolute_price': Decimal('299.00'),
                    'attr_type': 'sku',
                    'attr_value': 'item_a',
                    'rule_type': 'campaign',
                    'another_nested_node': {
                        '1': 10,
                        '2': 5,
                    },
                    'nested_node': {
                        'absolute_price': Decimal('199.00'),
                        'attr_type': 'sku',
                        'attr_value': 'item_a',
                        'rule_type': 'campaign',
                    }
                },
                'item_b': {
                    'absolute_price': Decimal('129.90'),
                    'attr_type': 'sku',
                    'attr_value': 'item_b',
                    'rule_type': 'campaign',
                    'nested_list': [
                        {
                            'a': 1.9,
                            'b': 'x',
                            'd': 9
                        },
                        {
                            'a': 1.9,
                            'b': 'x',
                            'd': 9
                        }
                    ]
                },
                'item_c': {
                    'absolute_price': Decimal('649.90'),
                    'attr_type': 'sku',
                    'attr_value': 'item_c',
                    'rule_type': 'campaign',
                }
            }
        }

        item.update(cls.group_c())
        item.update(cls.diff_group_d())

        return cls.sort_dict(item)

    @classmethod
    def fake_diff_previous_with_nested(cls):
        item = {
            'group_a': {
                'item_a': {
                    'absolute_price': Decimal('299.00'),
                    'attr_type': 'sku',
                    'attr_value': 'item_a',
                    'rule_type': 'campaign',
                    'nested_node': {
                        'absolute_price': Decimal('299.00'),
                        'attr_type': 'sku',
                        'attr_value': 'item_a',
                        'rule_type': 'campaign',
                    },
                    'another_nested_node': {
                        '1': 19,
                        '2': 5,
                    }
                },
                'item_b': {
                    'absolute_price': Decimal('29.90'),
                    'attr_type': 'sku',
                    'attr_value': 'item_b',
                    'rule_type': 'campaign',
                    'nested_list': [
                        {
                            'a': 1.9,
                            'b': 'x',
                            'd': 9
                        },
                        {
                            'a': 1.9,
                            'b': 'x',
                            'd': 9
                        }
                    ]
                },
                'item_c': {
                    'absolute_price': Decimal('349.90'),
                    'attr_type': 'sku',
                    'attr_value': 'item_c',
                    'rule_type': 'campaign',
                }
            }
        }

        item.update(cls.diff_group_b())
        item.update(cls.diff_group_c())

        return cls.sort_dict(item)
