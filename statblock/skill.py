from statblock.base import Bonus
from statblock.base import Component
from statblock.base import Modifier

import math

class SkillModifier(Modifier):
    
    def __init__(self, skill):
        Modifier.__init__(self, Bonus.UNTYPED, skill.ranks, skill)
        
    @property
    def value(self):
        return math.floor(self.source.value)
        

class AddSynergyAction(object):
    
    def __init__(self, component, target_id):
        self.done = False
        self.component = component
        self.target_id = target_id
    
    def execute(self, registry):
        other = registry.get(self.target_id)
        self.component.modified_component_ids.add(self.target_id)
        other.update(SynergyModifier(self.component))
        self.done = True
        
        
class SynergyModifier(Modifier):
    
    def __init__(self, skill):
        Modifier.__init__(self, Bonus.UNTYPED, skill.ranks, skill)
        
    @property
    def value(self):
        return +2 if self.source.ranks >= 5 else 0
        
        
class Skill(Component):
    
    def __init__(self, ranks=0):
        super(Skill, self).__init__(initial=ranks)
        self.bonus = SkillModifier(self)
    
    @property
    def value(self):
        return super(Skill, self).value
        
    @value.setter
    def value(self, other):
        if (other % 0.5) != 0:
            raise Exception("Only fractions of 0.5 can be set as ranks")
        self.initial = other
        
    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.value)
        
    ranks = value
    

class Balance(Skill):
    
    def id(self):
        return "Balance"
    
    def declare_dependencies(self):
        self.affected_component_ids.add("Dexterity")
        
        
class Jump(Skill):
    
    def id(self):
        return "Jump"
        
    def declare_dependencies(self):
        self.affected_component_ids.add("Strength")

        
class Tumble(Skill):
    
    def id(self):
        return "Tumble"
    
    def declare_dependencies(self):
        self.affected_component_ids.add("Dexterity")
        self.registry.actions.add(AddSynergyAction(self, "Balance"))
        self.registry.actions.add(AddSynergyAction(self, "Jump"))
