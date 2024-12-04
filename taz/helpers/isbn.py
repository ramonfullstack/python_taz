import isbnlib


def validate_isbn(value):
    if not value:
        return False

    return isbnlib.is_isbn13(value)
