from statblock.dice import Die
from statblock.dice import d4, d6, d8
from statblock.base import Component
from statblock.base import LinkBuilder
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

    def __init__(self, *args, **kwargs):
        super(Attack, self).__init__(*args, **kwargs)


class MeleeAttack(Attack):
    
    def __init__(self, weapon):
        super(MeleeAttack, self).__init__(weapon.id + "/melee/attack")
        LinkBuilder(self).is_modified_by("attack/melee")
        

class RangedAttack(Attack):
    
    def __init__(self, weapon):
        super(RangedAttack, self).__init__(weapon.id + "/ranged/attack")
        LinkBuilder(self).is_modified_by("attack/ranged")


class Damage(Component):
    
    def __init__(self, id, default, type):
        super(Damage, self).__init__(id)
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
    
    def __init__(self, weapon, default, type):
        super(MeleeDamage, self).__init__(weapon.id + "/melee/damage", default, type)
        LinkBuilder(self).is_modified_by("strength")

    
class RangedDamage(Damage):
    
    def __init__(self, weapon, default, type):
        super(RangedDamage, self).__init__(weapon.id + "/ranged/damage", default, type)
    

class CombatModifierGroup(object):
    
    def __init__(self, owner):
        self._attack = None
        self._damage = None
        
    @property
    def attack(self):
        return self._attack
    
    @attack.setter
    def attack(self, new_value):
        self._attack = new_value
        
    @property
    def damage(self):
        return self._damage
    
    @damage.setter
    def damage(self, new_value):
        self._damage = new_value
    

class Critical(Component):
    
    def __init__(self, weapon):
        super(Critical, self).__init__(weapon.id + "/critical")
        self.weapon = weapon
        self.range = [20]
        self.multiplier = 2
    
        
class Weapon(Component):
    
    def __init__(self, id):
        super(Weapon, self).__init__(id)
        self._melee = CombatModifierGroup(self)
        self._ranged = CombatModifierGroup(self)
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
    
    def __init__(self, id):
        super(MeleeWeapon, self).__init__(id)

    @property
    def damage(self):
        return self._melee.damage
    
    def set_damage(self, default_damage, type):
        attack = MeleeAttack(self)
        self._subcomponents.add(attack)
        self._melee.attack = attack
        
        damage = MeleeDamage(self, default_damage, type)
        self._subcomponents.add(damage)
        self._melee.damage = damage        

    def is_melee(self):
        return True
    
    
class RangedWeapon(Weapon):
    
    def __init__(self, id):
        super(RangedWeapon, self).__init__(id)
        self.increment = 10 # assumed default
    
    @property
    def damage(self):
        return self._ranged.damage
      
    def set_damage(self, default_damage, type):
        attack = RangedAttack(self)
        self._subcomponents.add(attack)
        self._ranged.attack = attack
        
        damage = RangedDamage(self, default_damage, type)
        self._subcomponents.add(damage)
        self._ranged.damage = damage        

    def is_ranged(self):
        return True
    
    
class CombinedWeapon(MeleeWeapon, RangedWeapon):
    
    def __init__(self, id):
        super(CombinedWeapon, self).__init__(id)
    
    @property
    def damage(self):
        return self._melee.damage 
    
    def set_damage(self, default_damage, type):
        MeleeWeapon.set_damage(self, default_damage, type)
        RangedWeapon.set_damage(self, default_damage, type)
        
        
# implementations

## they would need to add their 

class Longsword(MeleeWeapon):
    
    def __init__(self):
        super(Longsword, self).__init__("weapon/longsword")
        self.set_damage(d8, SLASHING)
        self.critical.range = [19, 20]
        self.weight = 4
        self.category = ONE_HANDED
        self.group = MARTIAL
        self.name = "Longsword"
    
    
class Dagger(CombinedWeapon):
    
    def __init__(self):
        super(Dagger, self).__init__("weapon/dagger")
        self.set_damage(d4, PIERCING)
        self.critical.range = [19, 20]
        self.increment = 10
        self.weight = 1
        self.category = LIGHT
        self.group = SIMPLE
        self.name = "Dagger"
    

class Javelin(RangedWeapon):
    
    def __init__(self):
        super(Javelin, self).__init__("weapon/javelin")
        self.set_damage(d6, PIERCING)
        self.increment = 30
        self.weight = 2
        self.category = RANGED
        self.group = SIMPLE
        self.name = "Javelin"
        
    
class Longbow(RangedWeapon):
    
    def __init__(self):
        super(Longbow, self).__init__("weapon/longbow")
        self.set_damage(d8, PIERCING)
        self.increment = 100
        self.weight = 3
        self.category = RANGED
        self.group = TWO_HANDED
        self.name = "Longbow"
