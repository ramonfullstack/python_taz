from simple_settings import settings


def build_category_data(category, subcategory=None):
    if not subcategory:
        return settings.CATEGORY_PATH.format(
            category['slug'],
            category['id']
        ).lower()

    return settings.SUBCATEGORY_PATH.format(
        subcategory['slug'],
        category['slug'],
        category['id'],
        subcategory['id'],
    ).lower()
