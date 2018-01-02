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
