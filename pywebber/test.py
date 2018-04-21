import unittest
import os
import shutil

from .ripper import Ripper

class TestRipper(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.url = "http://python.org"
        cls.page = Ripper(cls.url)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(os.path.dirname(cls.page.page_save_path()))

    def test_class_string_representation(self):
        self.assertEqual(self.page.__str__(), "Rip: {}".format(self.url))

    def test_words_is_not_empty(self):
        self.assertTrue(list(self.page.words()))

    def test_links_is_not_empty(self):
        self.assertTrue(list(self.page.links()))

    def test_file_created_upon_object_creation(self):
        obj_path = self.page.page_save_path()
        assert(obj_path)
        
    def test_reading_from_file_when_link_is_same(self):
        page = Ripper("http://python.org")
        self.assertFalse(page.from_source)

    def test_reads_from_source_when_refresh_is_true(self):
        page = Ripper("http://python.org", refresh=True)
        self.assertTrue(page.from_source)

    def test_reading_from_source_for_new_link(self):
        page = Ripper("https://google.com")
        self.assertTrue(page.from_source)
        shutil.rmtree(os.path.dirname(page.page_save_path()))

