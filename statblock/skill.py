from statblock.base import Bonus
from statblock.base import Component
from statblock.base import Modifier

class SkillModifier(Modifier):
    
    def __init__(self, skill):
        Modifier.__init__(self, Bonus.UNTYPED, skill.ranks, skill)
        

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
        

class Balance(Component):
    
    def __init__(self, ranks):
        super(Balance, self).__init__()
        self.ranks = ranks
        self.value = self.ranks
        self.bonus = SkillModifier(self)
        
    def id(self):
        return "Balance"
        
    def __repr__(self):
        return "Balance: %s" % self.value
    
    def declare_dependencies(self):
        self.affected_component_ids.add("Dexterity")
        
        
class Jump(Component):
    
    def __init__(self, ranks):
        super(Jump, self).__init__()
        self.ranks = ranks
        self.value = self.ranks
        self.bonus = SkillModifier(self)
        
    def id(self):
        return "Jump"
        
    def __repr__(self):
        return "Jump: %s" % self.value
    
    def declare_dependencies(self):
        self.affected_component_ids.add("Strength")

        
class Tumble(Component):
    
    def __init__(self, ranks):
        super(Tumble, self).__init__()
        self.ranks = ranks
        self.bonus = SkillModifier(self)
        self.value = self.ranks
    
    def id(self):
        return "Tumble"
    
    def __repr__(self):
        return "Tumble: %s" % self.value
    
    def declare_dependencies(self):
        self.affected_component_ids.add("Dexterity")
        self.registry._actions.add(AddSynergyAction(self, "Balance"))
        self.registry._actions.add(AddSynergyAction(self, "Jump"))
