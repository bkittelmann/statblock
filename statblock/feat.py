from statblock.base import Bonus
from statblock.base import Component
from statblock.base import Modifier


class FeatModifier(Modifier):
    
    def __init__(self, value, source):
        Modifier.__init__(self, Bonus.UNTYPED, value, source)


class Feat(Component):
    
    @property
    def name(self):
        return "Undefined"
    
    
#--- Implementations of PHB feats ------------------------------------- 

class ImprovedInitiative(Feat):
    "Described in PHB p.96"
    
    def __init__(self):
        super(ImprovedInitiative, self).__init__()
        self.bonus = FeatModifier(+4, self)
        self.modified_component_ids.add("initiative")
        
    @property
    def name(self):
        return "Improved Initiative"
        

class PowerAttack(Feat):
    "Described in PHB p.98"
    
    @property
    def name(self):
        return "Power Attack"
        
        
class WeaponFocus(Feat):
    "Described in PHB p.102"
    
    def __init__(self, weapon):
        super(WeaponFocus, self).__init__()
        self.bonus = FeatModifier(+1, self)
        self.weapon = weapon
        
    def declare_dependencies(self):
        self.modified_component_ids.add("%s/melee/attack" % self.weapon.id())
        
    @property
    def name(self):
        return "Weapon Focus (%s)" % self.weapon.name
        