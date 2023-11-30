class Configs():

    def __init__(self):
        self.subfolders = ('ADV', 'PollDay')
        self.nrcan_placenames_queries = {
            'Airport': ['Airport',
                        'Airfield'
                        ],
            'CFB': ['Canadian Forces Base',
                    'Canadian Forces Camp',
                    'Canadian Forces Range and/or Training Area (C.F.T.A.)',
                    'Canadian Forces Station'
                    ],
            "Cities": ['City'],
            "CmptRurComm": ['Compact Rural Community'],
            "Community": ['Community'],
            "Hamlet": ['Hamlet'],
            "Municipality": ['Municipality'],
            "NrthrnComm": ['Northern Community, '
                           'Northern Hamlet',
                           'Northern Settlement',
                           'Northern Village',
                           'Northern Village Municipality'
                           ],
            "Parks": ['Amusement Park',
                      'Federal Park',
                      'Industrial Park',
                      'International Park',
                      'Municipal Park',
                      'National Park',
                      'National Park Reserve',
                      'Park',
                      'Provincial Heritage Park',
                      'Provincial Historic Park',
                      'Provincial Marine Park',
                      'Provincial Park',
                      'Provincial Park Reserve',
                      'Provincial Wilderness Park',
                      'Public Park',
                      'Regional Park',
                      'Territorial Park',
                      'Trailer Park'],
            "Resort": ['Resort Municipality',
                       'Resort Village'],
            "SumVil": ['Summer Village'],
            "TownVillage": ['Town',
                            'Village'],
            "UrbComm": ['Urban Community']
        }
