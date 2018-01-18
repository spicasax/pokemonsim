import json
import os
from pymongo import MongoClient

HOME_DIR = os.getenv("HOME")
CARDS_DIR = os.path.join(HOME_DIR, 'pokemon-tcg-data', 'json', 'cards')
print(CARDS_DIR)

# drop and create cards database
client = MongoClient()
db = client.pokemontcg
result = db.cards.delete_many({})
print('cards deleted count: {0}'.format(result.deleted_count))

set_files = [f for f in os.listdir(CARDS_DIR) if os.path.isfile(os.path.join(CARDS_DIR, f))]

for set_file in set_files:
    with open(os.path.join(CARDS_DIR, set_file)) as json_file:
        json_data = json.load(json_file)
        for i in range(0, len(json_data)):
            #print(json_data[i]['name'])
            card_id = db.cards.insert_one(json_data[i]).inserted_id
            #print(card_id)
            pass

print('cards total count: {0}'.format(db.cards.count()))