from statblock.base import AbstractComponent, Bus, Component, Modifier, Bonus
from statblock.ability import Strength, Dexterity, Constitution, Intelligence, Wisdom, Charisma

class ValueModifier(Modifier):
    
    def __init__(self, source):
        Modifier.__init__(self, Bonus.UNTYPED, source.value, source)
        
    @property
    def value(self):
        return self.source.value  


class SizeModifier(Modifier):
    
    def __init__(self, source):
        Modifier.__init__(self, Bonus.SIZE, source.value, source)
        
    @property
    def value(self):
        return self.source.value
    
    
class _Size(Component):
    
    def __init__(self, name, value):
        super(_Size, self).__init__()
        self.name = name
        self.value = value
        self.bonus = SizeModifier(self)
        
    def declare_dependencies(self):
        self.modified_component_ids = set(["BaseAttack", "ArmorClass"])
    
    def get_provider_id(self):
        return "Size"
            
    def __repr__(self):
        return "<Size.%s>" % self.name
    

class Size(object):
    FINE       = _Size("Fine", +8)
    DIMINUTIVE = _Size("Diminutive", +4)
    TINY       = _Size("Fine", +2)
    SMALL      = _Size("Small", +1)
    MEDIUM     = _Size("Medium", 0)
    LARGE      = _Size("Large", -1)
    HUGE       = _Size("Huge", -2)
    GARGANTUAN = _Size("Gargantuan", -4)
    COLLOSAL   = _Size("Collossal", -8)
    

class Alignment(object):
    LG = "Lawful Good"
    LN = "Lawful Neutral"
    LE = "Lawful Evil"
    NG = "Neutral Good"
    N  = "Neutral"
    NE = "Neutral Evil"
    CG = "Chaotic Good"
    CN = "Chaotic Neutral"
    CE = "Chaotic Evil"
    

class Fortitude(Component):
    
    def get_provider_id(self):
        return "Fortitude"


class Reflex(Component):
    
    def get_provider_id(self):
        return "Reflex"
    

class Will(Component):
    
    def get_provider_id(self):
        return "Will"


class SavingThrowGroup(AbstractComponent):
    
    def __init__(self):
        self._fortitude = Fortitude(0)
        self._reflex = Reflex(0)
        self._will = Will(0)
        self._group = [self._fortitude, self._reflex, self._will]
    
    def add(self):
        for member in self._group:
            self.bus.add(member)
    
    def wire(self):
        for member in self._group:
            member.wire()
    
    @property
    def fortitude(self):
        return self._fortitude

    @fortitude.setter
    def fortitude(self, new_value):
        self._fortitude.value = new_value
        
    @property
    def reflex(self):
        return self._reflex

    @reflex.setter
    def reflex(self, new_value):
        self._reflex.value = new_value
        
    @property
    def will(self):
        return self._will

    @will.setter
    def will(self, new_value):
        self._will.value = new_value
        
    def __repr__(self):
        return "<SavingThrows>"


class AbilityGroup(AbstractComponent):
    
    def __init__(self):
        self._strength     = Strength(10)
        self._dexterity    = Dexterity(10)
        self._constitution = Constitution(10)
        self._intelligence = Intelligence(10)
        self._wisdom       = Wisdom(10)
        self._charisma     = Charisma(10)
        self._group = [
            self._strength,  self._dexterity, self._constitution,
            self._intelligence, self._wisdom, self._charisma
        ]

        
    def add(self):
        for member in self._group:
            self.bus.add(member)
    
    def wire(self):
        for member in self._group:
            member.wire()

    @property
    def strength(self):
        return self._strength    
    
    @strength.setter
    def strength(self, new_value):
        self._strength.value = new_value
        
    @property
    def dexterity(self):
        return self._dexterity    
    
    @dexterity.setter
    def dexterity(self, new_value):
        self._dexterity.value = new_value
        
    @property
    def constitution(self):
        return self._constitution    
    
    @constitution.setter
    def constitution(self, new_value):
        self._constitution.value = new_value
        
    @property
    def intelligence(self):
        return self._intelligence    
    
    @intelligence.setter
    def intelligence(self, new_value):
        self._intelligence.value = new_value
        
    @property
    def wisdom(self):
        return self._wisdom    
    
    @wisdom.setter
    def wisdom(self, new_value):
        self._wisdom.value = new_value
        
    @property
    def charisma(self):
        return self._charisma    
    
    @charisma.setter
    def charisma(self, new_value):
        self._charisma.value = new_value
        

class HitPoints(Component):
    
    def get_provider_id(self):
        return "HitPoints"     
    
    
class Initiative(Component):
    
    def get_provider_id(self):
        return "Initiative"
    
    def __repr__(self):
        return "Initiative: %s" % self.value


class BaseAttack(Component):
    
    def __init__(self, *args, **kwargs):
        super(BaseAttack, self).__init__(*args, **kwargs)
        self.bonus = ValueModifier(self)
    
    def get_provider_id(self):
        return "BaseAttack"
    
    def declare_dependencies(self):
        self.modified_component_ids.add("BaseMeleeAttack")
        self.modified_component_ids.add("BaseRangedAttack")

    
class AttackModifierGroup(object):
    
    def __init__(self):
        self.base = None
        self.melee = None
        self.ranged = None
    

class BaseMeleeAttack(Component):
    
    def get_provider_id(self):
        return "BaseMeleeAttack"   
    

class BaseRangedAttack(Component):
    
    def get_provider_id(self):
        return "BaseRangedAttack"
    
    
class ArmorClass(Component):
    
    def get_provider_id(self):
        return "ArmorClass"


class Character(Bus, AbstractComponent):
    
    def __init__(self):
        super(Character, self).__init__()
        
        self.hit_points = self.add(HitPoints(initial=8))
        self.initiative = self.add(Initiative(0))
        self.alignment = Alignment.N
        self.speed = 30
        self._size = self.add(Size.MEDIUM)

        self.abilities = self.add(AbilityGroup())
        self.saving_throws = self.add(SavingThrowGroup())
        self.armor_class = self.add(ArmorClass(10))
        
        self.attack = AttackModifierGroup()
        self.attack.base = self.add(BaseAttack(0))
        self.attack.melee = self.add(BaseMeleeAttack(0))
        self.attack.ranged = self.add(BaseRangedAttack(0))
        
#        self.melee = [Longsword()]
#        self.ranged = [Longbow()]
        
        
    @property
    def size(self):
        return self._size
        
        
    @size.setter
    def size(self, new_size):
        self.remove(self._size)
        self._size = self.add(new_size)
        self.wire()
        
        
    def __repr__(self):
        return "<Character>"
        
