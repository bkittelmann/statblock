from statblock.dice import Die
from statblock.dice import d4, d8
from statblock.base import AbstractComponent
from statblock.base import Component


class Attack(Component):

    def __init__(self, weapon):
        super(Attack, self).__init__()
        self.weapon = weapon


class MeleeAttack(Attack):
    
    def get_provider_id(self):
        return self.weapon.get_provider_id() + "/melee/attack"
    
    def declare_dependencies(self):
        self.affected_by_component_ids.add("BaseMeleeAttack")
        

class RangedAttack(Attack):
    
    def get_provider_id(self):
        return self.weapon.get_provider_id() + "/ranged/attack"
    
    def declare_dependencies(self):
        self.affected_by_component_ids.add("BaseRangedAttack")


class Damage(Component):
    
    def __init__(self, weapon, default):
        super(Damage, self).__init__()
        self.weapon = weapon
        self.default = default
    
    def get_combined(self):
        return Die(
            self.default.number, 
            multiplicator=self.default.multiplicator, 
            modifier=self.default.modifier + self.value
        )
    
    def roll(self):
        return self.get_combined().roll()
    

class MeleeDamage(Damage):
    
    def get_provider_id(self):
        return self.weapon.get_provider_id() + "/melee/damage"
    
    def declare_dependencies(self):
        self.affected_by_component_ids.add("Strength")
    
    
class RangedDamage(Damage):
    
    def get_provider_id(self):
        return self.weapon.get_provider_id() + "/ranged/damage"
    

class CombatModifierGroup(AbstractComponent):
    
    def __init__(self):
        super(CombatModifierGroup, self).__init__()
        self._attack = None
        self._damage = None
        
    def add(self, bus):
        if self._attack and self._damage:
            bus.add(self._attack)
            bus.add(self._damage)
    
    def wire(self):
        if self._attack and self._damage:
            self._attack.wire()
            self._damage.wire()
            
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
        

class Weapon(Component):
    
    def __init__(self):
        super(Weapon, self).__init__()
        self.melee = CombatModifierGroup()
        self.ranged = CombatModifierGroup()
        
    def add(self):
        self.melee.add(self.bus)
        self.ranged.add(self.bus)
        
    def wire(self):
        self.melee.wire()
        self.ranged.wire()
        
    def is_ranged(self):
        return self.ranged.attack and self.ranged.damage
    
    def is_melee(self):
        return self.melee.attack and self.melee.damage
    

class Longsword(Weapon):
    
    def __init__(self):
        super(Longsword, self).__init__()
        self.melee.attack = MeleeAttack(self)
        self.melee.damage = MeleeDamage(self, d8)
        
    def get_provider_id(self):
        return "weapon/longsword"
    
    
class Dagger(Weapon):
    
    def __init__(self):
        super(Dagger, self).__init__()
        self.melee.attack = MeleeAttack(self)
        self.melee.damage = MeleeDamage(self, d4)
        
        self.ranged.attack = RangedAttack(self)
        self.ranged.damage = RangedDamage(self, d4)
    
    def get_provider_id(self):
        return "weapon/dagger"
    