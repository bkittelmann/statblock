from statblock.base import Bonus
from statblock.base import Component
from statblock.base import Modifier

import math


class AbilityModifier(Modifier):
    
    def __init__(self, source):
        Modifier.__init__(self, Bonus.UNTYPED, source.value, source)
        
    @property
    def value(self):
        return int(math.floor((self.source.value - 10) / 2))    
    

class Ability(Component):
    
    def __init__(self, *args, **kwargs):
        super(Ability, self).__init__(*args, **kwargs)
        self.bonus = AbilityModifier(self)
    
    def __repr__(self):
        return "%s: %s" % (self.__class__.__name__, self.value)
        

class Strength(Ability):
    
    def get_provider_id(self):
        return "Strength"
    
    def declare_dependencies(self):
        self.modified_component_ids.add("BaseMeleeAttack")
        

class Dexterity(Ability):
    
    def get_provider_id(self):
        return "Dexterity"
    
    def declare_dependencies(self):
        self.modified_component_ids = set([
            "Initiative",
            "ArmorClass",
            "BaseRangedAttack",
            "Reflex"
        ])
        

class Constitution(Ability):
    
    def get_provider_id(self):
        return "Constitution"
    
    def declare_dependencies(self):
        self.modified_component_ids = set([
            "HitPoints",
            "Fortitude"
        ])
        

class Intelligence(Ability):
    
    def get_provider_id(self):
        return "Intelligence"

  
class Wisdom(Ability):
    
    def get_provider_id(self):
        return "Wisdom"
    
    def declare_dependencies(self):
        self.modified_component_ids.add("Will")
        

class Charisma(Ability):
    
    def get_provider_id(self):
        return "Charisma"