class Weapon:
    def __init__(self,name,damage,damage_type,ranged=0,special=0):
        self.name = name
        self.damage = damage
        self.damage_type = damage_type
        if special!=0: self.special = special
        if ranged!=0:
            self.attack_range = ranged
        else:
            self.attack_range = 1


