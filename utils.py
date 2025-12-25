# utils.py
import re


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
    Проверяет, что строка имеет формат YYYY-MM-DD.

    Примеры:
        validate_date("2025-12-25") → True
        validate_date("25-12-2025") → False
    """
    if not date_str or not date_str.strip():
        return True  # дата может быть не указана
    return bool(re.fullmatch(r'^\d{4}-\d{2}-\d{2}$', date_str.strip()))


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