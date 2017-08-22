import pandas as pd

cl = pd.read_csv('cards.csv', encoding="ISO-8859-1")

# print(cl.columns)

cards_sample = {'0': {'type': 'attack', 'stat': [1, -1, -3, 5]},
                '1': {'type': 'normal', 'stat': [5, 5, 5, -5]}
                }

columns = ['Card Name', 'Card Category', 'Card Type', 'Learning\rCategory',
           'Ranking Factor', 'Conversion Rate', 'Content Score', 'Spam Score',
           'Special Effect', 'Card Quantity', 'Card Description']


def generate_card_dict(card_category):
    cards = cl[cl['Card Category'] == card_category]

    cards_dict = {}
    count = 0
    for index, row in cards.iterrows():
        card_name = row['Card Name']
        card_type = row['Card Type']

        rf = int(row['Ranking Factor'])
        cr = int(row['Conversion Rate'])
        cs = int(row['Content Score'])
        ss = int(row['Spam Score'])
        stat = [rf, cr, cs, ss]

        special = row['Special Effect']
        description = row['Card Description']

        quantity = int(row['Card Quantity'])

        card = {'name': card_name,
                'type': card_type,
                'stat': stat,
                # 'special_effect': special,
                'description': description
                }

        for i in range(quantity):
            cards_dict[str(count)] = card
            count += 1

    return cards_dict

# tactic = 'Tactic Card'
# event = 'Event Card'
# cd = generate_card_dict(tactic)
# print(len(cd))
