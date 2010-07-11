from statblock.base import Component
from dice import d8
from statblock.dice import Die


class MeleeAttack(Component):
    
    def __init__(self, weapon):
        super(MeleeAttack, self).__init__()
        self.weapon = weapon
    
    def get_provider_id(self):
        return self.weapon.get_provider_id() + "/attack"
    
    def declare_dependencies(self):
        self.affected_by_component_ids.add("BaseMeleeAttack")


class MeleeDamage(Component):
    
    def __init__(self, default, weapon):
        super(MeleeDamage, self).__init__()
        self.default = default
        self.weapon = weapon
        
    def actual(self):
        return Die(self.default.number, self.default.multiplicator, self.default.modifier + self.value)
    
    def get_provider_id(self):
        return self.weapon.get_provider_id() + "/damage"
    
    def declare_dependencies(self):
        self.affected_by_component_ids.add("Strength")
        
    def roll(self):
        return self.actual().roll()
    

class Longsword(Component):
    
    def __init__(self):
        super(Longsword, self).__init__()
        self.attack = MeleeAttack(self)
        self.damage = MeleeDamage(d8, self)
        self.is_melee = True
        self.is_ranged = False
        self._group = [self.attack, self.damage]
    
    def get_provider_id(self):
        return "weapon/longsword"
    
    def declare_dependencies(self):
        pass
    
    def add(self):
        for member in self._group:
            self.bus.add(member)
    
    def wire(self):
        for member in self._group:
            member.wire()
    
    
    