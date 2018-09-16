from pymongo import MongoClient
import pprint


client = MongoClient()
db = client.pokemontcg

# find a pokemon by id and print out the raw data
for card in db.cards.find({'id': 'xy12-13'}):
    # print('Id, Set: {0}, {1}'.format(card['id'],card['set']))
    pprint.pprint(card)