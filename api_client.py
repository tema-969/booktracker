# api_client.py
import aiohttp
import asyncio
from typing import Optional, Dict, Any

GOOGLE_BOOKS_URL = "https://www.googleapis.com/books/v1/volumes"

async def fetch_book_by_isbn(isbn: str) -> Optional[Dict[str, Any]]:
    """
    Получает данные книги по ISBN через Google Books API (бесплатно, без ключа).
    """
    if not isbn:
        return None

    clean_isbn = isbn.replace("-", "").replace(" ", "")
    params = {"q": f"isbn:{clean_isbn}"}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(GOOGLE_BOOKS_URL, params=params, timeout=10) as response:
                if response.status != 200:
                    return None
                data = await response.json()

                items = data.get("items")
                if not items:
                    return None

                volume = items[0]["volumeInfo"]
                title = volume.get("title", "")
                authors = volume.get("authors", ["Unknown"])
                author = ", ".join(authors)
                pages = volume.get("pageCount")
                genre = ", ".join(volume.get("categories", ["Unknown"])) if volume.get("categories") else "Unknown"

                return {
                    "title": title,
                    "author": author,
                    "genre": genre,
                    "pages": pages
                }

    except asyncio.TimeoutError:
        print("⚠️ Тайм-аут при запросе к Google Books API")
        return None
    except Exception as e:
        print(f"⚠️ Ошибка в API-клиенте: {e}")
        return None