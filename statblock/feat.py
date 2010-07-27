from statblock.base import Bonus
from statblock.base import Component
from statblock.base import Modifier


class FeatModifier(Modifier):
    
    def __init__(self, value, source):
        Modifier.__init__(self, Bonus.UNTYPED, value, source)
        

class ImprovedInitiative(Component):
    "A feat, described in PHB p.96"
    
    def __init__(self):
        self.bonus = FeatModifier(+4, self)
        self.modified_component_ids.add("initiative")
        
        
class WeaponFocus(Component):
    
    def __init__(self):
        super(WeaponFocus, self).__init__()
        self.bonus = FeatModifier(+1, self)
        
    def declare_dependencies(self):
        # at the moment that's longsword-specific... should take weapon name into account
        self.modified_component_ids.add("weapon/longsword/melee/attack")
        
    
