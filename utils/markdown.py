def bold_text(text: str) -> str:
    '''
    Жирный текст
    :param text:
    :return:
    '''
    return f'<b>{text}</b>'


def under_text(text: str) -> str:
    '''
    Подчёркнутый текст
    :param text:
    :return:
    '''
    return f'<u>{text}</u>'


def hyper_text(text: str, url: str) -> str:
    '''
    Гипертекст
    :param text:
    :param url:
    :return:
    '''
    return f'<a href="{url}">{text}</a>'


def strikethrough_text(text: str) -> str:
    '''
    Зачёркнутый текст
    :param text:
    :return:
    '''
    return f'<s>{text}</s>'


def italic_text(text: str) -> str:
    '''
    Курсивный текст
    :param text:
    :return:
    '''
    return f'<i>{text}</i>'


def code_text(text):
    '''
    Моноширнный
    :param text:
    :return:
    '''
    return f'<code>{text}</code>'
