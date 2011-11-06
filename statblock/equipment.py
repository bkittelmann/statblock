class BodySlots(object):
    """
    A model for knowing which item is worn where on the body of a character.
    Currently only weapon- and armor related slots are implemented.
    """
    
    def __init__(self):
        self._items = {
            "right-hand": None,
            "left-hand": None,
            "body": None
        }
        
    def get(self, slot):
        return self._items[slot]
    
    def is_available(self, *slots):
        return all([self._items[slot] is None for slot in slots])

    def add(self, item):
        slots = item.find_slot(self)
        if len(slots) == 0:
            return False
        for slot in item.find_slot(self):
            self._items[slot] = item
        return True
    
    def clear(self, slot):
        self._items[slot] = None
    
    def remove(self, item):
        for slot, used_item in self._items.items():
            if used_item == item:
                self._items[slot] = None
    
    
class Wearable(object):
    "Mixin for items that can be worn by the character"
    slot = None # must overriden by subclasses
    
    def find_slot(self, slots):
        return [self.slot] if slots.is_available(self.slot) else []
    
    def can_be_added(self, slots):
        return len(self.find_slot(slots)) > 0
    
    
class OneHanded(Wearable):
    slot = ["right-hand", "left-hand"]
    
    def find_slot(self, slots):
        return [s for s in self.slot if slots.is_available(s)]
    

class TwoHanded(Wearable):
    slot = ["right-hand", "left-hand"]
    
    def find_slot(self, slots):
        if slots.is_available(*self.slot):
            return self.slot     
        return []
