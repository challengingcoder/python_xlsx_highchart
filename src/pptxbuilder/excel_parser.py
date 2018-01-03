from datetime import datetime

from xlrd import open_workbook, xldate_as_tuple
from xlrd.biffh import XLRDError

"""
Contains parser tools and relevant oop classes to convert excel files to a certain format.

- Table Bundle
Holds one or more tables.

- Table
A `table` has a question, options and sections.

- Table Section
There are 3 sections below. Total, Gender and Age.
+--------+--------+--------+--------+--------+--------+--------+--------+
| Total  | Gender |        |        | Age    |        |        |        |
+--------+--------+--------+--------+--------+--------+--------+--------+

- Section Category
+--------+
| Male   | -> Category name
| 27%    | -> Category values
| 27%    |
| 27%    |
| 27%    |
| 27%    |
+--------+
"""


class NameExistsError(Exception):
    def __init__(self, message=''):
        super(NameExistsError, self).__init__(message)


class TableBundle(object):
    def __init__(self, bundle_name=None):
        self._name = bundle_name
        self._tables = []

    @property
    def name(self):
        return self._name

    @property
    def tables(self):
        return self._tables

    def add_table(self, table):
        if (self.get_table_by_name(table.name) is not None):
            raise NameExistsError(
                'Table "{}" exists in Bundle'.format(table.name))

        self._tables.append(table)

    def get_table_by_name(self, table_name):
        for table in self._tables:
            if table.name == table_name:
                return table

    def to_dict(self):
        return {
            'name': self._name,
            'tables': [x.to_dict() for x in self._tables]
        }


class Table(object):
    def __init__(self, table_name, question, options):
        if not isinstance(options, list):
            raise TypeError('"options" must be list')

        if len(options) == 0:
            raise TypeError('"options" can not be empty')

        if not question:
            raise TypeError('"question" can not be empty')

        self._name = table_name
        self._question = question
        self._options = options
        self._sections = []

    def __repr__(self):
        return '{} ({})'.format(self.__class__, self._name)

    @property
    def name(self):
        return self._name

    @property
    def question(self):
        return self._question

    @question.setter
    def question(self, val):
        self._question = val

    @property
    def options(self):
        return self._options

    @options.setter
    def options(self, val):
        self._options = val

    @property
    def sections(self):
        return self._sections

    def add_section(self, section):
        if (self.get_section_by_name(section.name) is not None):
            raise NameExistsError(
                'Section "{}" exists in Table'.format(section.name))

        self._sections.append(section)

    def get_section_by_name(self, section_name):
        for section in self._sections:
            if section.name == section_name:
                return section

    def to_dict(self):
        return {
            'name': self._name,
            'question': self._question,
            'options': self._options,
            'sections': [x.to_dict() for x in self._sections],
            'data_by_options': self.data_by_options()
        }

    def data_by_options(self):
        data = []
        s = 0
        for section in self._sections:
            v = []
            o = 0
            for opt in self._options:
                k = {'name': opt, 'data': []}
                categories = section.to_dict()['categories']
                c = 0
                for cat in categories:
                    try:
                        k['data'].append(cat['data'][o])
                    except IndexError:
                        pass
                    c += 1
                v.append(k)
                o += 1
            data.append(v)
            s += 1

        return data


class TableSection(object):
    def __init__(self, section_name):
        self._name = section_name
        self._categories = []

    def __repr__(self):
        return '{} ({})'.format(self.__class__, self._name)

    @property
    def name(self):
        return self._name

    @property
    def categories(self):
        return self._categories

    def add_category(self, category):
        if (self.get_category_by_name(category.name) is not None):
            raise NameExistsError(
                'Category "{}" exists in Section'.format(category.name))

        self._categories.append(category)

    def get_category_by_name(self, category_name):
        for category in self._categories:
            if category.name == category_name:
                return category

    def to_dict(self):
        return {
            'name': self._name,
            'categories': [x.to_dict() for x in self._categories]
        }


class SectionCategory(object):
    def __init__(self, category_name, values=[]):
        if not isinstance(values, list):
            raise TypeError('Values must be list!')

        self._name = category_name
        self._values = values

    def __repr__(self):
        return '{} {}: {}'.format(self.__class__, self._name, self._values)

    @property
    def name(self):
        return self._name

    @property
    def values(self):
        return self._values

    @values.setter
    def values(self, new_val):
        self._values = new_val

    def to_dict(self):
        return {'name': self.name, 'data': self._values}


class IncompatibleExcelException(Exception):
    def __init__(self, message):
        super(IncompatibleExcelException, self).__init__(message)


class UnsupportedFileException(Exception):
    def __init__(self, message):
        super(UnsupportedFileException, self).__init__(message)


def parse(filename):
    """
    Parse excel file content to structured data

    :param filename: The path to the excel file to be opened.

    :returns: A TableBundle object that contains Tables from excel file given.
    """

    try:
        workbook = open_workbook(filename)
    except XLRDError:
        raise UnsupportedFileException('Unsupported file format')

    tables = [parse_worksheet(workbook.sheet_by_index(s))
              for s in range(workbook.nsheets)]

    bundle = TableBundle()
    for table in tables:
        bundle.add_table(table)

    return bundle


def parse_worksheet(worksheet):
    """
    Parse excel file content to structured data

    :param worksheet: Worksheet object to parse.
    """

    # Row count of worksheet
    worksheet_rows = worksheet.nrows

    # Column count of worksheet
    worksheet_cols = worksheet.ncols

    def cell_value(r, c, force_datetime=False, multiple_float=None):
        """
        Shortcut function to get value by row and column numbers.

        :param r: Row number
        :param c: Column number
        :param force_datetime: Default False. When it True trys convert cell data to datetime object
        :param multiple_float:
        """
        val = worksheet.cell_value(rowx=r, colx=c)

        # if found value is a string, strip it.
        if isinstance(val, str):
            val = val.strip()
            if val == '-':
                val = None

        if multiple_float is not None and isinstance(val, float):
            if str(val).startswith('0.'):
                val = round(val * multiple_float)

        if force_datetime and isinstance(val, float):
            # 42738.0
            if (len(str(val)) >= 7):
                try:
                    val_date = datetime(
                        *xldate_as_tuple(val, worksheet.book.datemode))
                    val = val_date.strftime('%Y-%m-%d')
                except Exception:
                    pass

        return val

    """
    Question of table. Parse from A3

    e.g. 'Q1. Do you have a social media account (such as Facebook or Twitter)
    that you have used in the last year?'
    """
    try:
        question = cell_value(2, 0)
        assert question != ''
    except (IndexError, AssertionError):
        raise IncompatibleExcelException('Question of table not found at A3! Worksheet: {}'.format(worksheet.name))

    """
    Options of table. Parse from B3 to end of worksheet.

    e.g. ['Yes', 'No', 'Don’t know']
    """
    options = []
    for i in range(2, (worksheet_rows)):
        val = cell_value(i, 1)
        if val != '':
            options.append(val)

    """
    Options size + 2 (2 column space from top) must be equals to
    worksheet rows count.
    """
    if (len(options) + 2) != worksheet_rows:
        raise IncompatibleExcelException('Options are not in expected position! Worksheet: {}'.format(worksheet.name))

    """
    Find section starting column numbers.

    e.g. [2, 3, 5, 10, 14, 18, 22]
    """
    section_indices = []
    used_section_names = []
    for i in range(2, worksheet_cols):
        # if next column content is empty or duplicate name (can be in merged cells), it means this section ended.
        c_v = cell_value(0, i)
        if c_v != '' and c_v not in used_section_names:
            section_indices.append(i)
            used_section_names.append(c_v)

    if len(section_indices) == 0:
        raise IncompatibleExcelException('No section found! Worksheet: {}'.format(worksheet.name))

    """
    Generate section boundaries.

    e.g [[2, 1], [3, 2], [5, 5], [10, 4], [14, 4], [18, 4], [22, 5]]
                    ↓
        This section starts at column 3 and section length is 2 column
    """
    section_bounds = []
    for i in range(len(section_indices)):
        # Get next item in the list
        try:
            n = section_indices[i + 1]
        except IndexError:
            n = worksheet_cols

        # Current item
        t = section_indices[i]

        # Length of the section
        le = n - t

        section_bounds.append([t, le])

    table = Table(worksheet.name, question, options)
    for sect in section_bounds:
        sect_starts = sect[0]
        sect_len = sect[1]

        section_name = cell_value(0, sect_starts)

        new_section = TableSection(section_name)

        for m in range(sect_len):
            cat_name = cell_value(1, sect_starts, True)
            cat_vals = [cell_value(r, sect_starts, multiple_float=100) for r in range(2, worksheet_rows)]

            if isinstance(cat_name, int) or isinstance(cat_name, float):
                cat_name = str(cat_name)

            if cat_name.strip() == '':
                raise IncompatibleExcelException(
                    'Category name can not be empty! Worksheet: {}, Section: {}'.format(worksheet.name, section_name))

            new_cat = SectionCategory(cat_name, cat_vals)
            new_section.add_category(new_cat)
            sect_starts += 1

        table.add_section(new_section)

    return table
