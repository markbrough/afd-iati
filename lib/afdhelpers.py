
# -*- coding: UTF-8 -*-

AFD_COUNTRIES = {'SYRIENNE, REP.': 'SYRIENNE, REPUBLIQUE ARABE',
                     'SYRIENNE REP.': 'SYRIENNE, REPUBLIQUE ARABE',
                     'VIET-NAM': 'VIET NAM',
                     'CENTRAFRIQUE': 'CENTRAFRICAINE, REPUBLIQUE',
                     'RDCONGO': 'CONGO, LA REPUBLIQUE DEMOCRATIQUE DU',
                     'TERR.AUTO.PALES': 'PALESTINIEN OCCUPE, TERRITOIRE',
                     'BIRMANIE': 'MYANMAR',
                     'TANZANIE': 'TANZANIE, REPUBLIQUE-UNIE DE',
                     'COTE D IVOIRE': "COTE D'IVOIRE",
                     'DOMINICAINE REP': 'DOMINICAINE, REPUBLIQUE',
                     'ILE DOMINIQUE': 'DOMINIQUE',
                     'LAOS': 'LAO, REPUBLIQUE DEMOCRATIQUE POPULAIRE',
                     'ZONE NEUTRE': "",
                     'SAO-TOME': "SAO TOME-ET-PRINCIPE"}

AFD_STATUSES = {
            'Faisabilité': '1',
            'Identification': '1',
            '': '2',
            'Ex\xef\xbf\xbdcution': '2',
            'Exécution': '2',
            'Achev\xef\xbf\xbd': '3',
            'Achevé': '3',
            'Evaluation': '4',
            'Annulé': '5'
        }

STATUSCODES = {
            '1': 'Pipeline/identification',
            '2': 'Implementation',
            '3': 'Completion',
            '4': 'Post-completion',
            '5': 'Cancelled'
        }

FINANCETYPES = {
            "": {
                'code': '',
                'text': ''
            },
            "ACTION": {
                'code': '500',
                'text': 'EQUITY'
            },
            "GARANTIES DONNEES": {
                'code': '900',
                'text': 'OTHER SECURITIES/CLAIMS'
            },
            "PRET": {
                'code': '400',
                'text': 'LOAN'
            },
            "SUBVENTION": {
                'code': '100',
                'text': 'GRANT'
            }
        }

AFD_SECTORS = {
    "": "",
    "Agriculture et sécurité alimentaire": "31100",
    "Eau et assainissement": "14000",
    "Education": "11100",
    "Environnement et ressources naturelles": "41000",
    "Hors secteurs CICID": "99810",
    "Infrastructures et développement urbain": "21000",
    "Santé et lutte contre le sida": "12200",
    "Secteur productif": "32100"
}

SECTORS = {
    "": "",
    "31100": "Agriculture",
    "14000": "Water and sanitation",
    "11100": "Education",
    "41000": "Environment",
    "99810": "Sectors not specified",
    "21000": "Infrastructure",
    "12200": "Health",
    "32100": "Industry"    
}
