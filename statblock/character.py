from statblock.ability import Charisma
from statblock.ability import Constitution
from statblock.ability import Dexterity
from statblock.ability import Intelligence
from statblock.ability import Strength
from statblock.ability import Wisdom

from statblock.armor import NaturalArmor

from statblock.base import Actor
from statblock.base import ArmorModifier
from statblock.base import Component
from statblock.base import LinkBuilder
from statblock.base import Modifier
from statblock.base import NaturalArmorModifier
from statblock.base import ShieldModifier
from statblock.base import SizeModifier
from statblock.base import ValueModifier
from statblock.base import calculate_modifier_sum

from statblock.skill import get_all_skill_classes
from statblock.skill import Craft
from statblock.skill import Perform
from statblock.skill import Profession


class Fortitude(Component):
    
    def __init__(self, initial=0):
        super(Fortitude, self).__init__("fortitude", initial)
    
    def is_destroyable(self):
        return False
    

class Reflex(Component):
    
    def __init__(self, initial=0):
        super(Reflex, self).__init__("reflex", initial)
    
    def is_destroyable(self):
        return False


class Will(Component):
    
    def __init__(self, initial=0):
        super(Will, self).__init__("will", initial)
    
    def is_destroyable(self):
        return False
    
    
class HitPoints(Component):
    
    def __init__(self, initial=0):
        super(HitPoints, self).__init__("hit-points", initial)     

    def is_destroyable(self):
        return False
    
    
class Initiative(Component):
    
    def __init__(self, initial=0):
        super(Initiative, self).__init__("initiative", initial)     

    def is_destroyable(self):
        return False

    def __repr__(self):
        return "Initiative: %s" % self.value


class SizeAttackModifier(Modifier):
    stackable = True
    
    def __init__(self, source):
        Modifier.__init__(self, source.value, source)
        
    @property
    def value(self):
        return self.source.attack
    

class SizeGrappleModifier(SizeModifier):

    def __init__(self, source):
        Modifier.__init__(self, source.value, source)
        
    @property
    def value(self):
        # for grappling a size attack bonus does not count, we invert it
        inverted_malus = (self.source.attack * -1)
        return inverted_malus + self.source.grapple
    

class _Size(Component):
    
    def __init__(self, name, attack, grapple):
        super(_Size, self).__init__("size")
        self.name = name
        self.attack = attack
        self.grapple = grapple
        self._default_bonus = SizeAttackModifier(self)
        lb = LinkBuilder(self)
        lb.modifies("attack/base", "armor-class")
        lb.modifies("attack/grapple", bonus=SizeGrappleModifier(self))                                                              
    
    def is_destroyable(self):
        return True
            
    def is_modifiable(self):
        return False
            
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


class BaseAttack(Component):
    
    def __init__(self, *args, **kwargs):
        super(BaseAttack, self).__init__("attack/base", *args, **kwargs)
        self._default_bonus = ValueModifier(self)
        LinkBuilder(self).modifies("attack/melee", "attack/ranged")
    
    def is_destroyable(self):
        return False
    
    
class AttackModifierGroup(object):
    
    def __init__(self):
        self.base = None
        self.melee = None
        self.ranged = None
        self.grapple = None
    

class BaseMeleeAttack(Component):
    
    def __init__(self, *args, **kwargs):
        super(BaseMeleeAttack, self).__init__("attack/melee", *args, **kwargs)
        self._default_bonus = ValueModifier(self)

    def is_destroyable(self):
        return False
    

class BaseRangedAttack(Component):
    
    def __init__(self, *args, **kwargs):
        super(BaseRangedAttack, self).__init__("attack/ranged", *args, **kwargs)
        self._default_bonus = ValueModifier(self)

    def is_destroyable(self):
        return False
    

class GrappleAttack(Component):
    
    def __init__(self, *args, **kwargs):
        super(GrappleAttack, self).__init__("attack/grapple", *args, **kwargs)
        self._default_bonus = ValueModifier(self)
        LinkBuilder(self).is_modified_by("attack/base", "strength")

    def is_destroyable(self):
        return False


class ArmorClass(Component):
    
    def __init__(self, initial=10):
        super(ArmorClass, self).__init__("armor-class", initial=initial) 

    def is_destroyable(self):
        return False
    
    
class FlatFooted(Component):
    
    def __init__(self):
        super(FlatFooted, self).__init__("flat-footed", initial=10)
        LinkBuilder(self).uses_all_from("armor-class")

    def is_destroyable(self):
        return False
    
    @property
    def value(self):
        mods = [m for m in self._modifiers if m.source.id is not "dexterity"]
        return self._initial + calculate_modifier_sum(mods)
    
    
class Touch(Component):
    
    def __init__(self):
        super(Touch, self).__init__("touch", initial=10) 
        LinkBuilder(self).uses_all_from("armor-class")

    def is_destroyable(self):
        return False
    
    @property
    def value(self):
        mods = filter(self._no_armor, self._modifiers)
        return self._initial + calculate_modifier_sum(mods)
       
    def _no_armor(self, m):
        return type(m) not in set([
           ArmorModifier, 
           NaturalArmorModifier, 
           ShieldModifier
        ])


class MeleeAttackCombination(object):
    
    def __init__(self, weapon):
        self.weapons = [weapon]


class RangedAttackCombination(object):
    
    def __init__(self, weapon):
        self.weapons = [weapon]


class Character(Actor):

    def __init__(self, ability_default=10):
        super(Character, self).__init__()
        
        # adding abilities
        self.registry.set(Strength(ability_default))
        self.registry.set(Dexterity(ability_default))
        self.registry.set(Constitution(ability_default))
        self.registry.set(Intelligence(ability_default))
        self.registry.set(Wisdom(ability_default))
        self.registry.set(Charisma(ability_default))
        
        # adding saving throws
        self.registry.set(Fortitude())
        self.registry.set(Reflex())
        self.registry.set(Will())
        
        # basic stuff
        self.registry.set(HitPoints(8))
        self.registry.set(Initiative())
        self.registry.set(Size.MEDIUM)
        
        # attacks
        self.attack = AttackModifierGroup()
        self.attack.base = self.registry.set(BaseAttack(0))
        self.attack.melee = self.registry.set(BaseMeleeAttack(0))
        self.attack.ranged = self.registry.set(BaseRangedAttack(0))
        self.attack.grapple = self.registry.set(GrappleAttack(0))
        
        # armor
        self.registry.set(ArmorClass(10))
        self.registry.set(NaturalArmor(0))
        self.registry.set(Touch())
        self.registry.set(FlatFooted())
        
        # skills, adding all found in the skill module
        for cls in self._base_skills():
            self.registry.set(cls())
        
    def configure(self, id, value):
        component = self.registry.get(id)
        if component.is_modifiable():
            component.value = value
        else:
            self.linker.remove(component)
            self.registry.set(value)
        self.connect_links()
        
    def add_component(self, component):
        self.registry.set(component)
        self.connect_links()
        
    def remove_component(self, thing):
        component = (thing if isinstance(thing, Component) 
                    else self.registry.get(thing))
        if component.is_destroyable():
            for item in component.subcomponents:
                self.remove_component(item)
            self.linker.remove(component)
            self.registry.remove(component.id)
    
    # TODO: Implement this!
    def use_equipment(self, id):
        pass
        
    def connect_links(self):
        self.linker.process_all()
    
    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        component_id = self._attribute_to_id(name)
        if self.registry.has(component_id):
            return self.registry.get(component_id)
        raise AttributeError(
            "Unknown attribute '%s' on Character object" % name
        )

    def __setattr__(self, name, value):
        # need to check for registry like this to prevent recursion in lookup
        component_id = self._attribute_to_id(name)
        registry = self.__dict__.get("registry")
        if not registry or not registry.has(component_id):
            super(Character, self).__setattr__(name, value)
        else:
            self.configure(component_id, value)
            
    def _attribute_to_id(self, name):
        return name.lower().replace("_", "-")
    
    def _base_skills(self):
        is_simple = lambda cls: cls not in (Craft, Perform, Profession)
        return filter(is_simple, get_all_skill_classes())
            
    
class ActorBuilder(object):
    
    def build(self):
        actor = Character()
        actor.connect_links()
        return actor
