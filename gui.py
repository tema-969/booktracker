# gui.py
import tkinter as tk
from tkinter import ttk, messagebox
import asyncio
from models import Book
from storage import load_books, save_books
from api_client import fetch_book_by_isbn
from visualization import plot_reading_stats
from utils import validate_isbn, validate_date, validate_pages, validate_not_empty


class BookTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BookTracker — Трекер книг")
        self.root.geometry("900x600")

        # Загружаем книги
        self.books = load_books()

        # Создаём виджеты
        self.create_widgets()
        self.refresh_book_list()

    def create_widgets(self):
        # === Верхняя панель: форма добавления ===
        form_frame = ttk.LabelFrame(self.root, text="Добавить книгу")
        form_frame.pack(fill="x", padx=10, pady=5)

        # Поля ввода
        ttk.Label(form_frame, text="ISBN:").grid(row=0, column=0, sticky="w", padx=5, pady=3)
        self.isbn_var = tk.StringVar()
        isbn_entry = ttk.Entry(form_frame, textvariable=self.isbn_var, width=20)
        isbn_entry.grid(row=0, column=1, padx=5, pady=3)

        ttk.Button(form_frame, text="Поиск по ISBN", command=self.on_fetch_isbn).grid(row=0, column=2, padx=5, pady=3)

        ttk.Label(form_frame, text="Название:").grid(row=1, column=0, sticky="w", padx=5, pady=3)
        self.title_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.title_var, width=50).grid(row=1, column=1, columnspan=2, padx=5, pady=3)

        ttk.Label(form_frame, text="Автор:").grid(row=2, column=0, sticky="w", padx=5, pady=3)
        self.author_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.author_var, width=50).grid(row=2, column=1, columnspan=2, padx=5, pady=3)

        ttk.Label(form_frame, text="Жанр:").grid(row=3, column=0, sticky="w", padx=5, pady=3)
        self.genre_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.genre_var, width=50).grid(row=3, column=1, columnspan=2, padx=5, pady=3)

        ttk.Label(form_frame, text="Страницы:").grid(row=4, column=0, sticky="w", padx=5, pady=3)
        self.pages_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.pages_var, width=10).grid(row=4, column=1, sticky="w", padx=5, pady=3)

        ttk.Label(form_frame, text="Статус:").grid(row=5, column=0, sticky="w", padx=5, pady=3)
        self.status_var = tk.StringVar(value="planned")
        status_frame = ttk.Frame(form_frame)
        status_frame.grid(row=5, column=1, sticky="w", padx=5, pady=3)
        ttk.Radiobutton(status_frame, text="В планах", variable=self.status_var, value="planned").pack(side="left")
        ttk.Radiobutton(status_frame, text="Читаю", variable=self.status_var, value="reading").pack(side="left", padx=5)
        ttk.Radiobutton(status_frame, text="Прочитано", variable=self.status_var, value="finished").pack(side="left", padx=5)

        ttk.Button(form_frame, text="Добавить книгу", command=self.on_add_book).grid(row=6, column=0, columnspan=3, pady=10)

        # === Кнопка статистики ===
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill="x", padx=10, pady=5)
        ttk.Button(btn_frame, text="Показать статистику", command=self.on_show_stats).pack(side="left")

        # === Таблица книг ===
        tree_frame = ttk.Frame(self.root)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("title", "author", "genre", "status")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        self.tree.heading("title", text="Название")
        self.tree.heading("author", text="Автор")
        self.tree.heading("genre", text="Жанр")
        self.tree.heading("status", text="Статус")
        self.tree.column("title", width=250)
        self.tree.column("author", width=150)
        self.tree.column("genre", width=150)
        self.tree.column("status", width=100)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

    def refresh_book_list(self):
        """Обновляет список книг в Treeview."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        for book in self.books:
            status_labels = {
                "planned": "В планах",
                "reading": "Читаю",
                "finished": "Прочитано"
            }
            self.tree.insert("", "end", values=(
                book.title,
                book.author,
                book.genre,
                status_labels.get(book.status, book.status)
            ))

    def on_fetch_isbn(self):
        """Обработчик кнопки 'Поиск по ISBN'."""
        isbn = self.isbn_var.get().strip()
        if not validate_isbn(isbn):
            messagebox.showerror("Ошибка", "Неверный формат ISBN!")
            return

        # Запускаем асинхронную функцию
        try:
            book_data = asyncio.run(fetch_book_by_isbn(isbn))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось получить данные: {e}")
            return

        if not book_data:
            messagebox.showwarning("Не найдено", "Книга с таким ISBN не найдена.")
            return

        # Заполняем поля
        self.title_var.set(book_data["title"])
        self.author_var.set(book_data["author"])
        self.genre_var.set(book_data["genre"])
        if book_data["pages"]:
            self.pages_var.set(str(book_data["pages"]))

    def on_add_book(self):
        """Добавляет новую книгу."""
        # Валидация
        if not validate_not_empty(self.title_var.get()):
            messagebox.showerror("Ошибка", "Укажите название книги.")
            return
        if not validate_not_empty(self.author_var.get()):
            messagebox.showerror("Ошибка", "Укажите автора.")
            return
        if not validate_not_empty(self.genre_var.get()):
            messagebox.showerror("Ошибка", "Укажите жанр.")
            return
        if self.pages_var.get() and not validate_pages(self.pages_var.get()):
            messagebox.showerror("Ошибка", "Количество страниц должно быть положительным числом.")
            return

        # Создаём объект
        book = Book(
            title=self.title_var.get(),
            author=self.author_var.get(),
            genre=self.genre_var.get(),
            isbn=self.isbn_var.get() or None,
            status=self.status_var.get(),
            pages=int(self.pages_var.get()) if self.pages_var.get() else None
        )

        self.books.append(book)
        save_books(self.books)
        self.refresh_book_list()

        # Сбрасываем форму
        self.isbn_var.set("")
        self.title_var.set("")
        self.author_var.set("")
        self.genre_var.set("")
        self.pages_var.set("")
        self.status_var.set("planned")

        messagebox.showinfo("Успех", "Книга добавлена!")

    def on_show_stats(self):
        """Показывает графики статистики."""
        plot_reading_stats(self.books)


def run_app():
    root = tk.Tk()
    app = BookTrackerApp(root)
    root.mainloop()