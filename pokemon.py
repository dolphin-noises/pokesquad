from pokesquad import files


class Pokemon:
    # Parameters: name (string), type1 (pokemon.Type), type2 (pokemon.Type), ability (pokemon.Ability)
    def __init__(self, name, _id, type1=None, type2=None, ability=None):
        self.name = name
        self._id = _id
        self.type1 = type1
        self.type2 = type2
        self.ability = ability

    def get_name(self):
        return self.name

    def get_id(self):
        return self._id

    def get_type1(self):
        return self.type1

    def get_type2(self):
        return self.type2

    def get_ability(self):
        return self.ability

    def is_dual_type(self):
        if self.type2 is None:
            return False
        return True

    # Parameters: defender (pokemon.Pokemon) - Returns float array
    def attack(self, defender):
        attacks = [defender.defend(self.get_type1())]
        if self.is_dual_type():
            attacks.append(defender.defend(self.get_type2()))
        else:
            attacks.append(-1.0)
        return attacks

    # Parameters: attack_type (pokemon.Type) - Returns float
    def defend(self, attack_type):
        defense = self.type1.get_defense_against(attack_type)
        if self.is_dual_type():
            defense = defense * self.type2.get_defense_against(attack_type)
        if self.get_ability() is not None:
            defense = defense * self.get_ability().get_multiplier(attack_type.get_name())
        return defense


class Type:
    # Parameters: name (string), weak (string array), resist (string array), immune (string array)
    def __init__(self, name, weak=[], resist=[], immune=[]):
        self.name = name
        self.weak = weak
        self.resist = resist
        self.immune = immune

    def get_name(self):
        return self.name

    # Parameters: attacker (pokemon.Type) - Returns float
    def get_defense_against(self, attacker):
        if attacker.get_name() in self.weak:
            return 2.0
        elif attacker.get_name() in self.resist:
            return 0.5
        elif attacker.get_name() in self.immune:
            return 0.0
        else:
            return 1.0


class Types:
    def __init__(self):
        type_file_list = files.FileParser.parse('types.txt')
        self.types = {}
        for x in type_file_list:
            name = x[0]
            weak = x[1].split(',')
            resist = x[2].split(',')
            immune = x[3].split(',')
            self.types[name] = (Type(name=name, weak=weak, resist=resist, immune=immune))

    # Parameters: name (string) - Returns pokemon.Type
    def get_type(self, name):
        if name != '':
            return self.types[name]
        else:
            return None

    def get_types(self):
        return self.types;


class Ability:
    # Parameters: name (string), multipliers (float dict)
    def __init__(self, name, multipliers={}):
        self.name = name
        self.multipliers = multipliers

    def get_name(self):
        return self.name

    # Parameters: type_name (string) - Returns float
    def get_multiplier(self, type_name):
        if type_name in self.multipliers.keys():
            return self.multipliers[type_name]
        else:
            return 1.0


class Abilities:
    def __init__(self):
        ability_file_list = files.FileParser.parse('abilities.txt')
        self.abilities = {}
        for x in ability_file_list:
            name = x[0]
            multipliers = {}
            multipliers_list = x[1].split(',')
            for y in multipliers_list:
                multipliers_split = y.split(':')
                multipliers[multipliers_split[0]] = float(multipliers_split[1])
            self.abilities[name] = (Ability(name=name, multipliers=multipliers))

    # Parameters: name (string)
    def get_ability(self, name):
        if name != '':
            return self.abilities[name]
        else:
            return None
