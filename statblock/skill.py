from statblock.base import Bonus
from statblock.base import Component
from statblock.base import Modifier

class SkillModifier(Modifier):
    
    def __init__(self, skill):
        Modifier.__init__(self, Bonus.UNTYPED, skill.ranks, skill)
        
        
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
        self.bonus = SkillModifier(self)
        
        
    def __repr__(self):
        return "Balance: %s" % self.value
    
    
    def declare_dependencies(self):
        self.affected_component_ids.add("Dexterity")
        
        
class Jump(Component):
    
    def __init__(self, ranks):
        super(Jump, self).__init__()
        self.ranks = ranks
        self.bonus = SkillModifier(self)
        
        
    def __repr__(self):
        return "Jump: %s" % self.value
    
    
    def declare_dependencies(self):
        self.affected_component_ids.add("Strength")

        
class Tumble(Component):
    
    def __init__(self, ranks):
        super(Tumble, self).__init__()
        self.ranks = ranks
        self.bonus = SkillModifier(self)
        
    def __repr__(self):
        return "Tumble: %s" % self.value
    
    def declare_dependencies(self):
        self.affected_component_ids.add("Dexterity")
        self.modified_component_ids.add("Balance") # set synergy
        self.modified_component_ids.add("Jump") # set synergy
    
    def extra_wire(self):
        super(Tumble, self).wire()
        self.bus.get("Balance").update(SynergyModifier(self))
        self.bus.get("Jump").update(SynergyModifier(self))