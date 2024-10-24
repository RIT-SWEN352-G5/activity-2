import unittest
from unittest.mock import Mock
from library import library_db_interface
import os

def make_mock_patron(mock_name: str = "mock_patron", f_name: str = "first", l_name: str = "last", age: int = 1, id: int = 1, borrowed: list = []):
    mock_patron = Mock(name=mock_name)
    mock_patron.get_fname = Mock(name="mockfn_get_fname", return_value=f_name)
    mock_patron.get_lname = Mock(name="mockfn_get_lname", return_value=l_name)
    mock_patron.get_age = Mock(name="mockfn_get_age", return_value=age)
    mock_patron.get_memberID = Mock(name="mockfn_get_memberID", return_value=id)
    mock_patron.get_borrowed_books = Mock(name="mockfn_get_borrowed", return_value=borrowed)

    return mock_patron

class TestLibrary_DB(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Backs up the database before clearing it for testing"""
        with open('db.json', 'r') as db_file, open('_db_backup.json', 'w') as backup:
            db = db_file.read()
            # print(db)
            backup.write(db)
        with open('db.json', 'w') as db_file:
            db_file.write('{"_default": {}}')

    @classmethod
    def tearDownClass(cls) -> None:
        """Restores the database from the backup created at setup"""
        with open('db.json', 'w') as db_file, open('_db_backup.json', 'r') as backup:
            bk = backup.read()
            # print(bk)
            db_file.write(bk)
        os.remove('_db_backup.json')

    def setUp(self):
        with open('db.json', 'w') as db_file:
            db_file.write('{"_default": {"1": {"fname": "f_existing", "lname": "l_existing", "age": 1, "memberID": 1, "borrowed_books": ["book"]}}}')
        self.dbi = library_db_interface.Library_DB()

    def tearDown(self):
        self.dbi.close_db()
        return super().tearDown()

    def test_insert_patron(self):
        mock_patron = make_mock_patron(age=20, id=2, borrowed=["book2"])

        data_id = self.dbi.insert_patron(mock_patron)
        self.assertEqual(2, data_id)

        with open('db.json', 'r') as db_file:
            data = db_file.read()
            self.assertTrue('"1": {"fname": "f_existing", "lname": "l_existing", "age": 1, "memberID": 1, "borrowed_books": ["book"]}' in data)
            self.assertTrue('"2": {"fname": "first", "lname": "last", "age": 20, "memberID": 2, "borrowed_books": ["book2"]}' in data)

    def test_insert_nothing(self):
        result = self.dbi.insert_patron(None)
        self.assertIsNone(result)

    def test_insert_existing(self):
        data_old = None
        with open("db.json", "r") as db_file:
            data_old = db_file.read()

        mock_patron = make_mock_patron(id=1)
        result = self.dbi.insert_patron(mock_patron)
        self.assertIsNone(result)

        with open('db.json', 'r') as db_file:
            data = db_file.read()
            self.assertEqual(data_old, data)

    def test_get_patron_count(self):
        self.assertEqual(1, self.dbi.get_patron_count())

    def test_get_all_patrons(self):
        all_patrons = self.dbi.get_all_patrons()
        self.assertEqual(1, len(all_patrons))
        self.assertEqual({
            'fname': 'f_existing',
            'lname': 'l_existing',
            'age': 1,
            'memberID': 1,
            'borrowed_books': ['book']
        }, all_patrons[0])

    def test_update_patron(self):
        mock_patron = make_mock_patron(f_name="f_existing", l_name="l_existing", id=1, age=20, borrowed=["book"])

        self.dbi.update_patron(mock_patron)

        with open('db.json', 'r') as db_file:
            data = db_file.read()
            self.assertTrue('"age": 20, "memberID": 1' in data)
            self.assertFalse('"age": 1' in data)

    def test_update_nothing(self):
        data_old = None
        with open("db.json", "r") as db_file:
            data_old = db_file.read()

        self.dbi.update_patron(None)

        with open("db.json", "r") as db_file:
            data = db_file.read()
            self.assertEqual(data_old, data)

    def test_retrieve_patron(self):
        patron = self.dbi.retrieve_patron(1)
        self.assertEqual("f_existing", patron.fname)
        self.assertEqual("l_existing", patron.lname)
        self.assertEqual(1, patron.age)
        self.assertEqual(1, patron.memberID)

    def test_close_db(self):
        self.assertTrue(self.dbi.db._opened)
        self.dbi.close_db()
        self.assertFalse(self.dbi.db._opened)

    def test_convert_patron_to_db_format(self):
        mock_patron = make_mock_patron(age=20, borrowed=["book"])

        converted = self.dbi.convert_patron_to_db_format(mock_patron)
        self.assertEqual({
            'fname': 'first',
            'lname': 'last',
            'age': 20,
            'memberID': 1,
            'borrowed_books': ['book']
        }, converted)
