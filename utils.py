
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


def str_to_type(type_text):
        type_dict = {
            'LargeText': QuestionType.LARGE_TEXT,
            'Checkbox': QuestionType.CHECKBOX,
            'Radio': QuestionType.RADIO
        }
        return type_dict.get(type_text, QuestionType.LARGE_TEXT)
