#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import requests


bicloo_stations = {
    "place ricordeau": '38',
    "chanzy": '66',
    "strasbourg": '3',
    "hotel de ville": '2',
    "machine de l'ile": '43',
    "region": '84',
    "madeleine": '40',
    "moquechien": '22',
    "gare maritime": '42',
    "gare pt rousseau": '102',
    "vincent gache": '56',
    "barillerie": '7',
    "prairie au duc": '45',
    "station mobile": '103',
    "picasso": '10',
    "gare nord": '62',
    "palais des sports": '58',
    "petit port": '94',
    "bourse": '31',
    "canclaux": '74',
    "gue moreau": '72',
    "saint similien": '19',
    "tabarly": '51',
    "aignan": '89',
    "ecole d'architecture": '77',
    "anatole france": '87',
    "martyrs nantais": '47',
    "saint donatien": '97',
    "commerce": '30',
    "guist'hau nord": '27',
    "place aristide briand": '15',
    "millerand": '83',
    "mediatheque": '34',
    "rd pt vannes": '91',
    "place republique": '46',
    "bellamy": '20',
    "mangin": '81',
    "magellan": '55',
    "de gaulle": '78',
    "place waldeck rousseau": '67',
    "gaetan rondeau": '57',
    "malakoff": '79',
    "lamoriciere": '75',
    "place viarme": '18',
    "michelet": '95',
    "bel air": '85',
    "dt pt rennes": '92',
    "stade saupin": '59',
    "olivettes": '53',
    "place rene bouhier": '76',
    "boucherie": '8',
    "sarradin": '73',
    "duchesse anne": '49',
    "facultes": '93',
    "verdun": '48',
    "prefecture": '1',
    "buat": '23',
    "proce": '90',
    "rubens": '32',
    "sainte elisabeth": '17',
    "duguay trouin": '29',
    "chateau": '50',
    "feydeau": '37',
    "hauts paves": '86',
    "quai moncousu": '39',
    "jean v": '35',
    "dalby": '25',
    "palais de justice": '44',
    "st jacques": '99',
    "victor hugo": '80',
    "lieu unique": '61',
    "marche talensac sud": '21',
    "marche talensac nord": '71',
    "chantier naval": '41',
    "place delorme": '12',
    "huit mai": '98',
    "guist'hau sud": '26',
    "baco": '52',
    "calvaire": '11',
    "jardin des plantes": '63',
    "place edouard normand": '16',
    "mellinet": '88',
    "moulin": '4',
    "tortiere": '96',
    "saint clement": '64',
    "guepin": '9',
    "racine": '33',
    "gare sud": '60',
    "versailles": '24',
    "manufacture": '69',
    "alger": '36',
    "sebilleau": '82',
    "brossard": '5',
    "pirmil": '101',
    "greneraie": '100',
    "cite internationale des congres": '54',
    "saint felix": '14',
    "place de l'edit nantes": '28',
    "livet": '68',
    "cours sully": '65',
    "bretagne sud": '13',
    "place du cirque": '6'
}


def read_credentials():
    with codecs.open('.bicloo_credentials', 'r', 'utf8') as fh:
        return fh.read().strip()


def bicloo(station):
    key = read_credentials()
    if station == 'help':
        return bicloo_help()
    if station not in bicloo_stations:
        return "je ne connais pas cette station."
    request_string = u'https://api.jcdecaux.com/vls/v1/stations/' \
        + '{station_number}?contract=Nantes&apiKey={key}'.format(
            station_number=bicloo_stations[station],
            key=key)
    request = requests.get(request_string)
    data = request.json()
    try:
        result = ("Ouverte: {status}\n"
                  "Bonus: {bonus}\n"
                  "CB: {cb}\n"
                  "Vélos disponibles: {bikes}\n"
                  "Emplacements disponibles: {stands}").format(
            status='oui' if data['status'] == 'OPEN' else 'non',
            bonus='oui' if data['bonus'] else 'non',
            cb='oui' if data['banking'] else 'non',
            bikes=data['available_bikes'],
            stands=data['available_bike_stands'])
    except:
        result = 'Réponse incomplète. J\'peux pas aider :(('
    return result


def bicloo_help():
    return ("# bicloo station où station est le nom "
            "de la station qui t'intéresse. Le nom est "
            "standardisé (lowercase pas d'accent).")




