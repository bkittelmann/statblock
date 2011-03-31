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
    "A default registry that is more friendly to its clients"
    
    def __init__(self):
        self._components = {}
        self._actions = set()
        
    def add_action(self, action):
        self._actions.add(action)

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
    
    def has(self, component_id):
        return component_id in self._components
    
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
    
    def __init__(self, component, id, bonus=None):
        self.done = False
        self.component = component
        self.id = id
        self.bonus = bonus
    
    def execute(self, registry):
        self.component.affects(registry.get(self.id), bonus=self.bonus)
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
        if self._registry.has(component.id()):
            self._registry.get(component.id()).destroy()
            
        self._components.append(component)
        self._registry.set(component)
        return component
             
    def destroy(self):
        "Subclasses need to override to define what would happen on destroy"
        pass

    def id(self):
        return self._id

    def is_destroyable(self):
        return True
    
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
        
        
    def affects(self, other, bonus=None):
        self.modified_component_ids.add(other.id())
        other.update(bonus or self.bonus)
        
        
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
    
    
    def destroy(self):
        if not self.is_destroyable():
            return
        for m in self.modified_component_ids:
            self.registry.get(m).remove(self.bonus)
            

class VirtualGroup(Component):
    
    def on_register(self, registry):
        self.registry = registry.merge(self.registry)
        return False
    
    def __iter__(self):
        return iter(self._components)
        
    def __repr__(self):
        return "<%s>" % self.__class__.__name__
            

class ComponentProxy(Component):
    
    def __init__(self, id):
        super(ComponentProxy, self).__init__()
        self._id = id
        self._target = Component()
        self._components.append(self._target)
        
    # make it possible to one and only child component
    def add(self, component):
        self.destroy()
        self._target = Component.add(self, component)
        return self
     
    def affects(self, other):
        self._target.affects(self, other)

    def destroy(self):
        if self.is_destroyable():
            self._components.remove(self._target)
            self._target.destroy()

    def remove(self, modifier):
        self._target.remove(modifier)
        
    def update(self, modifier):
        self._target.update(modifier)
        
    @property
    def value(self):
        return self._target.value
    
    @value.setter
    def value(self, new_value):
        self._target.value = new_value
        
    def __repr__(self):
        return repr(self._target)
        
            
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


class NaturalArmorModifier(Modifier):
    
    def __init__(self, source):
        Modifier.__init__(self, source.value, source)
        
    @property
    def value(self):
        return self.source.value


class ShieldModifier(Modifier):
    
    def __init__(self, source):
        Modifier.__init__(self, source.value, source)
