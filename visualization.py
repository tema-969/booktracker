# visualization.py
import matplotlib.pyplot as plt
from analysis import analyze_reading_stats
from models import Book
from typing import List

plt.rcParams['font.size'] = 10
plt.rcParams['figure.figsize'] = (12, 8)


def plot_reading_stats(books: List[Book]):
    """
    Строит три графика на основе данных о книгах:
    1. Топ-5 жанров (круговая диаграмма)
    2. Количество прочитанных книг по годам (столбчатая)
    3. Распределение по статусам (столбчатая)

    Графики отображаются в одном окне (3 подграфика).
    """
    if not books:
        plt.figure()
        plt.text(0.5, 0.5, "Нет данных для визуализации", ha='center', va='center', fontsize=14)
        plt.axis('off')
        plt.show()
        return

    stats = analyze_reading_stats(books)

    # Создаём фигуру с 3 подграфиками
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    fig.suptitle("Статистика чтения", fontsize=16, fontweight='bold')

    # 1. Топ-5 жанров — круговая диаграмма
    ax1 = axes[0]
    top_genres = stats["top_genres"]
    if top_genres:
        labels = list(top_genres.keys())
        sizes = list(top_genres.values())
        wedges, texts, autotexts = ax1.pie(
            sizes, labels=labels, autopct='%1.1f%%', startangle=90
        )
        ax1.set_title("Топ-5 жанров (прочитано)")
    else:
        ax1.text(0.5, 0.5, "Нет данных", ha='center', va='center')
        ax1.set_title("Топ-5 жанров (прочитано)")

    # 2. Книги по годам — столбчатая диаграмма
    ax2 = axes[1]
    books_by_year = stats["books_by_year"]
    if books_by_year:
        years = list(books_by_year.keys())
        counts = list(books_by_year.values())
        ax2.bar(years, counts, color='skyblue', edgecolor='navy')
        ax2.set_title("Прочитано книг по годам")
        ax2.set_xlabel("Год")
        ax2.set_ylabel("Количество книг")
        ax2.set_xticks(years)
    else:
        ax2.text(0.5, 0.5, "Нет данных", ha='center', va='center')
        ax2.set_title("Прочитано книг по годам")

    # 3. Статусы — столбчатая диаграмма
    ax3 = axes[2]
    status_counts = {
        "Прочитано": stats["finished_books_count"],
        "Читаю": stats["reading_books_count"],
        "В планах / Отложено": stats["total_books"] - stats["finished_books_count"] - stats["reading_books_count"]
    }
    statuses = list(status_counts.keys())
    counts = list(status_counts.values())
    colors = ['green', 'orange', 'gray']
    ax3.bar(statuses, counts, color=colors, edgecolor='black')
    ax3.set_title("Распределение по статусам")
    ax3.set_ylabel("Количество книг")
    ax3.set_ylim(0, max(counts) + 1 if max(counts) > 0 else 1)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()