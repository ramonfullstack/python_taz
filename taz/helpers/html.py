from bs4 import BeautifulSoup
from html_sanitizer import Sanitizer


def fix_broken_tags(raw_text):
    text = str(BeautifulSoup(raw_text, 'html5lib'))
    text = text.replace('<html><head></head><body>', '')
    text = text.replace('</body></html>', '')
    text = text.replace('\xa0', ' ')
    text = text.replace('\n', '')
    text = text.replace('\r', '')
    text = text.replace('\t', '')
    text = ' '.join(text.split())
    return text


def remove_html_tags(raw_text):
    text = BeautifulSoup(raw_text, 'html5lib')
    text = text.get_text()
    text = text.replace('\n', '')
    text = text.replace('\r', '')
    text = text.replace('\t', '')
    text = text.replace('\\s+', '')
    text = text.replace('&nbsp', '')
    text = text.replace('\xa0', ' ')
    text = ' '.join(text.split())
    return text


def clean_html_string(value, tags=None, empty=None):
    default_tags = {
        'p', 'br', 'span', 'b', 'strong', 'i', 'em',
        'mark', 'small', 'del', 'ins', 'sub', 'sup', 'li', 'ul'
    }
    default_empty = {'br'}

    sanitizer = Sanitizer({
        'tags': tags or default_tags,
        'attributes': {},
        'empty': default_empty if empty is None else empty,
        'separate': {},
        'whitespace': {},
        'keep_typographic_whitespace': False,
        'element_postprocessors': [
            remove_tag
        ],
        'is_mergeable': lambda e1, e2: False,
    })

    return sanitizer.sanitize(value)


def remove_tag(element):
    if element.tag == 'table':
        element.clear()
    return element
