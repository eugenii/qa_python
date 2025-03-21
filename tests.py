import pytest

from main import BooksCollector

class TestBooksCollector:

    # initialization
    def test_init(self, collector):
        collector.__init__()

        assert collector.books_genre == {}
        assert collector.favorites == []
        assert collector.genre == ['Фантастика', 'Ужасы', 'Детективы', 'Мультфильмы', 'Комедии']
        assert collector.genre_age_rating == ['Ужасы', 'Детективы']
    
    # Add book - amount, length, unique book: 2 tests
    def test_add_new_book_added_book_has_no_genre(self, book_to_coll):

        assert book_to_coll.books_genre['Гордость и предубеждение и зомби'] == ''

    @pytest.mark.parametrize(
            'books, res, comm',
            [
                [('Гордость и предубеждение и зомби', 'Что делать, если ваш кот хочет вас убить'), 2, ''],
                [('Что делать, если ваш кот хочет вас убить. (не пройдёт!)', ), 0, 'Too long']
            ]
    )
    def test_add_new_book_add_two_books_and_long_title(self, collector, books, res, comm):
        for book in books:
            collector.add_new_book(book)

        assert len(collector.books_genre) == res, comm

    def test_add_new_book_each_book_only_once_(self, book_to_coll):
        book_to_coll.add_new_book('Гордость и предубеждение и зомби')
        book_id_first = id(book_to_coll.books_genre['Гордость и предубеждение и зомби'])
        book_to_coll.add_new_book('Гордость и предубеждение и зомби')
        book_id_second = id(book_to_coll.books_genre['Гордость и предубеждение и зомби'])

        assert book_id_first == book_id_second

    # Set genre of book: 2 tests
    def test_set_book_genre_not_existed_book_not_setted(self, collector):
        collector.set_book_genre('Гордость и предубеждение и зомби', 'Ужасы')

        assert collector.books_genre.get('Гордость и предубеждение и зомби', None) == None
    
    @pytest.mark.parametrize(
            'book, genre, result, comm',
            [
                ['Гордость и предубеждение и зомби', 'Ужасы', 'Ужасы', 'check genre'],
                ['Гордость и предубеждение и зомби', 'trash', '', 'wrong genre'],
            ]
    )
    def test_set_book_genre_check_genre_n_genre_not_exists(self, collector, book, genre, result, comm):
        collector.add_new_book(book)
        collector.set_book_genre(book, genre)

        assert collector.books_genre[book] == result, comm

    # Getting genre of book: 1 test
    def test_get_book_genre_book_exist_return_genre(self, book_to_coll):
        book_to_coll.set_book_genre('Гордость и предубеждение и зомби', 'Ужасы')
        book_genre = book_to_coll.get_book_genre('Гордость и предубеждение и зомби')
        assert book_genre == 'Ужасы'

    # Get list of books with specific genres: 2 tests 
    @pytest.mark.parametrize(
            'book, genre, result',
            [
                ['Гордость и предубеждение и зомби', 'Ужасы', ['Гордость и предубеждение и зомби']],
                ['Гордость и предубеждение и зомби', 'Bla-bla', []],
                ['', '', []]
            ]
    )  
    def test_get_books_with_specific_genre_exist_return_list(self, collector, book, genre, result):
        collector.add_new_book(book)
        collector.set_book_genre(book, genre)
        genre_fiction = result
        result = collector.get_books_with_specific_genre(genre)

        assert result == genre_fiction

    # Get full object.
    def test_get_books_genre_all_positions_return_full(self, book_to_coll):
        book_to_coll.set_book_genre('Гордость и предубеждение и зомби','Ужасы')

        assert book_to_coll.get_books_genre() == {'Гордость и предубеждение и зомби': 'Ужасы'}

    # Getting books for children: 3 tests.
    @pytest.mark.parametrize(
            'book, result',
            [
                [[('Незнайка на Луне','Мультфильмы')], ['Незнайка на Луне']],
                [[('Незнайка на Луне','Мультфильмы'), ('Гордость и предубеждение и зомби','Ужасы')], ['Незнайка на Луне']],
                [[('Незнайка на Луне','Мультфильмы'), ('Просто зомби','strange')], ['Незнайка на Луне']],
            ]
    )
    def test_get_books_for_children_right_collection_returns_list(self, collector, book, result):
        for item, genre in book:
            collector.add_new_book(item)
            collector.set_book_genre(item, genre)

        assert collector.get_books_for_children() == result

    # Adding book to favorites.
    @pytest.mark.parametrize(
            'books, result, comm',
            [
                [('Нечто', 'Нечто'), 1, f'Добавление не прошло'],
                [('Нечто', 'Незнайка на Луне'), 0, f'Добавление несуществующей книги'],
                [('Нечто', 'Гордость и предубеждение и зомби'), 0, f'Добавление уже присутствующей книги'],
            ]
    )
    def test_add_book_in_favorites_returns_delta_length(self, collector, books, result, comm):
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_book_in_favorites('Гордость и предубеждение и зомби')
        pre_length = len(collector.favorites)
        collector.add_new_book(books[0])
        collector.add_book_in_favorites(books[1])
        post_length = len(collector.favorites)

        assert post_length - pre_length == result, comm
    
    # Deleting book from favorites.
    @pytest.mark.parametrize(
        'books, result, comm',
            [
                [('Нечто', 'Нечто'), -1, 'Удаление существующей книги'],  # positive
                [('Нечто', 'Нечто2'), 0, 'Удаление несущесвтующей книги'],  # no book in favorite
            ]
    )
    def test_delete_book_from_favorites_if_no_book_lenght_the_same(self, collector, books, result, comm):
        collector.add_new_book(books[0])
        collector.add_book_in_favorites(books[1])
        pre_length = len(collector.favorites)
        collector.delete_book_from_favorites(books[1])
        post_length = len(collector.favorites)

        assert post_length - pre_length == result

    # Gettin favorites list.
    def test_get_list_of_favorites_books_returns_right_list(self, book_to_coll):
        book_to_coll.add_new_book('Гордость и предубеждение и зомби')
        book_to_coll.add_book_in_favorites('Гордость и предубеждение и зомби')
        result = book_to_coll.get_list_of_favorites_books()
        must_be = ['Гордость и предубеждение и зомби']

        assert result == must_be

