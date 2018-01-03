from pptxbuilder.constants import *
from gettext import gettext as _


def str_chart_type(t):
    try:
        return {
            CHART_TYPE_BAR: _('Bar'),
            CHART_TYPE_COLUMN: _('Column'),
            CHART_TYPE_LINE: _('Line'),
            CHART_TYPE_PIE: _('Pie')
        }[t]
    except KeyError:
        return None


def str_series_opt(t):
    try:
        return {
            SERIES_BY_CATEGORIES: _('Categories'),
            SERIES_BY_OPTIONS: _('Options')
        }[t]
    except KeyError:
        return None
