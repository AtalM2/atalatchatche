#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import codecs
import requests


# def read_credentials():
#     with codecs.open('.tan_credentials', 'r', 'utf8') as fh:
#         return fh.read().strip()


def tan(station):
    if station == 'help':
        return tan_help()
    request_string = (u'https://open.tan.fr/ewp/tempsattente.json/'
                      '{station}').format(station=station)
    request = requests.get(request_string)
    data = request.json()
    print data
    # try:
    result = u''
    for line in data:
        if line['temps'] == 'Close':
            continue
        result += u"Ligne {line} vers {terminus} : {time}\n".format(
            line=line['ligne']['numLigne'],
            terminus=line['terminus'],
            time=line['temps'])
    result = result.encode('utf8')
    # except:
    #     result = 'Réponse incomplète. J\'peux pas aider :(('
    return result


def tan_help():
    return ("# tan station où station est le nom "
            "de la station qui t'intéresse.")







