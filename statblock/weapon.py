from statblock.dice import Die
from statblock.dice import d4, d8
from statblock.base import VirtualGroup
from statblock.base import Component


class Attack(Component):

    def __init__(self, weapon):
        super(Attack, self).__init__()
        self.weapon = weapon


class MeleeAttack(Attack):
    
    def id(self):
        return self.weapon.id() + "/melee/attack"
    
    def declare_dependencies(self):
        self.affected_component_ids.add("BaseMeleeAttack")
        

class RangedAttack(Attack):
    
    def id(self):
        return self.weapon.id() + "/ranged/attack"
    
    def declare_dependencies(self):
        self.affected_component_ids.add("BaseRangedAttack")


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
    
    def id(self):
        return self.weapon.id() + "/melee/damage"
    
    def declare_dependencies(self):
        self.affected_component_ids.add("Strength")
    
    
class RangedDamage(Damage):
    
    def id(self):
        return self.weapon.id() + "/ranged/damage"
    

class CombatModifierGroup(VirtualGroup):
    
    def __init__(self):
        super(CombatModifierGroup, self).__init__()
        self._attack = None
        self._damage = None
        
    @property
    def attack(self):
        return self._attack
    
    @attack.setter
    def attack(self, new_value):
        self._attack = self.add(new_value)
        
    @property
    def damage(self):
        return self._damage
    
    @damage.setter
    def damage(self, new_value):
        self._damage = self.add(new_value)
        

class Weapon(VirtualGroup):
    
    def __init__(self):
        super(Weapon, self).__init__()
        self.melee = self.add(CombatModifierGroup())
        self.ranged = self.add(CombatModifierGroup())
        
    def is_ranged(self):
        return self.ranged.attack and self.ranged.damage
    
    def is_melee(self):
        return self.melee.attack and self.melee.damage
    

class Longsword(Weapon):
    
    def __init__(self):
        super(Longsword, self).__init__()
        self.melee.attack = MeleeAttack(self)
        self.melee.damage = MeleeDamage(self, d8)
        
    def id(self):
        return "weapon/longsword"
    
    
class Dagger(Weapon):
    
    def __init__(self):
        super(Dagger, self).__init__()
        self.melee.attack = MeleeAttack(self)
        self.melee.damage = MeleeDamage(self, d4)
        
        self.ranged.attack = RangedAttack(self)
        self.ranged.damage = RangedDamage(self, d4)
    
    def id(self):
        return "weapon/dagger"
    