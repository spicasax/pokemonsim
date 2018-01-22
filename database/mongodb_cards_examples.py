from pymongo import MongoClient
import pprint


client = MongoClient()
db = client.pokemontcg

# find a pokemon by id
for card in db.cards.find({'id': 'pl4-SH10'}):
    print('Id, Set: {0}, {1}'.format(card['id'],card['set']))

# pick two random pokemon
for card in db.cards.aggregate([
        {'$match':  {"supertype": "Pokémon"}},
        {'$sample': {'size': 2}},
      ]):
    print('Id, Name, Set: {0}, {1}, {2}'.format(card['id'], card['name'], card['set']))

# list the unique sets
pprint.pprint(db.cards.distinct("set"))

# group by set and count pokemon cards
pprint.pprint(list(db.cards.aggregate([
    {"$match": {"supertype": "Pokémon"}},
    {"$group": {"_id":"$set", "count":{"$sum":1}}}
])))
