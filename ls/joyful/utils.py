# ------------------------------------------------------------------------------
# Joyful utils
# ------------------------------------------------------------------------------
import datetime as dt
from django.conf import settings
from django.utils import timezone

from ls.joyous.utils.mixins import ProxyPageMixin
from ls.joyous.utils.telltime import getLocalDatetime, getAwareDatetime
from ls.joyous.utils.weeks import getFirstDayOfWeek

# ------------------------------------------------------------------------------
def _getLocalDatetimeAtDate(atDate, time, *args, **kwargs):
    """
    Get the datetime at a certain date in the local timezone
    """
    # I don't know what date to use to get the correct atDate, so
    # try all the possibilities until we get it.
    for offset in (0, 1, -1, 2, -2):
        date = atDate + dt.timedelta(days=offset)
        retval = getLocalDatetime(date, time, *args, **kwargs)
        if retval.date() == atDate:
            return retval

try:
    # TODO: add getLocalDatetimeAtDate to Joyous utils
    from ls.joyous.utils.telltime import getLocalDatetimeAtDate
except ImportError:
    getLocalDatetimeAtDate = _getLocalDatetimeAtDate

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
