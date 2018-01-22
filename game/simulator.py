import random
import logging

from deck import PokemonCard
from card_helper import normalize_damage

logging.basicConfig(filename='../logs/simulator.log',level=logging.DEBUG)


class OneOnOneBattleSimulator():
    """
    A very basic way to play, kids sometimes will just battle Pokemon one on one, without worrying about energies,
    trainers, etc.
    """
    def __init__(self, card1_id, card2_id):
        """

        :param card1_id:
        :param card2_id:

        >>> b = OneOnOneBattleSimulator('xyp-XY01', 'xyp-XY174')
        initializing battle with: xyp-XY01, xyp-XY174
        """
        # determine which card goes first:
        coin_flip = random.randint(0, 1)
        if coin_flip:
            self.card1 = PokemonCard(card1_id)
            self.card2 = PokemonCard(card2_id)
            name1 = self.card1.get_data()['name']
            name2 = self.card2.get_data()['name']
        else:
            self.card1 = PokemonCard(card2_id)
            self.card2 = PokemonCard(card1_id)
            name1 = self.card2.get_data()['name']
            name2 = self.card1.get_data()['name']

        logging.debug('******************* BEGIN GAME *******************')
        logging.debug('initializing battle with: {0} [{1}], {2} [{3}]'.format(card1_id, name1, card2_id, name2))

        return

    def battle(self):
        done = False
        counter = 0

        # status at beginning of turn
        logging.debug("Card1: ")
        logging.debug(self.card1.__str__())
        currentHP1 = self.card1.get_current_HP()
        logging.debug('current HP: ')
        logging.debug(currentHP1)

        logging.debug("Card2: ")
        logging.debug(self.card2.__str__())
        currentHP2 = self.card2.get_current_HP()
        logging.debug('current HP: ')
        logging.debug(currentHP2)

        winner = ''

        attacker = self.card1
        not_attacker = self.card2

        while not done:
            # attacker card attacks not_attacker card
            logging.debug('{0} attacks {1}'.format(attacker.get_data()['name'], not_attacker.get_data()['name']))
            random_attack_idx = random.randint(0, len(attacker.get_all_attacks())-1)
            random_attack = attacker.get_all_attacks()[random_attack_idx]

            if len(random_attack['damage']) > 0:
                damage = int(normalize_damage(random_attack['damage']))
            else:
                damage = 0
            logging.debug('Attack: {0}, Damage: {1}'.format(random_attack['name'], damage))
            not_attacker.decrement_current_HP(damage)
            logging.debug('now {0} hp is: {1}'.format(not_attacker.get_data()['name'], not_attacker.get_current_HP()))

            if not_attacker.get_current_HP() == 0:
                done = True
                logging.debug('{0} wins'.format(attacker.get_data()['name']))
                winner = attacker.__str__()

            # swap attacker and not_attacker
            tmp = attacker
            attacker = not_attacker
            not_attacker = tmp

            # infinite loop check:
            counter += 1
            if counter >= 50:
                logging.error('Infinite loop check: stopping after 50 rounds')
                break

        logging.debug('******************** GAME OVER *******************')
        return winner

    pass


def main():
    from pymongo import MongoClient
    client = MongoClient()
    db = client.pokemontcg

    # pick two random Pokemon cards
    card_ids = []
    for card in db.cards.aggregate([
        {'$sample': {'size': 2}},
        {'$match': {"supertype": "Pokémon"}}
    ]):
        print('Id, Name, Set: {0}, {1}, {2}'.format(card['id'], card['name'], card['set']))
        card_ids.append(card['id'])
        pass

    # run battle simulation a number of times, then see which wins more often, and what percent
    if len(card_ids) == 2:
        winners = []
        num_battles = 100
        for i in range (0, num_battles):
            battle = OneOnOneBattleSimulator(card_ids[0], card_ids[1])
            winner = battle.battle()
            winners.append(winner)
        card_ids_1_wins = winners.count(card_ids[0])
        card_ids_2_wins = num_battles - card_ids_1_wins
        if card_ids_1_wins > card_ids_2_wins:
            print('Winner: {0} [{1}]'.format(card_ids[0], card_ids_1_wins / num_battles))
        elif card_ids_2_wins > card_ids_1_wins:
            print('Winner: {0} [{1}]'.format(card_ids[1], card_ids_2_wins / num_battles))
        else:
            print('Draw: no winner.')
    else:
        # it is not as interesting to battle same card
        print('Skip: drew same card twice.')

    return

if __name__ == "__main__":
    main()