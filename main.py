from typing import Optional, Any

from pokesquad import pokemon
from pokesquad import files

# pokemon.Type dict
types = pokemon.Types()
# pokemon.Ability dict
abilities = pokemon.Abilities()
# pokemon.Pokemon list
pokemon_list = []
# float dict
type_weight = {}
# float dict
pokemon_weight = {}

pokemon_file_list = files.FileParser.parse('pokemon.txt')

for x in range(0,len(pokemon_file_list)):
    pokemon_list.append(pokemon.Pokemon(name=pokemon_file_list[x][0],
                                        _id=x,
                                        type1=types.get_type(pokemon_file_list[x][1]),
                                        type2=types.get_type(pokemon_file_list[x][2]),
                                        ability=abilities.get_ability(pokemon_file_list[x][3])))


def calculate(offensive_weight=1.0,defensive_weight=1.0):
    if offensive_weight <= 0.0:
        print('\nDefense only:')
    elif defensive_weight <= 0.0:
        print('\nOffense only:')
    else:
        print('\nMixed:')
    for key in types.get_types().keys():
        type_weight[key] = defensive_weight
    for pk in pokemon_list:
        pokemon_weight[pk.get_name()] = offensive_weight
    for ra in range(0, 6):
        best_score = -200000.0
        best_pokemon = None
        for pk in pokemon_list:
            defense_score = 0.0
            offense_score = 0.0
            if defensive_weight > 0.0:
                for ty in types.get_types().values():
                    defense_score += pk.defend(ty) * type_weight[ty.get_name()]
                defense_score = 18 - defense_score
            if offensive_weight > 0.0:
                for mu in pokemon_list:
                    attacks = pk.attack(mu)
                    weighted_attacks = []
                    for at in attacks:
                        weighted_attacks.append(at * pokemon_weight[mu.get_name()])
                    if defensive_weight > 0.0:
                        counter_weight = defensive_weight
                        counter_attack = max(mu.attack(pk))
                        if 0 <= counter_attack < 0.25:
                            counter_weight *= 1.2
                        elif 0.25 <= counter_attack < 0.5:
                            counter_weight *= 1.2
                        elif 0.5 <= counter_attack < 1.0:
                            counter_weight *= 1.1
                        elif 1.0 <= counter_attack < 2.0:
                            counter_weight += 0.0
                        elif 2.0 <= counter_attack < 4.0:
                            counter_weight /= 2
                        elif counter_attack >= 4.0:
                            counter_weight /= 2.5
                        offense_score += max(weighted_attacks) * counter_weight
                    else:
                        offense_score += max(weighted_attacks)
                offense_score -= 69
            balanced_score = (defense_score * 2) + offense_score
            if balanced_score > best_score:
                best_score = balanced_score
                best_pokemon = pk
        print(best_pokemon.get_name())
        if defensive_weight > 0.0:
            for key, value in types.get_types().items():
                defense = best_pokemon.defend(value)
                if 0 <= defense < 0.25:
                    type_weight[key] /= 6.5
                elif 0.25 <= defense < 0.5:
                    type_weight[key] /= 6
                elif 0.5 <= defense < 1.0:
                    type_weight[key] /= 4
                elif 1.0 <= defense < 2.0:
                    type_weight[key] += 0
                elif 2.0 <= defense < 4.0:
                    type_weight[key] *= 4
                elif defense >= 4.0:
                    type_weight[key] *= 4.5
        if offensive_weight > 0.0:
            for mu in pokemon_list:
                key = mu.get_name()
                attack = max(best_pokemon.attack(mu))
                if attack >= 4.0:
                    pokemon_weight[key] /= 6.5
                elif 2.0 <= attack < 4.0:
                    pokemon_weight[key] /= 6
                elif 1.0 <= attack < 2.0:
                    pokemon_weight[key] += 0
                elif 0.5 <= attack < 1.0:
                    pokemon_weight[key] *= 1.5
                elif 0.25 <= attack < 0.5:
                    pokemon_weight[key] *= 2
                elif 0 <= attack < 0.25:
                    pokemon_weight[key] *= 2.5

calculate(1.0,0.0)
calculate(0.0,1.0)
calculate(1.0,1.0)
