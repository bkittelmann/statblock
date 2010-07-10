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
        self.modified_component_ids.add("Initiative")
    
