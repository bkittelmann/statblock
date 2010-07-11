from statblock.dice import Die
from statblock.dice import d8
from statblock.base import AbstractComponent
from statblock.base import Component


class CombatModifierGroup(AbstractComponent):
    
    def __init__(self):
        super(CombatModifierGroup, self).__init__()
        self._attack = None
        self._damage = None
        self._group = [self._attack, self._damage]
        
    def add(self):
        for member in [m for m in self._group if m]:
            self.bus.add(member)
    
    def wire(self):
        for member in [m for m in self._group if m]:
            member.wire()
            
    def register(self, other):
        other.bus = self.bus
        return other
                    
    @property
    def attack(self):
        return self._attack
    
    @attack.setter
    def attack(self, new_value):
        self._attack = self.register(new_value)
        
    @property
    def damage(self):
        return self._damage
    
    @damage.setter
    def damage(self, new_value):
        self._damage = self.register(new_value)


class MeleeAttack(Component):
    
    def __init__(self, weapon):
        super(MeleeAttack, self).__init__()
        self.weapon = weapon
    
    def get_provider_id(self):
        return self.weapon.get_provider_id() + "/attack"
    
    def declare_dependencies(self):
        self.affected_by_component_ids.add("BaseMeleeAttack")


class MeleeDamage(Component):
    
    def __init__(self, weapon, default):
        super(MeleeDamage, self).__init__()
        self.weapon = weapon
        self.default = default
        
    def get_combined(self):
        return Die(
            self.default.number, 
            multiplicator=self.default.multiplicator, 
            modifier=self.default.modifier + self.value
        )
    
    def get_provider_id(self):
        return self.weapon.get_provider_id() + "/damage"
    
    def declare_dependencies(self):
        self.affected_by_component_ids.add("Strength")
        
    def roll(self):
        return self.get_combined().roll()
    

class Longsword(Component):
    
    def __init__(self):
        super(Longsword, self).__init__()
        self.melee = CombatModifierGroup()
        self.melee.attack = MeleeAttack(self)
        self.melee.damage = MeleeDamage(self, d8)

        self.is_melee = True
        self.is_ranged = False
        self._group = [self.melee.attack, self.melee.damage]
    
    def get_provider_id(self):
        return "weapon/longsword"
    
    def add(self):
        for member in self._group:
            self.bus.add(member)
            member.add()
    
    def wire(self):
        for member in self._group:
            member.wire()
    
    
    