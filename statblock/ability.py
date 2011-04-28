from statblock.base import Component
from statblock.base import LinkBuilder
from statblock.base import Modifier

import math


class AbilityModifier(Modifier):
    stackable = True
    
    def __init__(self, source):
        Modifier.__init__(self, source.value, source)
        
    @property
    def value(self):
        return int(math.floor((self.source.value - 10) / 2))    
    

class Ability(Component):
    
    def __init__(self, *args, **kwargs):
        super(Ability, self).__init__(*args, **kwargs)
        self._default_bonus = AbilityModifier(self)
    
    def is_destroyable(self):
        return False
    
    def __repr__(self):
        return "%s: %s" % (self.__class__.__name__, self.value)
    
        
class Dexterity(Ability):
    
    def __init__(self, initial=0):
        super(Dexterity, self).__init__("dexterity", initial)
        LinkBuilder(self).modifies(
            "armor-class",
            "attack/ranged",
            "reflex",
            "initiative"
        )
        

class Strength(Ability):
    
    def __init__(self, initial=0):
        super(Strength, self).__init__("strength", initial)
        LinkBuilder(self).modifies("attack/melee")
        

class Constitution(Ability):
    
    def __init__(self, initial=0):
        super(Constitution, self).__init__("constitution", initial)
        LinkBuilder(self).modifies("hit-points", "fortitude")


class Intelligence(Ability):
    
    def __init__(self, initial=0):
        super(Intelligence, self).__init__("intelligence", initial)

  
class Wisdom(Ability):
    
    def __init__(self, initial=0):
        super(Wisdom, self).__init__("wisdom", initial)
        LinkBuilder(self).modifies("will")


class Charisma(Ability):
    
    def __init__(self, initial=0):
        super(Charisma, self).__init__("charisma", initial)
