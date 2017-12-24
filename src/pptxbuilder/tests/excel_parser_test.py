import os
import unittest

from pptxbuilder.excel_parser import (SectionCategory, Table, TableBundle,
                                      TableNameExistsError, TableSection,
                                      parse)


class ExcelParserTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cur_dir = os.path.abspath(
            os.path.dirname(os.path.realpath(__file__)))

    def test_00_test_oop(self):
        # xlsx_dir = os.path.join(self.cur_dir, 'xls', '1.xlsx')

        # Section 1
        sect1 = TableSection("T")

        # TableSection.name test
        self.assertEquals(sect1.name, "T")

        # category 1
        sect1_cat1 = SectionCategory("Total")

        # SectionCategory.values test
        self.assertEquals(len(sect1_cat1.values), 0)
        sect1_cat1.values = [17.5, 17.5, 17.5]
        self.assertEquals(len(sect1_cat1.values), 3)

        # SectionCategory.to_dict test
        self.assertIsInstance(sect1_cat1.to_dict(), dict)
        self.assertEquals(len(sect1_cat1.to_dict()['values']), 3)

        sect1.add_category(sect1_cat1)

        # TableSection.get_category_by_name test
        self.assertIsInstance(
            sect1.get_category_by_name("Total"), SectionCategory)
        self.assertEqual(sect1.get_category_by_name("Tota"), None)

        # ----------------------------------------------------- #

        # Section 2
        sect2 = TableSection("Gender")

        # category 1
        sect2_cat1 = SectionCategory("Male", [26.8, 26.8, 26.8])
        # category 2
        sect2_cat2 = SectionCategory("Female", [23.4, 23.4, 23.4])

        sect2.add_category(sect2_cat1)
        sect2.add_category(sect2_cat2)

        self.assertEquals(len(sect2.categories), 2)
        self.assertRaises(TableNameExistsError, sect2.add_category, sect2_cat1)
        self.assertRaisesRegex(
            TableNameExistsError, 'Category "*.*" exists in Section', sect2.add_category, sect2_cat1)

        # TableSection.to_dict test
        self.assertIsInstance(sect2.to_dict(), dict)
        self.assertEquals(len(sect2.to_dict()['categories']), 2)
        self.assertEquals(sect2.to_dict()['categories'][0]['name'], 'Male')
        self.assertEquals(sect2.to_dict()['categories'][1]['name'], 'Female')

        # ----------------------------------------------------- #

        # Table 1
        table1 = Table("Table 1", "How are you", ["good", "bad", "not bad"])

        # Table.name test
        self.assertEquals(table1.name, "Table 1")

        # Table.question test
        table1.question = 'How are you ?'
        self.assertEquals(table1.question, 'How are you ?')

        # Table.options test
        table1.options = ["good", "bad", "not bad", "feel lucky"]
        self.assertEquals(
            table1.options, ["good", "bad", "not bad", "feel lucky"])

        # Table.add_section test
        table1.add_section(sect1)
        table1.add_section(sect2)
        self.assertRaises(TableNameExistsError, table1.add_section, sect1)
        self.assertRaisesRegex(
            TableNameExistsError, 'Section "*.*" exists in Table', table1.add_section, sect1)

        # Table.sections test
        self.assertIsInstance(table1.sections, list)
        self.assertEquals(len(table1.sections), 2)

        # Table.get_section_by_name test
        self.assertIsInstance(
            table1.get_section_by_name("Gender"), TableSection)
        self.assertEquals(table1.get_section_by_name("Gende"), None)

        # Table.to_dict test
        self.assertIsInstance(table1.to_dict(), dict)
        self.assertEquals(len(table1.to_dict()['sections']), 2)

        # ----------------------------------------------------- #

        # Bundle
        bundle = TableBundle("Bundle")

        # TableBundle.name test
        self.assertEquals(bundle.name, "Bundle")

        # TableBundle.add_table test
        bundle.add_table(table1)
        self.assertRaises(TableNameExistsError, bundle.add_table, table1)
        self.assertRaisesRegex(
            TableNameExistsError, 'Table "*.*" exists in Bundle', bundle.add_table, table1)

        # TableBundle.tables test
        self.assertIsInstance(bundle.tables, list)
        self.assertEquals(len(bundle.tables), 1)

        # TableBundle.get_table_by_name test
        self.assertIsInstance(bundle.get_table_by_name("Table 1"), Table)
        self.assertEquals(bundle.get_table_by_name("Table "), None)

        # TableBundle.to_dict test
        self.assertIsInstance(bundle.to_dict(), dict)
        self.assertEquals(len(bundle.to_dict()['tables']), 1)
        self.assertEquals(
            bundle.to_dict()['tables'][0]['sections'][1]['name'], 'Gender')
        self.assertEquals(bundle.to_dict()[
                          'tables'][0]['sections'][1]['categories'][1]['name'], 'Female')

        # ----------------------------------------------------- #

        # Table.__init__ test
        self.assertRaises(TypeError, Table, "Table 1", "How are ya", "not bad")

        # SectionCategory.__init__ test
        self.assertRaises(TypeError, SectionCategory, "Cat 1", "Foo")

    def test_00_test_parse_1(self):
        xlsx_dir = os.path.join(self.cur_dir, 'xls', '1.xlsx')

        bundle = parse(xlsx_dir)

        # Table question test
        table_question = bundle.get_table_by_name('Table 1').question
        self.assertEquals(
            table_question, 'Q1. Do you have a social media account (such as Facebook or Twitter) that you have used in the last year?')

        # Table options test
        table_options = bundle.get_table_by_name('Table 1').options
        self.assertEquals(table_options, ['Yes', 'No', 'Don’t know'])

        # Random test 1
        values = bundle.get_table_by_name('Table 1')\
            .get_section_by_name('Age')\
            .get_category_by_name('25-34').values
        self.assertEquals(values, [20.7, 20.7, 20.7])

        # Random test 2
        values = bundle.get_table_by_name('Table 1')\
            .get_section_by_name('Social grade')\
            .get_category_by_name('C1').values
        self.assertEquals(values, [None, None, 16.6])

        # Random test 3
        values = bundle.get_table_by_name('Table 1')\
            .get_section_by_name('Region (4 code scale)')\
            .get_category_by_name('West').values
        self.assertEquals(values, [12.3, 12.3, 12.3])

        # Random test 4
        values = bundle.get_table_by_name('Table 2')\
            .get_section_by_name('Employment status')\
            .get_category_by_name('Part-time').values
        self.assertEquals(values, [13.4, 13.4, 13.4, 13.4, 13.4])

        # Random test 5
        values = bundle.get_table_by_name('Table 2')\
            .get_section_by_name('Education')\
            .get_category_by_name('Degree/Masters/PhD').values
        self.assertEquals(values, [17.6, 17.6, 99.0, 11.0, 17.6])

        # to_dict test
        # find Education -> No formal qualifications category
        cat = bundle.to_dict()['tables'][1]['sections'][5]['categories'][3]
        self.assertEquals(cat['name'], 'No formal qualifications')
        self.assertEquals(cat['values'], [16.6, 16.6, 16.6, 16.6, 16.6])

    def test_00_test_parse_2(self):
        xlsx_dir = os.path.join(self.cur_dir, 'xls', '2.xlsx')

        bundle = parse(xlsx_dir)

        # Table question test
        table_question = bundle.get_table_by_name('Table 1').question
        self.assertEquals(
            table_question, 'Q1. Do you have a social media account last year?')

        # Table options test
        table_options = bundle.get_table_by_name('Table 1').options
        self.assertEquals(table_options, ['Yes', 'No', 'Don’t know'])

        # Random test 1
        values = bundle.get_table_by_name('Table 1')\
            .get_section_by_name('Total')\
            .get_category_by_name('All').values
        self.assertEquals(values, [17.5, 1, 17.5])

        # Random test 2
        values = bundle.get_table_by_name('Table 1')\
            .get_section_by_name('Social grade')\
            .get_category_by_name('C2').values
        self.assertEquals(values, [11.5, 11.5, 11.5])

        # Random test 3
        values = bundle.get_table_by_name('Table 1')\
            .get_section_by_name('Wave 1')\
            .get_category_by_name('February').values
        self.assertEquals(values, [55, None, 58])

        # Random test 4
        values = bundle.get_table_by_name('Table 1')\
            .get_section_by_name('Wave 2')\
            .get_category_by_name('2017-01-02').values
        self.assertEquals(values, [55, 65, 58])

        # Random test 5
        values = bundle.get_table_by_name('Table 1')\
            .get_section_by_name('Wave 2')\
            .get_category_by_name('2017-01-03').values
        self.assertEquals(values, [25, 11, 23])

        # Random test 6
        values = bundle.get_table_by_name('Table 2')\
            .get_section_by_name('Wave 1')\
            .get_category_by_name('March').values
        self.assertEquals(values, [0, 0.11, 23, 23, 23])

        # to_dict test
        # find gender -> female category
        cat = bundle.to_dict()['tables'][0]['sections'][1]['categories'][1]
        self.assertEquals(cat['name'], 'Female')
        self.assertEquals(cat['values'], [23.4, 0.0, 23.4])
