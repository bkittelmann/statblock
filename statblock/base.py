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
    
class Registry(object):
    "A default registry that is more friendly to its clients"
    
    def __init__(self):
        self._components = {}
        self._actions = set()

    @property
    def actions(self):
        return self._actions

    @property
    def components(self):
        return self._components.values()
        
    def set(self, component):
        if component.on_register(self):
            self._actions.update(component.dependency_actions())
            self._components[component.id()] = component
        self.wire()
            
    def get(self, component_id):
        return self._components[component_id]
    
    def merge(self, other):
        for component in other.components:
            self.set(component)
        self._actions.update(other._actions)
        return self
    
    def wire(self):
        remove_later = []
        for action in self._actions:
            try:
                action.execute(self)
                if action.done:
                    remove_later.append(action)
            except Exception as e:
                # TODO: Add logging
                #print e.__class__, e
                pass
        # remove finished actions
        for action in remove_later:
            self._actions.remove(action)
    

class ModifyOtherAction(object):
    
    def __init__(self, component, id):
        self.done = False
        self.component = component
        self.id = id
    
    def execute(self, registry):
        self.component.affects(registry.get(self.id))
        self.done = True
        
        
class DependsOnAction(object):
    
    def __init__(self, component, id):
        self.done = False
        self.component = component
        self.id = id
    
    def execute(self, registry):
        registry.get(self.id).affects(self.component)
        self.done = True


class AbstractComponent(object):
    
    def __init__(self, id=None):
        self._registry = Registry()
        self._id = id
        self._components = []
        
    def add(self, component):
        self._components.append(component)
        self._registry.set(component)
        return component
    
    def id(self):
        return self._id
    
    def on_register(self, registry):
        # It might be that the component has already actions set,
        # which are only expressed as dependencies of its child
        # components. In this case we need to copy those over to
        # the new registry, otherwise they get erased.
        registry.actions.update(self.registry.actions)
        self.registry = registry
        return True
    
    @property
    def registry(self):
        return self._registry    
    
    @registry.setter
    def registry(self, new_registry):
        self._registry = new_registry
        for component in self._components:
            component.registry = new_registry
    
    def __repr__(self):
        return "<Component '%s'>" % self.id()
        

class Component(Modifiable, AbstractComponent):
    
    def __init__(self, initial=0):
        AbstractComponent.__init__(self)
        Modifiable.__init__(self, initial=initial)
                
        # TODO: Refactor these out into sth else
        self.modified_component_ids = set()
        self.affected_component_ids = set()
        self.bonus = None
        
        
    def affects(self, other):
        self.modified_component_ids.add(other.id())
        other.update(self.bonus)
        
        
    def dependency_actions(self):
        self.declare_dependencies()
        actions = []
        for id in self.modified_component_ids:
            actions.append(ModifyOtherAction(self, id))
        for id in self.affected_component_ids:
            actions.append(DependsOnAction(self, id))
        return actions
        
    # template method to be used by child classes 
    def declare_dependencies(self):
        pass


class VirtualGroup(Component):
    
    def on_register(self, registry):
        self.registry = registry.merge(self.registry)
        return False
        
    def __repr__(self):
        return "<%s>" % self.__class__.__name__
            
#--- concrete implementations of modifiers -----------------------------------------
    
class EnhancementModifier(Modifier):
    
    def __init__(self, value, source):
        Modifier.__init__(self, Bonus.ENHANCEMENT, value, source)
        
