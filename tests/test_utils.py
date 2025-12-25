# tests/test_utils.py
import unittest
from utils import validate_isbn, validate_date, validate_pages, validate_not_empty


class TestUtils(unittest.TestCase):

    def test_validate_isbn(self):
        # Корректные ISBN
        self.assertTrue(validate_isbn("978-0-14-044926-6"))
        self.assertTrue(validate_isbn("9780140449266"))
        self.assertTrue(validate_isbn("0140449266"))
        self.assertTrue(validate_isbn("0-14-044926-6"))
        self.assertTrue(validate_isbn(""))

        # Некорректные ISBN
        self.assertFalse(validate_isbn("12345"))
        self.assertFalse(validate_isbn("97801404492666"))  # 14 цифр
        self.assertFalse(validate_isbn("014044926"))        # 9 цифр
        self.assertFalse(validate_isbn("014044926Xx"))      # смешанный регистр и длина

    def test_validate_date(self):
        # Корректные даты
        self.assertTrue(validate_date("2025-12-25"))
        self.assertTrue(validate_date("2000-01-01"))
        self.assertTrue(validate_date(""))

        # Некорректные даты
        self.assertFalse(validate_date("25-12-2025"))
        self.assertFalse(validate_date("2025/12/25"))
        self.assertFalse(validate_date("2025-13-01"))  # неверный месяц — но валидация по формату, не по смыслу
        self.assertFalse(validate_date("2025-12-"))

    def test_validate_pages(self):
        # Корректные значения
        self.assertTrue(validate_pages("1"))
        self.assertTrue(validate_pages("999"))
        self.assertTrue(validate_pages(""))

        # Некорректные значения
        self.assertFalse(validate_pages("0"))
        self.assertFalse(validate_pages("-5"))
        self.assertFalse(validate_pages("abc"))
        self.assertFalse(validate_pages("12.5"))

    def test_validate_not_empty(self):
        self.assertTrue(validate_not_empty("Book"))
        self.assertTrue(validate_not_empty(" Author "))
        self.assertFalse(validate_not_empty(""))
        self.assertFalse(validate_not_empty("   "))