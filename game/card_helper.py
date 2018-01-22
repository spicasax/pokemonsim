from pymongo import MongoClient

client = MongoClient()
db = client.pokemontcg


def normalize_damage(damage):
    damage = damage.replace('+', '')
    damage = damage.replace('-', '')
    damage = damage.replace('x', '')
    damage = damage.replace('×', '')
    damage = damage.replace('n/a', '')
    return damage


def pick_two_random_pokemon():
    card_ids = []
    for card in db.cards.aggregate([
        {'$sample': {'size': 2}},
        {'$match': {"supertype": "Pokémon"}}
    ]):
        print('Id, Name, Set: {0}, {1}, {2}'.format(card['id'], card['name'], card['set']))
        card_ids.append(card['id'])
        pass
    return card_ids
