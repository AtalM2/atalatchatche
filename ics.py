#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
from datetime import datetime
from icalendar import Calendar
import locale
import pytz
from pytz import utc
import requests


def read_credentials():
    with codecs.open('.ics_credentials', 'r', 'utf8') as fh:
        data = fh.read().strip().split('	')
        return data[0], data[1]


def ics():
    previous_locale = locale.getlocale()
    locale.setlocale(locale.LC_ALL, 'fr_FR')
    login, pw = read_credentials()
    request = requests.get(
        'https://edt.univ-nantes.fr/sciences/g78125.ics',
        auth=(login, pw))
    if not 200 <= request.status_code < 300:
        return "Error status while retrieving the ics file."
    format = "%Y%m%dT%H%M%SZ"
    now = datetime.utcnow().strftime(format)
    paris = pytz.timezone('Europe/Paris')
    current = '99991231T235959Z'
    dtstart = dtend = description = ''
    for component in Calendar.from_ical(request.text).walk():
        if component.name == 'VEVENT':
            current_start = component.get('DTSTART').to_ical()
            if now > current_start:
                continue
            if current_start < current:
                current = current_start
                description = unicode(component.get('DESCRIPTION'))
                start = component.get('DTSTART').to_ical()
                end = component.get('DTEND').to_ical()
    dtutcstart = utc.localize(datetime.strptime(start, format))
    dtutcend = utc.localize(datetime.strptime(end, format))
    dtstart = dtutcstart.astimezone(paris)
    dtend = dtutcend.astimezone(paris)
    result = (u"Prochain cours le {date} de {start} à {end} :\n"
              "{description}").format(
        date=dtstart.strftime("%A %d/%m/%Y"),
        start=dtstart.strftime("%Hh%M"),
        end=dtend.strftime("%Hh%M"),
        description=description).encode('utf8').strip()
    locale.setlocale(locale.LC_ALL, previous_locale)
    return result










