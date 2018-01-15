import os
import unittest
from random import randint

from selenium import webdriver
from selenium.webdriver.support.ui import Select

this_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

test_xls_file = os.path.realpath(os.path.join(this_dir, 'xls', '3.xlsx'))


class UiTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()
        cls.base_url = 'http://127.0.0.1:5000'
        cls.slide_count = 0

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_00_home(self):
        self.driver.get(self.base_url)

    def test_02_upload(self):
        # Uplad xlsx file
        element = self.driver.find_element_by_css_selector('#the-file')
        element.send_keys(test_xls_file)
        self.driver.implicitly_wait(5)
        slide_items = self.driver.find_elements_by_css_selector('.slide-item')
        self.assertEqual(len(slide_items), 21)
        UiTestCase.slide_count = len(slide_items)

    def test_03_browse_pages(self):
        # Navigate through pages
        for i in range(self.slide_count):
            u = '{}/builder/{}'.format(self.base_url, i)
            self.driver.get(u)
            self.driver.implicitly_wait(1)

    def test_04_browse_pages_and_make_settings(self):
        # Navigate through pages and make random settings
        # Do 2 times
        for i in range(2):
            for i in range(self.slide_count):
                u = '{}/builder/{}'.format(self.base_url, i)
                self.driver.get(u)

                cross_break_select_elem = self.driver.find_element_by_css_selector('select[name="cross-break"]')
                cross_break_options = cross_break_select_elem.find_elements_by_tag_name('option')
                cross_break_select = Select(cross_break_select_elem)
                index = randint(0, (len(cross_break_options) - 1))
                cross_break_select.select_by_index(index)

                self.driver.implicitly_wait(1)

                chart_type_select_elem = self.driver.find_element_by_css_selector('select[name="chart-type"]')
                chart_type_options = chart_type_select_elem.find_elements_by_tag_name('option')
                chart_type_select = Select(chart_type_select_elem)
                index = randint(0, (len(chart_type_options) - 1))
                chart_type_select.select_by_index(index)

                self.driver.implicitly_wait(1)

                series_by_select_elem = self.driver.find_element_by_css_selector('select[name="series-by"]')
                series_by_options = series_by_select_elem.find_elements_by_tag_name('option')
                series_by_select = Select(series_by_select_elem)
                index = randint(0, (len(series_by_options) - 1))
                series_by_select.select_by_index(index)

                self.driver.implicitly_wait(1)

    def test_05_click_download_button(self):
        # Download file dialog should be shown
        self.driver.find_element_by_css_selector('.btn-download').click()


if __name__ == '__main__':
    unittest.main()
