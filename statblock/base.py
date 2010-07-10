class _Bonus(object):
    
    def __init__(self, name, stackable):
        self.name = name
        self.stackable = stackable
        
    def __repr__(self):
        return self.name.upper()
        
    def stacks(self):
        return self.stackable
    

class Bonus(object):
    UNTYPED     = _Bonus("untyped",     True)
    ENHANCEMENT = _Bonus("enhancement", False)
    SIZE        = _Bonus("size",        False)
    

class ModifierSet(set):
    
    def __init__(self, modifiers=[]):
        self._type = modifiers[0].type
        map(self.add, modifiers)
        
                
    def add(self, modifier):
        if modifier.type != self._type:
            raise TypeError("%s does not have bonus of %s" % (modifier, self._type))
        super(ModifierSet, self).add(modifier)


    def stacks(self):
        return self._type.stacks()
    
    
    def calculate(self, initial):
        func = self._add_all if self.stacks() else self._get_highest
        return func(initial)
    
    
    def _add_all(self, initial):
        return reduce(lambda a, b: a + b.value, self, initial)
    
        
    def _get_highest(self, initial):
        return initial + sorted(self, key=lambda m: m.value, reverse=True)[0].value
    
    
class Modifier(object):
        
    def __init__(self, type, value, source):
        self.type = type
        self._value = value
        self.source = source
        
    def __hash__(self):
        return self.source.__hash__()
    
    def __eq__(self, other):
        return other.source == self.source
    
    def __repr__(self):
        return "<Modifier %s to %s, source %s>" % (self.type, self.value, self.source.__class__.__name__)
    
    @property
    def value(self):
        return self._value


class Modifiable(object):
    
    def __init__(self, initial=0):
        self.initial = initial
        self.modifiers = {}
        
    def update(self, modifier):
        modifier_set = self.modifiers.setdefault(modifier.type, ModifierSet([modifier]))
        modifier_set.add(modifier)
        
    def remove(self, modifier):
        self.modifiers[modifier.type].remove(modifier)
        if len(self.modifiers[modifier.type]) == 0:
            del self.modifiers[modifier.type]
        
    @property
    def value(self):
        return reduce(lambda a, b: a + b.calculate(0), self.modifiers.values(), self.initial)
    
    @value.setter
    def value(self, new_value):
        self.initial = new_value
        
    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.value)
    

#--- basic registry architecture --------------------------------------
    
class AbstractComponent(object):
    
    def __init__(self):
        self.bus = None # Use a NullBus?
        self.modified_component_ids = set()
        self.affected_by_component_ids = set()
        self.bonus = None
        
    def get_provider_id(self):
        return self.__class__
    
    # for adding child components - setting bus here?
    def add(self):
        pass
    
    # to remove modifiers that haven been set elsewhere when this
    # component is getting removed
    def destroy(self):
        for id in self.modified_component_ids:
            self.bus.get(id).remove(self.bonus)
    
    def wire(self):
        for id in self.modified_component_ids:
            self.bus.get(id).update(self.bonus)
        for id in self.affected_by_component_ids:
            self.bus.get(id).affects(self)
    
    def affects(self, other):
        self.modified_component_ids.add(other.get_provider_id)
        other.update(self.bonus)
        

class Component(Modifiable, AbstractComponent):
    
    def __init__(self, initial=0):
        Modifiable.__init__(self, initial=initial)
        AbstractComponent.__init__(self)
        self.declare_dependencies()
        
    # template method to be used by child classes 
    def declare_dependencies(self):
        pass


class Bus():
    
    def __init__(self):
        self._objects = {}
        
    def add(self, component):
        component.bus = self
        component.add()
        self._objects[component.get_provider_id()] = component
        return component
    
    def remove(self, component):
        stored = self._objects.pop(component.get_provider_id(), AbstractComponent())
        stored.destroy()
    
    def get(self, provider_id):
        return self._objects[provider_id]
    
    def wire(self):
        for obj in self._objects.values():
            obj.wire()
            
            
#--- concrete implementations of modifiers -----------------------------------------
    
class EnhancementModifier(Modifier):
    
    def __init__(self, value, source):
        Modifier.__init__(self, Bonus.ENHANCEMENT, value, source)
        
