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

    def test_get_ebooks_count(self):
        self.lib.api.get_ebooks = Mock(return_value=self.books_data)
        
        self.assertEqual(self.lib.get_ebooks_count("Among us"), 18)

    ############################################################################
    #################################  AUTHORS  ###############################
    ############################################################################

    def test_get_ebook_author(self):
        self.lib.api.get_ebooks = Mock(return_value=self.books_data)


    def test_no_author(self):
            
    def test_get_language_for_book(self):

    def test_no_language_for_book(self)

    def test_invalid_language_for_book(self):

    def test_register_patron(self):

    def test_register_patron_doesnt_exist(self):

    def test_patron_registered(self):
    
    def test_book_borrowed(self):

    def test_book_not_exit_borrowed(self):

    def test_book_borrowed_patron_not_registered(self):

    def test_book_returned(self):

    def test_book_returned_book_not_exist(self):

    def test_is_book_borrowed(self):



    

