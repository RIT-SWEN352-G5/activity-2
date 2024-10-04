import unittest
from unittest.mock import Mock
from library import library, library_db_interface
import json


class TestLibrary(unittest.TestCase):

    def setUp(self):
        self.lib = library.Library()
        self.lib.api = Mock(name="mock_api")
        
        self.lib.db = Mock(name = "mock_db")
        
        with open('tests_data/ebooks.txt', 'r') as f:
            self.books_data = json.loads(f.read())

    def test_is_ebook_true(self):
        self.lib.api.get_ebooks = Mock(return_value = self.books_data)
        self.assertTrue(self.lib.is_ebook('learning python'))

    def test_is_ebook_false(self):
        self.lib.api.get_ebooks = Mock(return_value = self.books_data)
        self.assertFalse(self.lib.is_ebook(' '))

    def test_get_ebooks_count(self):
        self.lib.api.get_ebooks = Mock(return_value=self.books_data)
        self.assertEqual(self.lib.get_ebooks_count("learning python"), 8)
        
    ############################################################################
    #################################  AUTHORS  ###############################
    ############################################################################

    def test_is_book_by_author_true(self):
        self.lib.api.get_ebooks = Mock(return_value = self.books_data)

        self.lib.api.books_by_author = Mock("books_by_author", return_value=["the amazing digital circus"])

        self.assertFalse(self.lib.is_book_by_author('the amazing digital circus', 'Wei-Meng Lee'))
    
    def test_is_book_by_author_false(self):
        self.lib.api.get_ebooks = Mock(return_value = self.books_data)

        self.lib.api.books_by_author = Mock("books_by_author", return_value=[])

        self.assertFalse(self.lib.is_book_by_author(' ', 'Wei-Meng Lee'))
            
    def test_get_language_for_book(self):  
        
        self.lib.api.get_book_info = Mock(name = 'AHHHHHHHHHHHHHHHHHHHHHHHH', return_value=[{'language': {'hin'}}])

        self.assertEqual(self.lib.get_languages_for_book('learning python'), {'hin'})
        
    def test_borrow_book(self):

        testPatron = Mock(name = "testPatron")

        testPatron.add_borrowed_book = Mock(name = "mock_borrowedBook")
        testPatron.fname = "SSSSSANAS"
        self.lib.db.update_patron = Mock(name = "update patron mock")

        self.lib.borrow_book('learning python', testPatron)

        testPatron.add_borrowed_book.assert_called()
        self.lib.db.update_patron.assert_called()

    def test_return_borrowed_book(self):
        testPatron = Mock(name = "testPatron")

        testPatron.add_borrowed_book = Mock(name = "mock_borrowedBook")
        testPatron.return_borrowed_book = Mock(name = 'mock return book')
        testPatron.fname = "SSSSSANAS"
        self.lib.db.update_patron = Mock(name = "update patron mock")

        self.lib.borrow_book('learning python', testPatron)
        self.lib.return_borrowed_book('learning python', testPatron)

        testPatron.return_borrowed_book.assert_called()
        self.lib.db.update_patron.assert_called()

    # def test_is_book_borrowed(self):

    # def test_register_patron(self):
        
    # def test_is_patron_registered_true(self):

    # def test_is_patron_registered_false(self):