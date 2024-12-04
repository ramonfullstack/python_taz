import logging

logger = logging.getLogger(__name__)


class DiffMixin:

    def lists_differ(self, list_a, list_b):
        if (
            self.has_nested_type(list, list_a) or
            self.has_nested_type(list, list_b)
        ):
            return self.compare_types(list, list_a, list_b)
        elif (
            self.has_nested_type(dict, list_a) or
            self.has_nested_type(dict, list_b)
        ):
            return self.compare_types(dict, list_a, list_b)
        else:
            normalized_list_a = self._normalize_primitives(list_a)
            normalized_list_b = self._normalize_primitives(list_b)
            a_minus_b_differs = len(
                set(normalized_list_a) - set(normalized_list_b)
            ) > 0
            b_minus_a_differs = len(
                set(normalized_list_b) - set(normalized_list_a)
            ) > 0
            return a_minus_b_differs or b_minus_a_differs

    def has_divergent_values(self, dict_a, dict_b):
        if not dict_a and not dict_b:
            return False

        if (
            self.has_nested_type(dict, dict_a) or
            self.has_nested_type(dict, dict_b)
        ):
            return self.compare_types(dict, dict_a, dict_b)
        else:
            return self.lists_differ(dict_b.values(), dict_a.values())

    def diff_items(self, dict_a, dict_b):
        keys = []
        for k, v in dict_b.items():
            if k not in dict_a:
                keys.append((k, None))
                logger.debug('Change detected: {}'.format(k))
                continue

            [keys.append((k, i_id)) for i_id in v if i_id not in dict_a[k]]

        return keys

    def diff_updated_items(self, current_dataset, previous_dataset):
        updated_keys = []
        for k in current_dataset:
            if k not in previous_dataset:
                continue

            for i_id in current_dataset[k]:
                if i_id not in previous_dataset[k]:
                    continue

                if self.has_divergent_values(
                    current_dataset[k][i_id],
                    previous_dataset[k][i_id]
                ):
                    updated_keys.append((k, i_id))

        return updated_keys

    def diff_with_items(self, dataset_a, dataset_b):
        result = self.diff_items(dataset_a, dataset_b)

        items = []

        for scope, key in result:
            if key:
                items.append(dataset_b[scope][key])
            else:
                [
                    items.append(dataset_b[scope][key])
                    for key in dataset_b[scope]
                ]

        return items

    def diff_deleted(self, current_dataset, previous_dataset):
        result = self.diff_with_items(
            current_dataset,
            previous_dataset
        )
        return result

    def diff_inserted(self, current_dataset, previous_dataset):
        result = self.diff_with_items(
            previous_dataset,
            current_dataset
        )
        return result

    def diff_updated(self, current_dataset, previous_dataset):
        updated = self.diff_updated_items(current_dataset, previous_dataset)

        items = [current_dataset[scope][key] for scope, key in updated]

        return items

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

    def diff(self, current_dataset, previous_dataset):
        logger.debug('Current dataset is: {} Previous dataset was: {}'.format(
            current_dataset,
            previous_dataset,
        ))

        sorted_current_dataset = self.sort_dict(current_dataset)
        sorted_previous_dataset = self.sort_dict(previous_dataset)

        return (
            self.diff_deleted(
                sorted_current_dataset,
                sorted_previous_dataset,
            ),
            self.diff_inserted(
                sorted_current_dataset,
                sorted_previous_dataset,
            ),
            self.diff_updated(
                sorted_current_dataset,
                sorted_previous_dataset,
            ),
        )
