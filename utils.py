import re
import logging
from model import QuestionType

logging.basicConfig(level=logging.INFO, filename='logs\\info.log')
logger_io = logging.getLogger('IO')
logger_process = logging.getLogger('process')


def is_empty(string):
    """
    This method verifies if the given string is empty
    '' ---> True
    None ---> True
    'None' ---> True
    """
    return string is None or not string.strip() or string == 'None'


def is_empty_with_none(string):
    """
    This method verifies if the given string is empty
    '' ---> True
    None ---> True
    """
    return string is None or not string.strip()


def format_filename(string):
    filename = string.replace(' ', '_')
    filename = ''.join(c
                       .replace('/', '_')
                       .replace('(', '')
                       .replace(')', '')
                       .replace('@', '_')
                       .replace('*', '')
                       .replace('&', '_')
                       .replace('$', '')
                       .replace('+', '')
                       for c in filename)
    return filename


def replace_ignore(str_val, old, new):
    pattern = re.compile(re.escape(old), re.IGNORECASE)
    return pattern.sub(new, str_val)


def wrap_padding(value):
    return '##' + value + '##'


def str_to_type(type_text):
    type_dict = {
        'LargeText': QuestionType.LARGE_TEXT,
        'Checkbox': QuestionType.CHECKBOX,
        'Radio': QuestionType.RADIO
    }
    return type_dict.get(type_text, QuestionType.LARGE_TEXT)


def join_with_commas(list_, op=lambda x: x):
    with_comma = ', '.join([op(e) for e in list_ if e is not None])
    at_last = with_comma.rsplit(',', 1)
    if len(at_last) > 1:
        with_comma = at_last[0] + ' and' + at_last[1]
    return with_comma
