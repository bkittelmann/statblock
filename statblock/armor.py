from statblock.base import Component
from statblock.base import LinkBuilder
from statblock.base import ArmorModifier
from statblock.base import NaturalArmorModifier
from statblock.base import ShieldModifier
from statblock.equipment import Wearable


class Armor(Component, Wearable):
    slot = "body"
    
    def __init__(self, id, initial=0):
        super(Armor, self).__init__(id, initial=initial)
        self._default_bonus = ArmorModifier(self)
        LinkBuilder(self).modifies("armor-class")
        
        
class NaturalArmor(Component):
    
    def __init__(self, initial=0):
        super(NaturalArmor, self).__init__("natural-armor", initial=initial)
        self._default_bonus = NaturalArmorModifier(self)
        LinkBuilder(self).modifies("armor-class")
    
    def is_destroyable(self):
        return False
        

class Shield(Component, Wearable):
    slot = ["right-hand", "left-hand"]

    def __init__(self, id, initial=0):
        super(Shield, self).__init__(id, initial=initial)
        self._default_bonus = ShieldModifier(self)
        LinkBuilder(self).modifies("armor-class")
        
    def find_slot(self, slots):
        left = slots.get("left-hand")
        right = slots.get("right-hand")
        if not left and not isinstance(right, Shield):
            return ["left-hand"]
        if not right and not isinstance(left, Shield):
            return ["right-hand"]
        return []
        

class ChainMail(Armor):
    
    def __init__(self):
        super(ChainMail, self).__init__("armor/chain-mail", initial=5)
    
        
class LightSteelShield(Shield):
    
    def __init__(self):
        super(LightSteelShield, self).__init__("shield/light-steel-shield", initial=1)
        
    
class HeavySteelShield(Shield):
    
    def __init__(self):
        super(HeavySteelShield, self).__init__("shield/heavy-steel-shield", initial=2)
        
    