from datetime import datetime
def is_isbn_or_key(word):
    """
    接受一个字符串，返回这个字符串是ISBN还是关键字
    :param word: string ''
    :return: 'isbn' or 'key'
    """
    isbn_or_key = 'key'
    if len(word) == 13 and word.isdigit():
        isbn_or_key = 'isbn'
    short_word = word.replace('-', '')
    if '-' in word and len(short_word) == 10 and short_word.isdigit():
        isbn_or_key = 'isbn'
    return isbn_or_key


def timestamp():
    return datetime.now().timestamp()