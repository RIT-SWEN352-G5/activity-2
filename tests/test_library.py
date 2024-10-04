import unittest
from unittest.mock import Mock
from library import library
import json


class TestLibrary(unittest.TestCase):

    def setUp(self):
        self.lib = library.Library()

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
        # print(self.lib.api.get_book_info('learning python'))
        self.assertTrue(self.lib.is_book_by_author('Learning WatchKit programming', 'Wei-Meng Lee'))
    
    def test_is_book_by_author_false(self):
        self.lib.api.get_ebooks = Mock(return_value = self.books_data)
        # print(self.lib.api.books_by_author('Wei-Meng Lee'))

        self.assertFalse(self.lib.is_book_by_author(' ', 'Wei-Meng Lee'))
            
    def test_get_language_for_book(self):
        self.lib.api.get_ebooks = Mock(return_value=self.books_data)
        self.assertEqual(self.lib.get_languages_for_book('learning python'), {'hin', 'por', 'eng', 'ger'})
        

    # def test_register_patron(self):

    # def test_is_patron_registered_true(self):

    # def test_is_patron_registered_false(self):

    # def test_borrow_book(self):

    # def test_return_borrowed_book(self):

    # def test_is_book_borrowed(self):