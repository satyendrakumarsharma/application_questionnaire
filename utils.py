
import logging


logging.basicConfig(level=logging.INFO, filename='logs\\info.log')
logger = logging.getLogger('Application IO')


def is_empty(string):
    """
    This method verifies if the given string is empty
    '' ---> True
    None ---> True
    'None' ---> True
    """
    return string is None or not string.strip() or string == 'None'


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


