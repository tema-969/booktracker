import re
from datetime import datetime

def validate_isbn(isbn: str) -> bool:
    """
    Проверяет корректность ISBN-10 или ISBN-13.
    Допускает дефисы и пробелы (они удаляются перед проверкой).

    Примеры:
        validate_isbn("978-0-14-044926-6") → True
        validate_isbn("0140449266") → True
        validate_isbn("12345") → False
    """
    if not isbn or not isbn.strip():
        return True  # ISBN может быть не указан

    # Удаляем всё, кроме цифр и X/x (X допустим только в ISBN-10 на последнем месте)
    cleaned = re.sub(r'[^0-9Xx]', '', isbn.strip())

    # ISBN-10: 9 цифр + [0-9 или X/x]
    if len(cleaned) == 10:
        return bool(re.fullmatch(r'^[0-9]{9}[0-9Xx]$', cleaned))

    # ISBN-13: 13 цифр
    if len(cleaned) == 13:
        return bool(re.fullmatch(r'^[0-9]{13}$', cleaned))

    return False


def validate_date(date_str: str) -> bool:
    """
    Проверяет, что строка имеет формат YYYY-MM-DD и представляет собой корректную дату.
    """
    if not date_str or not date_str.strip():
        return True  # дата может быть не указана

    # Сначала проверяем формат через регулярное выражение
    if not re.fullmatch(r'^\d{4}-\d{2}-\d{2}$', date_str.strip()):
        return False

    # Затем проверяем, что это реальная дата
    try:
        datetime.strptime(date_str.strip(), "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validate_pages(pages_str: str) -> bool:
    """
    Проверяет, что строка — положительное целое число.
    """
    if not pages_str or not pages_str.strip():
        return True  # страницы могут быть не указаны
    return bool(re.fullmatch(r'^[1-9]\d*$', pages_str.strip()))


def validate_not_empty(text: str) -> bool:
    """
    Проверяет, что строка не пустая и не состоит только из пробелов.
    """
    return bool(text and text.strip())