# coding=utf-8
from pymongo import MongoClient
import csv
import os
import sys
THIS_PATH = os.getcwd()
PARENT_PATH  = os.path.dirname(THIS_PATH)
GAME_DIR = os.path.join(PARENT_PATH, 'game')

sys.path.insert(0,GAME_DIR)

from card_helper import normalize_damage

THIS_PATH = os.getcwd()
PARENT_PATH  = os.path.dirname(THIS_PATH)
DATA_DIR = os.path.join(PARENT_PATH, 'data_extract')

client = MongoClient()
db = client.pokemontcg

with open(os.path.join(DATA_DIR,'cards_by_subtype.csv'),'w') as f:
    writer = csv.writer(f, delimiter=',')
    row = ['ID','Name','HP','RetreatCostCount',
           'AttackCount', 'AttackConvertedEnergyCostTotal',
           'WeaknessTotal', 'ResistanceTotal', 'Ability', 'Subtype', 'Types', 'StrongestDamage']
    writer.writerow(row)

    for card in db.cards.find({'supertype': 'Pokémon'}):
        id = ''
        name = ''
        hp = ''
        subtype = ''
        types = []
        retreat_cost_count = 0
        attack_count = 0
        attack_converted_energy_cost_total = 0
        weakness_total = ''
        resistance_total = ''
        ability = 0
        strongest_damage = 0
        if 'id' in card: id = card['id']
        if 'name' in card: name = card['name']
        if 'hp' in card: hp = card['hp']
        if 'subtype' in card: subtype = card['subtype']
        if 'retreatCost' in card: retreat_cost_count = len(card['retreatCost'])
        if 'attacks' in card: attack_count = len(card['attacks'])
        if 'attacks' in card:
            for attack in card['attacks']:
                if 'damage' in attack:
                    attack_damage = normalize_damage(attack['damage'])
                    if int(attack_damage) > strongest_damage:
                        strongest_damage = int(attack_damage)
                    attack_converted_energy_cost_total += attack['convertedEnergyCost']
        if 'weaknesses' in card:
            for weakness in card['weaknesses']:
                weakness_total = weakness['value']
        if 'resistances' in card:
            for res in card['resistances']:
                resistance_total = res['value']
        if 'ability' in card: ability = 1
        if 'types' in card:
            types = card['types']


        row = [id, name, hp, retreat_cost_count, attack_count, attack_converted_energy_cost_total,
               weakness_total, resistance_total, ability, subtype, types, strongest_damage]
        writer.writerow(row)