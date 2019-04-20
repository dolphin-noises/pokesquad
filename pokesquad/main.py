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
matchup_weight = {}

pokemon_file_list = files.FileParser.parse('pokemon.txt')

for x in range(0,len(pokemon_file_list)):
    pokemon_list.append(pokemon.Pokemon(name=pokemon_file_list[x][0],
                                        _id=x,
                                        type1=types.get_type(pokemon_file_list[x][1]),
                                        type2=types.get_type(pokemon_file_list[x][2]),
                                        ability=abilities.get_ability(pokemon_file_list[x][3])))


def calculate(attack_weight=1.0,defense_weight=1.0):
    # Initialize weights
    for key in types.get_types().keys():
        type_weight[key] = 1.0
    for mu in pokemon_list:
        matchup_weight[mu.get_name()] = 1.0

    for ra in range(0, 6):
        best_score = 0.0
        best_pokemon = None

        for pk in pokemon_list:
            defense_score = 0.0
            attack_score = 0.0

            # Calculate the defense score against all types
            for ty in types.get_types().values():
                defense_score += (36 - pk.defend(ty)) * type_weight[ty.get_name()]

            # Calculate the offense against all matchups
            for mu in pokemon_list:
                attack_score += pk.attack(mu) * matchup_weight[mu.get_name()]
                attack_score -= (mu.attack(pk) / 2) * defense_weight * matchup_weight[mu.get_name()]

            # Calculate the full score
            balanced_defense = defense_score * defense_weight
            balanced_attack = attack_score * attack_weight
            balanced_score = balanced_defense + balanced_attack

            # Is this the best score?
            if balanced_score > best_score:
                best_score = balanced_score
                best_pokemon = pk

        # Print the Pokemon with the best score
        print(best_pokemon.get_name())

        # Weigh the types and Pokemon for the next run
        for key, value in types.get_types().items():
            defense = best_pokemon.defend(value)
            type_weight[key] *= pokemon.Weights.get_type_weight(defense)
        for mu in pokemon_list:
            attack = best_pokemon.attack(mu)
            matchup_weight[mu.get_name()] *= pokemon.Weights.get_matchup_weight(attack)


calculate(attack_weight=1.0,defense_weight=0.0)
print('\n')
calculate(attack_weight=0.0,defense_weight=1.0)
print('\n')
calculate(attack_weight=1.0,defense_weight=1.0)
