# tests/test_models.py
import unittest
from models import Book


class TestBook(unittest.TestCase):

    def test_book_creation(self):
        book = Book(
            title="1984",
            author="George Orwell",
            genre="Dystopia",
            isbn="9780451524935",
            status="finished",
            start_date="2024-01-10",
            end_date="2024-01-25",
            pages=328
        )
        self.assertEqual(book.title, "1984")
        self.assertEqual(book.author, "George Orwell")
        self.assertEqual(book.status, "finished")
        self.assertEqual(book.pages, 328)

    def test_book_to_dict_and_back(self):
        original = Book(
            title="Dune",
            author="Frank Herbert",
            genre="Sci-Fi",
            status="planned"
        )
        data = original.to_dict()
        restored = Book.from_dict(data)

        self.assertEqual(original.title, restored.title)
        self.assertEqual(original.author, restored.author)
        self.assertEqual(original.genre, restored.genre)
        self.assertEqual(original.status, restored.status)
        self.assertIsNone(restored.isbn)
        self.assertIsNone(restored.pages)

    def test_book_with_none_fields(self):
        book = Book("Test", "Author", "Genre")
        self.assertIsNone(book.isbn)
        self.assertIsNone(book.start_date)
        self.assertIsNone(book.pages)