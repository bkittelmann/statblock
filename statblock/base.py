from itertools import groupby


def calculate_modifier_sum(modifiers):
    "Default algorithm to calculate the sum of all modifiers values."
    def add(klass, group): 
        if klass.stackable:
            return sum(group) 
        return max(group).value
    return sum(add(k, g) for k, g in groupby(modifiers, type))


class Modifier(object):
    stackable = False    
    
    def __init__(self, value, source=None):
        assert isinstance(value, int)
        self._value = value
        self._source = source or object()
    
    @property
    def source(self):
        return self._source
    
    @property
    def value(self):
        return self._value
    
    def __add__(self, other):
        return self.value + int(other)

    def __radd__(self, other):
        return self + other
        
    def __gt__(self, other):
        return self.value > other.value
    
    def __int__(self):
        return self.value
    
    def __hash__(self):
        return self._source.__hash__()
    
    def __eq__(self, other):
        return other._source == self._source
    
    def __repr__(self):
        return "<%s: %+i>" % (self.__class__.__name__, self.value)
    
    def stacks(self):
        return self.__class__.stackable


class Modifiable(object):
    
    def __init__(self, initial=0):
        self._initial = initial
        self._modifiers = set()
        
    def is_modifiable(self):
        return True
        
    def update(self, *modifiers):
        for m in modifiers:
            self._modifiers.add(m)
        
    def remove(self, modifier):
        self._modifiers.remove(modifier)
        
    @property
    def value(self):
        return self._initial + calculate_modifier_sum(self._modifiers)
    
    @value.setter
    def value(self, new_value):
        self._initial = new_value
    
    def __str__(self):
        return str(self.value)    
        
    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.value)
    

#--- basic registry architecture --------------------------------------
    
class Registry(object):
    
    def __init__(self):
        self._components = {}
        
    @property
    def components(self):
        return self._components.values()
        
    def set(self, component):
        self._components[component.id] = component
        for child in component.subcomponents:
            self.set(child)
        return component
            
    def get(self, id):
        return self._components[id]
    
    def has(self, id):
        return id in self._components
    
    def remove(self, id):
        for child in self.get(id).subcomponents:
            self.remove(child)
        del self._components[id]


class Component(Modifiable):
    
    def __init__(self, id, *args, **kwargs):
        super(Component, self).__init__(*args, **kwargs)
        self._id = id
        self._links = set()
        self._default_bonus = None
        self._subcomponents = set()
    
    @property
    def bonus(self):
        return self._default_bonus
    
    @property
    def id(self):
        return self._id
    
    @property
    def links(self):
        return self._links
    
    @property
    def subcomponents(self):
        return self._subcomponents
    
    def __repr__(self):
        return "<Component '%s'>" % self._id
    

#--- basic character/actor building blocks ------------------------------------------
        
class Actor(object):
    
    def __init__(self):
        self.registry = Registry()
        self.linker = LinkProcessor(self.registry)

        
class Link(object):
    "Links a particular modifier to another component"
    def __init__(self, source, target, modifier):
        self.source = source
        self.target = target
        self.modifier = modifier
        
    def connect(self, registry):
        registry.get(self.target).update(self.modifier)
        
    def __repr__(self):
        return "<Link: '%s' adds a %s to '%s'>" % (
            self.source, self.modifier, self.target
        )
     
        
class ReverseLink(object):
    "Depend on another component's default modifier"    
    def __init__(self, source, target):
        self.source = source
        self.target = target
        
    def connect(self, registry):
        source_obj = registry.get(self.source)
        registry.get(self.target).update(source_obj.bonus)
        
    def __repr__(self):
        return "<ReverseLink: '%s' is modified by '%s'>" % (
            self.target, self.source
        )
        
        
class UseLink(object):
    "Use all modifiers of a source to the target"    
    def __init__(self, source, target):
        self.source = source
        self.target = target
        
    def connect(self, registry):
        source_obj = registry.get(self.source)
        registry.get(self.target).update(*source_obj._modifiers)
        
    def __repr__(self):
        return "<UseLink: '%s' uses all modifiers from '%s'>" % (
            self.target, self.source
        )
        
     
class LinkProcessor(object):
    
    def __init__(self, registry):
        self.registry = registry
        self.unapplied = set()
    
    def apply(self, modifiable):
        for link in modifiable.links:
            try:
                link.connect(self.registry)
            except KeyError:
                self.unapplied.add(link)
        
    def process_all(self):
        for c in self.registry.components:
            self.apply(c)
   
    def remove(self, modifiable):
        for component in modifiable.subcomponents:
            self.remove(component)
        self._run(modifiable, lambda c, m: c.remove(m))
            
    def _run(self, modifiable, callback):
        for link in modifiable.links:
            callback(self.registry.get(link.target), link.modifier)
            

class LinkBuilder(object):
    
    def __init__(self, component):
        self._component = component
        
    def uses_all_from(self, provider):
        "Uses the same modifiers as the target it links to"
        self._component._links.add(UseLink(provider, self._component.id))
        return self
        
        
    def modifies(self, *targets, **kwargs):
        bonus = kwargs.get("bonus", self._component.bonus)
        for target in targets:
            self._component._links.add(Link(self._component.id, target, bonus))
        return self
    
    def is_modified_by(self, *targets):
        for target in targets:
            self._component._links.add(ReverseLink(target, self._component.id))
        return self
    
    def build(self):
        return self._component.links
            
            
#--- concrete implementations of _modifiers -----------------------------------------
    
class EnhancementModifier(Modifier): 
    pass
        

class UntypedModifier(Modifier): 
    stackable = True


class SizeModifier(Modifier): 
    pass      


class ArmorModifier(Modifier):
    
    def __init__(self, source):
        Modifier.__init__(self, source.value, source)


class ShieldModifier(Modifier):
    
    def __init__(self, source):
        Modifier.__init__(self, source.value, source)
        
        
class ValueModifier(Modifier):
    stackable = True    
    
    def __init__(self, source):
        Modifier.__init__(self, source.value, source)
        
    @property
    def value(self):
        return self.source.value  


class NaturalArmorModifier(ValueModifier):
    pass