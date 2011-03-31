from statblock.base import Component
from statblock.base import Modifier
from statblock.base import ArmorModifier
from statblock.base import NaturalArmorModifier
from statblock.base import ShieldModifier


class Armor(Component):

    def __init__(self, initial=0):
        super(Armor, self).__init__(initial=initial)
        self.bonus = ArmorModifier(self)
        
    def declare_dependencies(self):
        self.modified_component_ids.add("armor-class")
        
        
class NaturalArmor(Component):
    
    def __init__(self):
        super(NaturalArmor, self).__init__(initial=0)
        self.bonus = NaturalArmorModifier(self)
    
    def id(self):
        return "natural-armor"
    
    def is_destroyable(self):
        return False
    
    def declare_dependencies(self):
        self.modified_component_ids.add("armor-class")
        

class Shield(Component):

    def __init__(self, initial=0):
        super(Shield, self).__init__(initial=initial)
        self.bonus = ShieldModifier(self)
        
    def declare_dependencies(self):
        self.modified_component_ids.add("armor-class")
        

class ChainMail(Armor):
    
    def __init__(self):
        super(ChainMail, self).__init__(initial=5)
    
    def id(self):
        return "armor/chain-mail"
    
        
class LightSteelShield(Shield):
    
    def __init__(self):
        super(LightSteelShield, self).__init__(initial=1)
        
    def id(self):
        return "shield/light-steel-shield"
    
    
class HeavySteelShield(Shield):
    
    def __init__(self):
        super(HeavySteelShield, self).__init__(initial=2)
        
    def id(self):
        return "shield/heavy-steel-shield"
    
    