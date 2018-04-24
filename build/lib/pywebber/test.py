import unittest
import os
import shutil

from .ripper import Ripper

class TestRipper(unittest.TestCase):
    def setUp(self):
        self.url = "http://python.org"
        self.page = Ripper(self.url)

    def test_class_string_representation(self):
        self.assertEqual(self.page.__str__(), "Rip: {}".format(self.url))

    def test_words_is_not_empty(self):
        self.assertTrue(list(self.page.words()))

    def test_links_is_not_empty(self):
        self.assertTrue(list(self.page.links()))

    def test_file_created_upon_object_creation(self):
        obj_path = self.page.page_save_path()
        assert(obj_path)

    # def test_reads_from_source_when_refresh_is_true(self):
    #     self.page.refresh = True
    #     self.assertTrue(self.page.from_source)

    def test_reading_from_for_old_link(self):
        self.assertFalse(self.page.from_source)

    def test_reading_from_source_for_new_link(self):
        page = Ripper("https://google.com")
        self.assertTrue(page.from_source)
        shutil.rmtree(os.path.dirname(page.page_save_path()))

