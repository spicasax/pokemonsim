from pymongo import MongoClient

import doctest


class Card():
    def __init__(self, card_id):
        self.data = {}
        self.card_id = card_id
        return

    def __str__(self):
        """

        :return:

        >>> c = Card('xyp-XY01')
        >>> c.load_data()
        >>> c.__str__()
        'xyp-XY01'
        """
        return self.card_id

    def get_data(self):
        """

        :return:
        >>> c = Card('xyp-XY01')
        >>> c.load_data()
        >>> data = c.get_data()
        >>> data['name']
        'Chespin'
        """
        return self.data

    def load_data(self):
        """

        :return:

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


        :param card_id:

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

        :return:

        >>> c = PokemonCard('sm35-10')
        >>> c.get_current_HP()
        180
        """
        return self.currentHP

    def decrement_current_HP(self, amount):
        """


        :param amount:
        :return:

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
        if 'hp' in self.data:
            self.currentHP = int(self.data['hp'])
            pass
        return

    def get_all_attacks(self):
        pokemon_data = self.get_data()
        attacks = []
        if 'attacks' in pokemon_data:
            attacks = pokemon_data['attacks']
        return attacks

