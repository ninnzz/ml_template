"""Tests for util functions"""
import unittest

from src.common.utils import *


class TestUtils(unittest.TestCase):
    """
    Test class.

    Attributes
    ----------
        unittest.TestCase (obj): unittest testcase class
    """

    def test_is_s3_file(self):
        """
        Checking of s3
        Returns
        -------

        """
        s3_url = "s3://bucket/folder/"
        non_s3_url = "/local/folder/some_file.jpg"

        self.assertTrue(is_s3_file(s3_url))
        self.assertFalse(is_s3_file(non_s3_url))
