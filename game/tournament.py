from simulator import OneOnOneBattleSimulator
from random import shuffle
from pymongo import MongoClient
import pprint


client = MongoClient()
db = client.pokemontcg

candidates = []
for card in db.cards.aggregate([
        {'$match':  {"supertype": "Pokémon"}},
      ]):
    candidates.append(card['id'])

# for debugging:

# candidates = ['xy7-1', 'xy7-2', 'xy7-3', 'xy7-4', 'xy7-5', 'xy7-6', 'xy7-7', 'xy7-8','xy7-9','xy7-10',
#              'xy7-11','xy7-12','xy7-13','xy7-14','xy7-15',]
# candidates = ['sm35-28', 'ex10-K', 'ex10-42', 'ex1-48', 'neo4-39', 'ex2-6']

shuffle(candidates)

while len(candidates) > 1:
    print("\ncandidates: {0}".format(candidates))
    winners = []
    pairs = []
    if len(candidates) % 2 == 1:
        candidates.append(None)
    for i in range(0, len(candidates), 2):
        pairs.append((candidates[i], candidates[i + 1],))

    for p in pairs:
        print("Match: {0}".format(p))
        if p[1] is not None:
            sim = OneOnOneBattleSimulator(p[0], p[1])
            winner = sim.multi_one_on_on_battle(100)
            if winner == 'draw':
                winners.append(p[0])
                winners.append(p[1])
                pass
            else:
                winners.append(winner)
        else:
            winners.append(p[0])
            print('Bye: {0}'.format(p[0]))
        pass

    candidates = winners

# TODO: add stats on number of candidates in each round
# TODO: add indicator or counter for number of rounds