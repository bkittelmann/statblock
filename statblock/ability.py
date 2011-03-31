from statblock.base import Component
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
        self.bonus = AbilityModifier(self)
    
    def is_destroyable(self):
        return False
    
    def __repr__(self):
        return "%s: %s" % (self.__class__.__name__, self.value)
        

class Strength(Ability):
    
    def id(self):
        return "strength"
    
    def declare_dependencies(self):
        self.modified_component_ids.add("attack/melee")
        

class Dexterity(Ability):
    
    def id(self):
        return "dexterity"
    
    def declare_dependencies(self):
        self.modified_component_ids = set([
            "initiative",
            "armor-class",
            "attack/ranged",
            "reflex"
        ])
        

class Constitution(Ability):
    
    def id(self):
        return "Constitution"
    
    def declare_dependencies(self):
        self.modified_component_ids = set([
            "hit-points",
            "fortitude"
        ])
        

class Intelligence(Ability):
    
    def id(self):
        return "intelligence"

  
class Wisdom(Ability):
    
    def id(self):
        return "wisdom"
    
    def declare_dependencies(self):
        self.modified_component_ids.add("will")
        

class Charisma(Ability):
    
    def id(self):
        return "charisma"