class Weapon:
    def __init__(self,name,ranged=0):
        self.name = name
        if ranged!=0:
            self.attack_range = ranged
        else:
            self.attack_range = 1


