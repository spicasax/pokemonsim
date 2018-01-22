def normalize_damage(damage):
    damage = damage.replace('+', '')
    damage = damage.replace('-', '')
    damage = damage.replace('x', '')
    damage = damage.replace('×', '')
    damage = damage.replace('n/a', '')
    return damage