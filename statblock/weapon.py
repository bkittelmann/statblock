from statblock.dice import Die
from statblock.dice import d4, d6, d8
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
    
    @property
    def value(self):
        "The value of a damage is the combined dice roll with modifiers."
        return Die(
            self.default.number, 
            multiplicator=self.default.multiplicator, 
            modifier=self.default.modifier + self._calculate_modifiers()
        )
    
    def _calculate_modifiers(self):
        "Since value() is overridden, we need this method to sum up the modifiers."
        return reduce(lambda a, b: a + b.calculate(0), self.modifiers.values(), self.initial)
    

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
        self._melee = self.add(CombatModifierGroup())
        self._ranged = self.add(CombatModifierGroup())
      
    @property
    def melee(self):
        return self._melee
        
    @property
    def ranged(self):
        return self._ranged
        
    def is_ranged(self):
        return False
    
    def is_melee(self):
        return False
    
    
class MeleeWeapon(Weapon):
    
    def __init__(self):
        super(MeleeWeapon, self).__init__()
    
    def damage(self, default_damage):
        self._melee.attack = MeleeAttack(self)
        self._melee.damage = MeleeDamage(self, default_damage)        

    def is_melee(self):
        return True
    
    damage = property(fset=damage)
    
    
class RangedWeapon(Weapon):
    
    def __init__(self):
        super(RangedWeapon, self).__init__()
        
    def damage(self, default_damage):
        self._ranged.attack = RangedAttack(self)
        self._ranged.damage = RangedDamage(self, default_damage)        

    def is_ranged(self):
        return True
    
    damage = property(fset=damage)
    
    
class CombinedWeapon(MeleeWeapon, RangedWeapon):
    
    def __init__(self):
        super(CombinedWeapon, self).__init__()
    
    def damage(self, default_damage):
        MeleeWeapon.damage.fset(self, default_damage)
        RangedWeapon.damage.fset(self, default_damage)
        
    damage = property(fset=damage)

    
class Longsword(MeleeWeapon):
    
    def __init__(self):
        super(Longsword, self).__init__()
        self.damage = d8
        
    def id(self):
        return "weapon/longsword"
    
    
class Dagger(CombinedWeapon):
    
    def __init__(self):
        super(Dagger, self).__init__()
        self.damage = d4
    
    def id(self):
        return "weapon/dagger"
    

class Javelin(RangedWeapon):
    
    def __init__(self):
        super(Javelin, self).__init__()
        self.damage = d6
        
    def id(self):
        return "weapon/javelin"
    
    