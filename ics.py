#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from icalendar import Calendar
import pytz
from pytz import utc
import requests


def ics(login, pw):
    request = requests.get(
        'https://edt.univ-nantes.fr/sciences/g78125.ics',
        auth=(login, pw))
    if not 200 <= request.status_code < 300:
        return "Error status while retrieving the ics file."
    format = "%Y%m%dT%H%M%SZ"
    now = datetime.utcnow().strftime(format)
    paris = pytz.timezone('Europe/Paris')
    current = '99991231T235959Z'
    dtstart = dtend = description = location = ''
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
                location = unicode(component.get('LOCATION'))
    dtutcstart = utc.localize(datetime.strptime(start, format))
    dtutcend = utc.localize(datetime.strptime(end, format))
    dtstart = dtutcstart.astimezone(paris)
    dtend = dtutcend.astimezone(paris)
    return (u"Prochain cours  - le {date} de {start} à {end}\n"
            "Salle           - {location}\n"
            "Description     - {description}").format(
        date=dtstart.strftime("%d/%m/%Y"),
        start=dtstart.strftime("%Hh%M"),
        end=dtend.strftime("%Hh%M"),
        location=location,
        description=description).encode('utf8').strip()
