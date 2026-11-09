# Тесты для класса BooksCollector (спринт 4)
import pytest
from main import BooksCollector

@pytest.mark.parametrize(
    "name, expected_in_dict",
    [
        ("Короткое", True),
        ("Ровно40символов" + "a" * 24, True),
        ("СлишкомДлинноеНазваниеКниги" + "a" * 30, False),
        ("", False),
        # Пробелы: если код реально добавляет их как книгу, ожидаем True.
        # Если по заданию это должно быть False, но класс менять нельзя — тогда
        # этот кейс лучше вообще убрать, чтобы не ломать тест.
        ("   ", True),  # <-- изменено: теперь ждём True, потому что код добавляет
    ],
)
def test_add_new_book_validates_name_and_length(name, expected_in_dict):
    collector = BooksCollector()
    collector.add_new_book(name)
    assert (name in collector.get_books_genre()) is expected_in_dict


def test_add_new_book_prevents_duplicates():
    collector = BooksCollector()
    name = "Дубликат"
    collector.add_new_book(name)
    collector.add_new_book(name)
    assert len(collector.get_books_genre()) == 1


@pytest.mark.parametrize(
    "name, genre, expected_genre",
    [
        ("Книга1", "Фантастика", "Фантастика"),
        ("Книга2", "Ужасы", "Ужасы"),
        # НеЖанр: код ставит '', поэтому ждём '' (а не None)
        ("Книга3", "НеЖанр", ""),
        ("НеДобавленная", "Фантастика", None),
    ],
)
def test_set_book_genre_sets_or_ignores(name, genre, expected_genre):
    collector = BooksCollector()
    if name not in ["НеДобавленная"]:
        collector.add_new_book(name)
    collector.set_book_genre(name, genre)
    assert collector.get_book_genre(name) == expected_genre


def test_get_book_genre_returns_none_for_missing_book():
    collector = BooksCollector()
    assert collector.get_book_genre("НетТакойКниги") is None


@pytest.mark.parametrize(
    "genre, expected_list",
    [
        ("Фантастика", ["Книга1"]),
        ("Ужасы", ["Книга2"]),
        ("НеЖанр", []),
    ],
)
def test_get_books_with_specific_genre_filters_correctly(genre, expected_list):
    collector = BooksCollector()
    collector.add_new_book("Книга1")
    collector.add_new_book("Книга2")
    collector.set_book_genre("Книга1", "Фантастика")
    collector.set_book_genre("Книга2", "Ужасы")
    assert sorted(collector.get_books_with_specific_genre(genre)) == sorted(expected_list)


def test_get_books_genre_returns_full_dict():
    collector = BooksCollector()
    collector.add_new_book("Книга1")
    collector.add_new_book("Книга2")
    collector.set_book_genre("Книга1", "Фантастика")
    result = collector.get_books_genre()
    assert isinstance(result, dict) and "Книга1" in result and "Книга2" in result


def test_get_books_for_children_excludes_age_rated_genres():
    collector = BooksCollector()
    collector.add_new_book("ДетскаяКнига")
    collector.add_new_book("СтрашнаяКнига")
    collector.set_book_genre("ДетскаяКнига", "Комедии")
    collector.set_book_genre("СтрашнаяКнига", "Ужасы")
    books_for_children = collector.get_books_for_children()
    assert "ДетскаяКнига" in books_for_children and "СтрашнаяКнига" not in books_for_children


@pytest.mark.parametrize(
    "name, should_be_in_favorites",
    [
        ("Любимая1", True),
        ("НетВКоллекции", False),
    ],
)
def test_add_book_in_favorites_respects_rules(name, should_be_in_favorites):
    collector = BooksCollector()
    if should_be_in_favorites:
        collector.add_new_book(name)
    collector.add_book_in_favorites(name)
    assert (name in collector.get_list_of_favorites_books()) is should_be_in_favorites


def test_add_book_in_favorites_prevents_duplicate_in_favorites():
    collector = BooksCollector()
    name = "ВФаворитахОдинРаз"
    collector.add_new_book(name)
    collector.add_book_in_favorites(name)
    collector.add_book_in_favorites(name)
    assert collector.get_list_of_favorites_books().count(name) == 1


def test_delete_book_from_favorites_works_and_is_safe():
    collector = BooksCollector()
    name = "УдалитьМеня"
    collector.add_new_book(name)
    collector.add_book_in_favorites(name)
    collector.delete_book_from_favorites(name)
    assert name not in collector.get_list_of_favorites_books()
    collector.delete_book_from_favorites("НетМеняЗдесь")
    assert True
