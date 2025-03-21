import pytest
from main import BooksCollector

@pytest.fixture
def collector():
    collector = BooksCollector()
    return collector

@pytest.fixture
def book_to_coll(collector):
    collector.add_new_book('Гордость и предубеждение и зомби')
    return collector
