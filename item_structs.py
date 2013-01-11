class Weapon:
    def __init__(self,name,damage,damage_type,ranged=0,special=0):
        self.name = name
        self.stats = self.name+' Damage: '
        self.damage = damage
        self.stats = self.stats+str(damage)
        self.stats = self.stats+' Type: '
        self.damage_type = damage_type
        if self.damage_type=='p':
            self.stats = self.stats+'Piercing'
        if self.damage_type=='s':
            self.stats = self.stats+'Slashing'
        if self.damage_type=='b':
            self.stats = self.stats+'Bludgeoning'

        self.stats = self.stats+' Range: '
        if ranged!=0:
            self.attack_range = ranged
            self.stats = self.stats +str(ranged[0])+'-'+str(ranged[1])
        else:
            self.attack_range = 1
            self.stats = self.stats + 'Melee'
        if special!=0: self.special = special

