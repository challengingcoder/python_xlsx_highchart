import unittest
from .excel_parser_test import ExcelParserTestCase


def make_suite():
    test_excel_parser = unittest.TestLoader().loadTestsFromTestCase(ExcelParserTestCase)
    suite = unittest.TestSuite([test_excel_parser])
    return suite


def do_tests():
    runner = unittest.TextTestRunner()
    test_suite = make_suite()
    runner.run(test_suite)
