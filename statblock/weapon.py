from statblock.dice import Die
from statblock.dice import d4, d6, d8
from statblock.base import VirtualGroup
from statblock.base import Component
from statblock.base import calculate_modifier_sum

#--- some constants about damage types --------------------------------
PIERCING    = "piercing"
BLUDGEONING = "bludgeoning"
SLASHING    = "slashing"

            
#--- some constants regarding a weapon's category ---------------------
        
RANGED     = "ranged"
UNARMED    = "unarmed"
LIGHT      = "light-melee"
ONE_HANDED = "one-handed"
TWO_HANDED = "two-handed" 

    
#--- some constants regarding a weapon's group ------------------------
    
SIMPLE  = "simple"
MARTIAL = "martial"
EXOTIC  = "exotic"


class Attack(Component):

    def __init__(self, weapon):
        super(Attack, self).__init__()
        self.weapon = weapon


class MeleeAttack(Attack):
    
    def id(self):
        return self.weapon.id() + "/melee/attack"
    
    def declare_dependencies(self):
        self.affected_component_ids.add("attack/melee")
        

class RangedAttack(Attack):
    
    def id(self):
        return self.weapon.id() + "/ranged/attack"
    
    def declare_dependencies(self):
        self.affected_component_ids.add("attack/ranged")


class Damage(Component):
    
    def __init__(self, weapon, default, type):
        super(Damage, self).__init__()
        self.weapon = weapon
        self.default = default
        self.type = type
    
    @property
    def value(self):
        "The value of a damage is the combined dice roll with modifiers."
        return Die(
            self.default.number, 
            multiplicator=self.default.multiplicator, 
            modifier=self.default.modifier + calculate_modifier_sum(self._modifiers)
        )


class MeleeDamage(Damage):
    
    def id(self):
        return self.weapon.id() + "/melee/damage"
    
    def declare_dependencies(self):
        self.affected_component_ids.add("strength")
    
    
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
    

class Critical(Component):
    
    def __init__(self, weapon):
        super(Critical, self).__init__()
        self.weapon = weapon
        self.range = [20]
        self.multiplier = 2
    
    def id(self):
        return self.weapon.id() + "critical"
            
        
class Weapon(VirtualGroup):
    
    def __init__(self):
        super(Weapon, self).__init__()
        self._melee = self.add(CombatModifierGroup())
        self._ranged = self.add(CombatModifierGroup())
        self.critical = Critical(self)
        self.weight = 0
        self.size = "M" # weaponSize as a component?
        self.group = None
        self.category = None
        self.name = ""
      
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

    @property
    def damage(self):
        return self._melee.damage
    
    def set_damage(self, default_damage, type):
        self._melee.attack = MeleeAttack(self)
        self._melee.damage = MeleeDamage(self, default_damage, type)        

    def is_melee(self):
        return True
    
    
class RangedWeapon(Weapon):
    
    def __init__(self):
        super(RangedWeapon, self).__init__()
        self.increment = 10 # assumed default
    
    @property
    def damage(self):
        return self._ranged.damage
      
    def set_damage(self, default_damage, type):
        self._ranged.attack = RangedAttack(self)
        self._ranged.damage = RangedDamage(self, default_damage, type)        

    def is_ranged(self):
        return True
    
#    damage = property(fset=damage)
    
    
class CombinedWeapon(MeleeWeapon, RangedWeapon):
    
    def __init__(self):
        super(CombinedWeapon, self).__init__()
    
    @property
    def damage(self):
        return self._melee.damage 
    
    def set_damage(self, default_damage, type):
        MeleeWeapon.set_damage(self, default_damage, type)
        RangedWeapon.set_damage(self, default_damage, type)
        
        
# implementations
    
class Longsword(MeleeWeapon):
    
    def __init__(self):
        super(Longsword, self).__init__()
        self.set_damage(d8, SLASHING)
        self.critical.range = [19, 20]
        self.weight = 4
        self.category = ONE_HANDED
        self.group = MARTIAL
        self.name = "Longsword"
        
    def id(self):
        return "weapon/longsword"
    
    
class Dagger(CombinedWeapon):
    
    def __init__(self):
        super(Dagger, self).__init__()
        self.set_damage(d4, PIERCING)
        self.critical.range = [19, 20]
        self.increment = 10
        self.weight = 1
        self.category = LIGHT
        self.group = SIMPLE
        self.name = "Dagger"
    
    def id(self):
        return "weapon/dagger"
    

class Javelin(RangedWeapon):
    
    def __init__(self):
        super(Javelin, self).__init__()
        self.set_damage(d6, PIERCING)
        self.increment = 30
        self.weight = 2
        self.category = RANGED
        self.group = SIMPLE
        self.name = "Javelin"
        
    def id(self):
        return "weapon/javelin"
    
    
class Longbow(RangedWeapon):
    
    def __init__(self):
        super(Longbow, self).__init__()
        self.set_damage(d8, PIERCING)
        self.increment = 100
        self.weight = 3
        self.category = RANGED
        self.group = TWO_HANDED
        self.name = "Longbow"
        
    def id(self):
        return "weapon/longbow"    
    
    