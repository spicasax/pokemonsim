import random
import logging
import doctest

from deck import PokemonCard
from card_helper import normalize_damage, pick_two_random_pokemon

logging.basicConfig(filename='../logs/simulator.log',level=logging.DEBUG)


class OneOnOneBattleSimulator():
    """
    A very basic way to play, kids sometimes will just battle Pokemon one on one, without worrying about energies,
    trainers, etc.

    For a given card, each attack id chosen randomly from that card's attacks.
    """
    def __init__(self, card1_id, card2_id):
        """

        :param card1_id:
        :param card2_id:

        >>> b = OneOnOneBattleSimulator('xyp-XY01', 'xyp-XY174')

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
            if len(attacker.get_all_attacks()) > 0:
                random_attack_idx = random.randint(0, len(attacker.get_all_attacks())-1)
                random_attack = attacker.get_all_attacks()[random_attack_idx]

                damage = 0
                if 'damage' in random_attack:
                    normalized_damage = normalize_damage(random_attack['damage'])
                    if len(normalized_damage) > 0:
                        damage = int(normalized_damage)

                logging.debug('Attack: {0}, Damage: {1}'.format(random_attack['name'], damage))
                not_attacker.decrement_current_HP(damage)
                logging.debug('now {0} hp is: {1}'.format(not_attacker.get_data()['name'], not_attacker.get_current_HP()))

                if not_attacker.get_current_HP() == 0:
                    done = True
                    logging.debug('{0} wins'.format(attacker.get_data()['name']))
                    winner = attacker.__str__()
            else:
                logging.debug('SKIP ATTACK: {0} has no attacks with damage points.'.format(attacker.__str__()))

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

    def multi_one_on_on_battle(self, num_battles):
        winners = []
        final_winner = ''
        for i in range(0, num_battles):
            winner = self.battle()
            winners.append(winner)
            self.card1.reset_HP()
            self.card2.reset_HP()
            pass
        card_ids_1_wins = winners.count(self.card1.__str__())
        card_ids_2_wins = winners.count(self.card2.__str__())

        if card_ids_1_wins > card_ids_2_wins:
            print('Winner: {0} [{1}]'.format(self.card1.__str__(), card_ids_1_wins / num_battles))
            final_winner = self.card1.__str__()
        elif card_ids_2_wins > card_ids_1_wins:
            print('Winner: {0} [{1}]'.format(self.card2.__str__(), card_ids_2_wins / num_battles))
            final_winner = self.card2.__str__()
        else:
            print('Draw: no winner.')
            final_winner = 'draw'

        return final_winner

    pass


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Pokemon Battle Simulator')
    parser.add_argument('-n', action="store", dest="num_battles", type=int, default=100, required=False)
    parser.add_argument('-c1', action="store", dest="card1_id", type=str, required=False)
    parser.add_argument('-c2', action="store", dest="card2_id", type=str, required=False)
    cmd_args = parser.parse_args()

    if (not cmd_args.card1_id) | (not cmd_args.card2_id):
        print('We are not given two cards to battle, so, we pick two random Pokemon cards.')
        card_ids = pick_two_random_pokemon()
    else:
        card_ids = [cmd_args.card1_id, cmd_args.card2_id]

    # run battle simulation a number of times, then see which wins more often, and what percent
    if len(card_ids) == 2:
        num_battles = cmd_args.num_battles
        sim = OneOnOneBattleSimulator(card_ids[0], card_ids[1])
        sim.multi_one_on_on_battle(num_battles)
    else:
        # it is not as interesting to battle same card
        print('Skip: both cards are the same.')

    return

if __name__ == "__main__":
    main()
