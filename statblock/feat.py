from statblock.base import Component
from statblock.base import LinkBuilder
from statblock.base import Modifier


class FeatModifier(Modifier):
    
    def __init__(self, value, source):
        Modifier.__init__(self, value, source)


class Feat(Component):
    
    @property
    def name(self):
        return "Undefined"
    
    
#--- Implementations of PHB feats ------------------------------------- 

class ImprovedInitiative(Feat):
    "Described in PHB p.96"
    
    def __init__(self):
        super(ImprovedInitiative, self).__init__("feat/improved-initiative")
        self._default_bonus = FeatModifier(+4, self)
        LinkBuilder(self).modifies("initiative")
        
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
        id = "feat/weapon-focus/%s" % weapon.name.lower()
        super(WeaponFocus, self).__init__(id)
        self._default_bonus = FeatModifier(+1, self)
        self.weapon = weapon
        LinkBuilder(self).modifies("%s/melee/attack" % self.weapon.id)
        
    @property
    def name(self):
        return "Weapon Focus (%s)" % self.weapon.name
        