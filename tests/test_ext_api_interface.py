import unittest
from unittest.mock import Mock
from library import ext_api_interface
import json

class TestLibrary(unittest.TestCase):

    def setUp(self):
        self.maxDiff=None
        self.ext=ext_api_interface.Books_API()
        self.ext.api = Mock(name="mock_api")
        with open('tests_data/ext_api.txt', 'r') as f:
            self.mock_data = json.loads(f.read())
        f.close()
        with open('tests_data/books.txt', 'r') as f:
            self.books_by_author = f.read()
        f.close()
        with open('tests_data/book_info.txt', 'r') as f:
            self.book_info = f.read()
        f.close()
        with open('tests_data/ebooks.txt', 'r') as f:
            self.ebooks = f.read()
        f.close()
        

    def test_make_request_success(self):
        self.ext.api.make_request = Mock(return_value =self.mock_data )
        self.assertEqual(self.ext.make_request("http://openlibrary.org/search.json"), self.mock_data)

    def test_make_request_fail(self):
        self.ext.api.make_request = Mock(return_value =None)
        self.assertEqual(self.ext.make_request("http://GrunkleStunklewinstheFunkleBunkle"), None)

    def test_make_request_error(self):
        self.ext.api.make_request = Mock(return_value =None)
        self.assertEqual(self.ext.make_request("https://httpstat.us/400"), None)

    def test_book_is_available(self):
        self.ext.api.is_book_available = Mock(return_value =True )
        self.assertEqual(self.ext.is_book_available("learning python"),True)
    
    def test_book_is_not_available(self):
        self.ext.api.is_book_available = Mock(return_value =False )
        self.assertEqual(self.ext.is_book_available("Grunkle Stunkle Wins the Funkle Bunkle"),False)
    
    def test_get_books_by_author_invalid_author(self):
        self.ext.api.books_by_author = Mock(return_value =[] )
        self.assertEqual(self.ext.books_by_author("Grunkle Stunkle Wins the Funkle Bunkle"),[])

    def test_get_books_by_valid_author(self):
        self.ext.api.books_by_author = Mock(return_value =self.books_by_author)
        self.assertEqual(str(self.ext.books_by_author('George RR Martin')),self.books_by_author)
    
    def test_get_book_info_from_valid_book(self):
        self.ext.api.get_book_info = Mock(return_value =self.book_info)
        self.assertEqual(str(self.ext.get_book_info("Nathan Hale's Hazardous Tales: Major Impossible")),self.book_info)
    
    def test_get_book_info_from_invalid_book(self):
        self.ext.api.get_book_info = Mock(return_value =[])
        self.assertEqual(self.ext.get_book_info("Grunkle Stunkle Wins the Funkle Bunkle"),[])

    def test_get_ebooks_from_valid_title(self):
        self.ext.api.get_ebooks = Mock(return_value =self.ebooks)
        self.assertEqual(str(self.ext.get_ebooks("North-West Territories")),self.ebooks)
    
    def test_get_ebooks_from_invalid_title(self):
        self.ext.api.get_ebooks = Mock(return_value =[])
        self.assertEqual(self.ext.get_ebooks("Grunkle Stunkle Wins the Funkle Bunkle"),[])
    
    
    
    

    
        
    

    
    


    



    

    
  

        
    
