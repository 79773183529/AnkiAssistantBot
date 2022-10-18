from typing import Union, Optional


# Принимает текст и разбивает его символом "\n" на строки длиной (по умолчанию) до 33 символов
def text_separator(text: str, lenght: int = 33, result_text: Optional[str] = None) -> str:
    if result_text is None:
        result_text = ''
    if len(text) <= lenght:
        result_text += text
        return result_text
    index = lenght
    for i in range(lenght):
        if text[i] == " ":
            index: int = i
    result_text += text[:index] + "\n"
    text = text[index + 1:]
    return text_separator(text=text, lenght=lenght, result_text=result_text)


# Принимает код и делит длинные строки символом \n
def code_separator(code: str, lenght: int = 41) -> str:
    code_list = code.split('\n')
    new_code_list = []
    for el in code_list:
        new_el = text_separator(text=el, lenght=lenght)
        new_code_list.append(new_el)
    return '\n'.join(new_code_list)


# Находить х от длины текста чтобы он распологался по центру
def center(head):
    long = len(head)
    if long > 25:
        raise ValueError('оглавление не может быть больше 25 букв')
    return (25 - long) * 10


# Находит Y для code от длины основного текста
def y_position(text, y_text=110):
    space_number = text.count('\n')
    return y_text + 40 + (30 * space_number)
