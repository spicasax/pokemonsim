# coding=utf-8
from pymongo import MongoClient
import doctest

client = MongoClient()
db = client.pokemontcg


def normalize_damage(damage):
    """
    >>> normalize_damage("60+")
    '60'
    >>> normalize_damage("120−")
    '120'
    """
    damage = damage.strip()
    damage = damage.encode('ascii', 'ignore').decode()
    damage = damage.replace('+', '')
    damage = damage.replace('-', '')
    damage = damage.replace('x', '')
    damage = damage.replace('×', '')
    damage = damage.replace('n/a', '')

    return damage


def pick_two_random_pokemon():
    card_ids = []
    for card in db.cards.aggregate([
        {'$match': {"supertype": "Pokémon"}},
        {'$sample': {'size': 2}},
    ]):
        print('Id, Name, Set: {0}, {1}, {2}'.format(card['id'], card['name'], card['set']))
        card_ids.append(card['id'])
        pass
    return card_ids
