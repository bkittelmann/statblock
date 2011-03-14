from statblock.skill import SkillsGroup
from statblock.dice import d8
import re

from statblock.base import VirtualGroup, Component, Modifier, Bonus
from statblock.base import ComponentProxy
from statblock.ability import Strength, Dexterity, Constitution, Intelligence, Wisdom, Charisma
from statblock.armor import NaturalArmor
from statblock.base import ModifyOtherAction

class ValueModifier(Modifier):
    
    def __init__(self, source):
        Modifier.__init__(self, Bonus.UNTYPED, source.value, source)
        
    @property
    def value(self):
        return self.source.value  


class SizeAttackModifier(Modifier):
    
    def __init__(self, source):
        Modifier.__init__(self, Bonus.SIZE, source.value, source)
        
    @property
    def value(self):
        return self.source.attack
    

class SizeGrappleModifier(Modifier):

    def __init__(self, source):
        Modifier.__init__(self, Bonus.SIZE, source.value, source)
        
    @property
    def value(self):
        # for grappling a size attack bonus does not count, we invert it
        inverted_malus = (self.source.attack * -1)
        return inverted_malus + self.source.grapple


class _Size(Component):
    
    def __init__(self, name, attack, grapple):
        super(_Size, self).__init__()
        self.name = name
        self.attack = attack
        self.grapple = grapple
        self.bonus = SizeAttackModifier(self)
        
    def declare_dependencies(self):
        self.modified_component_ids = set(["attack/base", "armor-class"])
        self.registry.add_action(ModifyOtherAction(self, "attack/grapple", bonus=SizeGrappleModifier(self)))
    
    def id(self):
        return "size"
    
    def is_destroyable(self):
        return True
            
    def __str__(self):
        return self.name
            
    def __repr__(self):
        return "<Size.%s>" % self.name
    

class Size(object):
    FINE       = _Size("Fine", +8, -16)
    DIMINUTIVE = _Size("Diminutive", +4, -12)
    TINY       = _Size("Fine", +2, -8)
    SMALL      = _Size("Small", +1, -4)
    MEDIUM     = _Size("Medium", 0, 0)
    LARGE      = _Size("Large", -1, +4)
    HUGE       = _Size("Huge", -2, + 8)
    GARGANTUAN = _Size("Gargantuan", -4, +12)
    COLLOSAL   = _Size("Collossal", -8, +16)


class _Alignment(object):
    
    def __init__(self, name):
        self.long_name = name
        self.short_name = re.sub("[a-z ]", "", name)
        
    def __str__(self):
        return self.short_name
    

class Alignment(object):
    LG = _Alignment("Lawful Good")
    LN = _Alignment("Lawful Neutral")
    LE = _Alignment("Lawful Evil")
    NG = _Alignment("Neutral Good")
    N  = _Alignment("Neutral")
    NE = _Alignment("Neutral Evil")
    CG = _Alignment("Chaotic Good")
    CN = _Alignment("Chaotic Neutral")
    CE = _Alignment("Chaotic Evil")
    

class Fortitude(Component):
    
    def id(self):
        return "fortitude"
    
    def is_destroyable(self):
        return False


class Reflex(Component):
    
    def id(self):
        return "reflex"
    
    def is_destroyable(self):
        return False
    

class Will(Component):
    
    def id(self):
        return "will"

    def is_destroyable(self):
        return False
    

class SavingThrowGroup(VirtualGroup):
    
    def __init__(self):
        super(SavingThrowGroup, self).__init__()
        self._fortitude = self.add(Fortitude(0))
        self._reflex = self.add(Reflex(0))
        self._will = self.add(Will(0))
    
    @property
    def fortitude(self):
        return self._fortitude

    @fortitude.setter
    def fortitude(self, new_value):
        self._fortitude.value = new_value
        
    @property
    def reflex(self):
        return self._reflex

    @reflex.setter
    def reflex(self, new_value):
        self._reflex.value = new_value
        
    @property
    def will(self):
        return self._will

    @will.setter
    def will(self, new_value):
        self._will.value = new_value
        
    def __repr__(self):
        return "<SavingThrows>"


class AbilityGroup(VirtualGroup):
    
    def __init__(self):
        super(AbilityGroup, self).__init__()
        
        self._strength     = self.add(Strength(10))
        self._dexterity    = self.add(Dexterity(10))
        self._constitution = self.add(Constitution(10))
        self._intelligence = self.add(Intelligence(10))
        self._wisdom       = self.add(Wisdom(10))
        self._charisma     = self.add(Charisma(10))

    @property
    def strength(self):
        return self._strength    
    
    @strength.setter
    def strength(self, new_value):
        self._strength.value = new_value
        
    @property
    def dexterity(self):
        return self._dexterity    
    
    @dexterity.setter
    def dexterity(self, new_value):
        self._dexterity.value = new_value
        
    @property
    def constitution(self):
        return self._constitution    
    
    @constitution.setter
    def constitution(self, new_value):
        self._constitution.value = new_value
        
    @property
    def intelligence(self):
        return self._intelligence    
    
    @intelligence.setter
    def intelligence(self, new_value):
        self._intelligence.value = new_value
        
    @property
    def wisdom(self):
        return self._wisdom    
    
    @wisdom.setter
    def wisdom(self, new_value):
        self._wisdom.value = new_value
        
    @property
    def charisma(self):
        return self._charisma    
    
    @charisma.setter
    def charisma(self, new_value):
        self._charisma.value = new_value
        

class HitPoints(Component):
    
    def id(self):
        return "hit-points"     

    def is_destroyable(self):
        return False
    
    
class Initiative(Component):
    
    def id(self):
        return "initiative"

    def is_destroyable(self):
        return False

    def __repr__(self):
        return "Initiative: %s" % self.value


class BaseAttack(Component):
    
    def __init__(self, *args, **kwargs):
        super(BaseAttack, self).__init__(*args, **kwargs)
        self.bonus = ValueModifier(self)
    
    def id(self):
        return "attack/base"
    
    def is_destroyable(self):
        return False
    
    def declare_dependencies(self):
        self.modified_component_ids.add("attack/melee")
        self.modified_component_ids.add("attack/ranged")

    
class AttackModifierGroup(object):
    
    def __init__(self):
        self.base = None
        self.melee = None
        self.ranged = None
        self.grapple = None
    

class BaseMeleeAttack(Component):
    
    def __init__(self, *args, **kwargs):
        super(BaseMeleeAttack, self).__init__(*args, **kwargs)
        self.bonus = ValueModifier(self)
    
    def id(self):
        return "attack/melee"   

    def is_destroyable(self):
        return False
    

class BaseRangedAttack(Component):
    
    def __init__(self, *args, **kwargs):
        super(BaseRangedAttack, self).__init__(*args, **kwargs)
        self.bonus = ValueModifier(self)
    
    def id(self):
        return "attack/ranged"

    def is_destroyable(self):
        return False
    

class GrappleAttack(Component):
    
    def __init__(self, *args, **kwargs):
        super(GrappleAttack, self).__init__(*args, **kwargs)
        self.bonus = ValueModifier(self)
    
    def id(self):
        return "attack/grapple"

    def is_destroyable(self):
        return False
    
    def declare_dependencies(self):
        self.affected_component_ids.add("attack/base")
        self.affected_component_ids.add("strength")

    
class ArmorClass(Component):
    
    def id(self):
        return "armor-class"

    def is_destroyable(self):
        return False
    
    
class FlatFooted(Component):
    
    def id(self):
        return "flat-footed"

    def is_destroyable(self):
        return False
    
    @property
    def value(self):
        self.initial = self._filter_modifiers()
        return Component.value.fget(self)
        
    def _filter_modifiers(self):
        ac = self.registry.get("armor-class")
        dex = self.registry.get("dexterity")

        def is_not_dex(m):
            return m.source is not dex
        
        def without_dex(a, b):
            return a + b.calculate(0, ignore_func=is_not_dex)
        
        return reduce(without_dex, ac.modifiers.values(), 10)
    
    
class Touch(Component):
    
    def id(self):
        return "touch"

    def is_destroyable(self):
        return False
    
    @property
    def value(self):
        self.initial = self._filter_modifiers()
        return Component.value.fget(self)
        
    def _filter_modifiers(self):
        ac = self.registry.get("armor-class")
        
        def no_armor(m):
            return m.type not in (Bonus.ARMOR, Bonus.SHIELD, Bonus.NATURAL_ARMOR)
        
        def without_armor(a, b):
            return a + b.calculate(0, ignore_func=no_armor)
        
        return reduce(without_armor, ac.modifiers.values(), 10)


class MonsterType(object):
    
    def __init__(self, name, type, subtypes=None):
        self.name = name
        self.type = type
        self.subtypes = subtypes or []
        
        
class MeleeAttackCombination(object):
    
    def __init__(self, weapon):
        self.weapons = [weapon]


class RangedAttackCombination(object):
    
    def __init__(self, weapon):
        self.weapons = [weapon]


class Character(VirtualGroup):
    
    def __init__(self):
        super(Character, self).__init__()
        
        self.name = "Tordek"
        self.type_info = MonsterType("Human", type="Humanoid", subtypes=["Human"])
        self.gender = "Male"
        self.level = "Warrior 1"
        
        self.hit_points = self.add(HitPoints(initial=8))
        self.hit_dice = d8
        self.initiative = self.add(Initiative(0))
        self.alignment = Alignment.LG
        self.speed = 30
        self._size = self.add(Size.MEDIUM)

        self.abilities = self.add(AbilityGroup())
        self.saving_throws = self.add(SavingThrowGroup())
        self.armor_class = self.add(ArmorClass(10))
        
        self.attack = AttackModifierGroup()
        self.attack.base = self.add(BaseAttack(0))
        self.attack.melee = self.add(BaseMeleeAttack(0))
        self.attack.ranged = self.add(BaseRangedAttack(0))
        self.attack.grapple = self.add(GrappleAttack(0))
        self.weapons = self.add(VirtualGroup())
        
        self.melee = []
        self.ranged = []
    
        self._armor = self.add(ComponentProxy("armor"))
        self._shield = self.add(ComponentProxy("shield"))
        self.natural_armor = self.add(NaturalArmor())
        self.flat_footed = self.add(FlatFooted())
        self.touch = self.add(Touch())
        
        self.skills = self.add(SkillsGroup())
        self.feats = self.add(VirtualGroup())
        self.languages = ["Common"]
        

    @property
    def size(self):
        return self._size
        
    @size.setter
    def size(self, new_size):
        self._size = self.add(new_size)
        
    @property
    def armor(self):
        return self._armor
    
    @armor.setter
    def armor(self, new_armor):
        self._armor.add(new_armor)
    
    @property
    def shield(self):
        return self._shield
    
    @shield.setter
    def shield(self, new_shield):
        self._shield.add(new_shield)
        
    def __repr__(self):
        return "<Character>"
        
