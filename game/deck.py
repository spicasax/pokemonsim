# coding=utf-8
from pymongo import MongoClient

import doctest


class Card:
    def __init__(self, card_id):
        """
        >>> c = Card('xyp-XY01')
        >>> c.card_id
        'xyp-XY01'
        """
        self.data = {}
        self.card_id = card_id
        self.isDiscarded = False
        return

    def __str__(self):
        """
        >>> c = Card('xyp-XY01')
        >>> c.load_data()
        >>> c.__str__()
        'xyp-XY01'
        """
        return self.card_id

    def get_data(self):
        """
        >>> c = Card('xyp-XY01')
        >>> c.load_data()
        >>> data = c.get_data()
        >>> data['name']
        'Chespin'
        """
        return self.data

    def load_data(self):
        """
        >>> c = Card('xyp-XY01')
        >>> c.load_data()
        >>> data = c.get_data()
        >>> data['id']
        'xyp-XY01'
        """
        client = MongoClient()
        db = client.pokemontcg
        doc = db.cards.find_one({"id": self.card_id})
        self.data = doc


class PokemonCard(Card):
    def __init__(self, card_id):
        """
        >>> c = PokemonCard('sm35-10')
        >>> c.isEX
        False
        >>> c.isMega
        False
        >>> c.isGX
        True
        """
        Card.__init__(self, card_id)
        self.energies = []
        self.damage = 0

        self.load_data()
        data = self.get_data()

        self.isGX = False
        if data['subtype'] == 'GX':
            self.isGX = True

        self.isEX = False
        if data['subtype'] == 'EX':
            self.isEX = True

        self.isMega = False
        if data['subtype'] == 'MEGA':
            self.isMega = True

        self.currentHP = 0
        if 'hp' in data: self.currentHP = int(data['hp'])

        return

    def get_current_HP(self):
        """
        >>> c = PokemonCard('sm35-10')
        >>> c.get_current_HP()
        180
        """
        return self.currentHP

    def decrement_current_HP(self, amount):
        """
        >>> c = PokemonCard('sm35-10')
        >>> c.decrement_current_HP(10)
        170
        >>> c.get_current_HP()
        170
        """
        self.currentHP -= amount
        if self.currentHP < 0:
            self.currentHP = 0
        return self.currentHP

    def reset_HP(self):
        """
        >>> c = PokemonCard('sm35-10')
        >>> c.decrement_current_HP(10)
        170
        >>> c.reset_HP()
        >>> c.get_current_HP()
        180
        """
        if 'hp' in self.data:
            self.currentHP = int(self.data['hp'])
            pass
        return

    def get_all_attacks(self):
        """
        >>> c = PokemonCard('sm35-10')
        >>> attacks = c.get_all_attacks()
        >>> len(attacks)
        3
        """
        pokemon_data = self.get_data()
        attacks = []
        if 'attacks' in pokemon_data:
            attacks = pokemon_data['attacks']
        return attacks


class EnergyCard(Card):
    def __init__(self, card_id):
        """
        >>> c = EnergyCard('base1-101')
        >>> c.card_id
        'base1-101'
        >>> c.energy_type
        'Psychic Energy'
        """
        Card.__init__(self, card_id)

        self.load_data()
        data = self.get_data()

        self.energy_type = data['name']

        return


class TrainerCard(Card):
    def __init__(self, card_id):
        """
        >>> c = TrainerCard('base1-93')
        >>> c.card_id
        'base1-93'
        >>> c.name
        'Gust of Wind'
        >>> c.text[0]
        "Choose 1 of your opponent's Benched Pokémon and switch it with his or her Active Pokémon."
        """
        Card.__init__(self, card_id)

        self.load_data()
        data = self.get_data()

        self.name = data['name']
        self.text = data['text']

        return