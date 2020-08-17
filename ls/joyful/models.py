# ------------------------------------------------------------------------------
# Joyful models
# ------------------------------------------------------------------------------
import datetime as dt
from dateutil.parser import parse as dt_parse
from dateutil.parser import ParserError
from django.conf import settings
from django.http import Http404, JsonResponse
from django.template.response import TemplateResponse
from django.utils.translation import get_language, gettext_lazy as _
from django.utils import timezone
from ls.joyous.models.calendar import CalendarPage, DatePictures
from ls.joyous.models import (SimpleEventPage, MultidayEventPage,
                              RecurringEventPage, EventExceptionBase)
from .utils import getLocalDatetimeAtDate, ProxyPageMixin, getFirstDayOfWeek
from wagtail.contrib.routable_page.models import route
from . import __version__

# ------------------------------------------------------------------------------
class FullHoliday(dict):
    def __init__(self, date, holiday):
        self['display'] = "background"
        self['title'] = holiday
        self['start'] = date
        self['end']   = date
        self['className'] = "joy-bg-holiday"

class FullEventBase(dict):
    def __init__(self, thisEvent):
        super().__init__()
        self['title'] = thisEvent.title
        self['url']   = thisEvent.url

class FullOneOffEvent(FullEventBase):
    def __init__(self, thisEvent):
        super().__init__(thisEvent)
        page = thisEvent.page
        if page.time_from is None:
            self['start'] = page._getFromDt().date()
        else:
            self['start'] = page._getFromDt()
        if page.time_to is None:
            self['end'] = page._getToDt().date() + dt.timedelta(days=1)
        else:
            self['end'] = page._getToDt()

class FullRecurringEvent(FullEventBase):
    def __init__(self, date, thisEvent):
        super().__init__(thisEvent)
        page = thisEvent.page
        if page.time_from is None:
            self['start'] = date
        else:
            self['start'] = getLocalDatetimeAtDate(date, page.time_from, page.tz)
        endDate = date + dt.timedelta(days=page.num_days - 1)
        if page.time_to is None:
            self['end'] = endDate + dt.timedelta(days=1)
        else:
            self['end'] = getLocalDatetimeAtDate(endDate, page.time_to, page.tz)
        #TODO? self['groupId'] = page.uid

class FullEventTypeError(TypeError):
    pass

def makeFullEvent(date, thisEvent):
    page = thisEvent.page
    if isinstance(page, (SimpleEventPage, MultidayEventPage)):
        return FullOneOffEvent(thisEvent)

    elif isinstance(page, (RecurringEventPage, EventExceptionBase)):
        return FullRecurringEvent(date, thisEvent)

    else:
        raise FullEventTypeError("Unsupported page type")


FULL_VIEWS = {'L': "listYear",
              'M': "dayGridMonth",
              'W': "timeGridWeek",
              'D': "timeGridDay",}

class FullCalendarPage(ProxyPageMixin, CalendarPage):
    class Meta(ProxyPageMixin.Meta):
        verbose_name = _("full calendar page")
        verbose_name_plural = _("full calendar pages")

    @route(r"^events/$")
    def serveData(self, request):
        try:
            startDt = dt_parse(request.GET.get('start', ""))
            endDt   = dt_parse(request.GET.get('end', ""))
        except ParserError:
            raise Http404("invalid parameters")
        fullEvents = []
        evods = self._getEventsByDay(request, startDt.date(), endDt.date())
        for evod in evods:
            if evod.holiday:
                fullEvents.append(FullHoliday(evod.date, evod.holiday))
            for thisEvent in evod.days_events:
                fullEvents.append(makeFullEvent(evod.date, thisEvent))
        return JsonResponse(fullEvents, safe=False)

    @route(r"^month/$")
    @route(r"^{YYYY}/{MM}/$".format(**DatePictures))
    def serveMonth(self, request, year=None, month=None):
        return self.serveFull(request)

    @route(r"^week/$")
    @route(r"^{YYYY}/W{WW}/$".format(**DatePictures))
    def serveWeek(self, request, year=None, week=None):
        return self.serveFull(request)

    @route(r"^day/$")
    @route(r"^{YYYY}/{MM}/{DD}/$".format(**DatePictures))
    def serveDay(self, request, year=None, month=None, dom=None):
        return self.serveFull(request)

    @route(r"^upcoming/$")
    def serveUpcoming(self, request):
        return self.serveFull(request)

    @route(r"^past/$")
    def servePast(self, request):
        return self.serveFull(request)

    def serveFull(self, request):
        cxt = self.get_context(request)
        cxt.update({'version':  __version__,
                    'today':    timezone.localdate(),
                    'language': get_language() })
        fullViews = [FULL_VIEWS.get(choice) for choice in self.view_choices]
        cxt['viewChoices'] = ",".join(view for view in fullViews if view)
        cxt['defaultView'] = FULL_VIEWS.get(self.default_view, "dayGridMonth")
        if getFirstDayOfWeek() == 1:
            cxt['firstDayOfWeek']      = 1
            cxt['daysWithinFirstWeek'] = 4
        else:
            cxt['firstDayOfWeek']      = 0
            cxt['daysWithinFirstWeek'] = 5
        cxt.update(self._getExtraContext("full"))
        return TemplateResponse(request, "joyful/full_calendar_page.html", cxt)

for Page in (SimpleEventPage, MultidayEventPage, RecurringEventPage):
    Page.parent_page_types.append("joyful.FullCalendarPage")

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
