from collections import OrderedDict
from operator import itemgetter


class SortMixin:

    def _sort_not_iterable_values(self, unsorted_list):
        sorted_list = []

        for not_iterable_type in [int, bool, str]:
            if any(
                isinstance(i, not_iterable_type) for i in unsorted_list
            ):
                list_of_ints = [
                    unsorted_item
                    for unsorted_item in unsorted_list
                    if isinstance(unsorted_item, not_iterable_type)
                ]
                sorted_list += sorted(list_of_ints)

        return sorted_list

    def sort_list(self, unsorted_list):
        sorted_list = self._sort_not_iterable_values(unsorted_list)

        if any(isinstance(i, list) for i in unsorted_list):
            sorted_list += [
                self.sort_list(unsorted_item)
                for unsorted_item in unsorted_list
                if isinstance(unsorted_item, list)
            ]

        if any(isinstance(i, dict) for i in unsorted_list):
            common_key_name = self._find_common_key_name(unsorted_list)

            if not common_key_name:
                return unsorted_list

            sorted_list += sorted(
                [
                    self.sort_dict(unsorted_item)
                    for unsorted_item in unsorted_list
                    if isinstance(unsorted_item, dict)
                ],
                key=itemgetter(common_key_name),
            )

        return sorted_list

    def _find_common_key_name(self, unsorted_list_of_dicts):
        common_keys = sorted(set.intersection(
            *sorted([
                set([
                    k for k, v in d.items()
                    if not isinstance(v, list)
                ])
                for d in unsorted_list_of_dicts
                if isinstance(d, dict)
            ])
        ))

        if common_keys:
            return common_keys[0]

    def sort_dict(self, unsorted_dict):
        """
        Here I sort any nested dict by key to avoid
        a wrong diff computation.
        Nested lists of dicts MUST HAVE same structure so the sorting can be
        precisely determined.
        """
        sorted_dict = OrderedDict()
        for k, v in sorted(unsorted_dict.items()):
            if isinstance(v, dict):
                sorted_dict[k] = self.sort_dict(v)
            elif isinstance(v, list):
                sorted_dict[k] = self.sort_list(v)
            else:
                sorted_dict[k] = v

        return sorted_dict
