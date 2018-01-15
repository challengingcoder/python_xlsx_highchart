import unittest
from .excel_parser_test import ExcelParserTestCase
from .ui_test import UiTestCase


def make_suite():
    test_excel_parser = unittest.TestLoader().loadTestsFromTestCase(ExcelParserTestCase)
    test_ui = unittest.TestLoader().loadTestsFromTestCase(UiTestCase)
    suite = unittest.TestSuite([test_excel_parser, test_ui])
    return suite


def do_tests():
    runner = unittest.TextTestRunner()
    test_suite = make_suite()
    runner.run(test_suite)
