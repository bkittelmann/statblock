import pytest

from statblock.base import EnhancementModifier
from statblock.base import Modifiable
from statblock.base import UntypedModifier


# a simple mock
class Sword(Modifiable): pass


def test_adding_one_modifier():
    mod = EnhancementModifier(+2)
    s = Sword(0)
    s.update(mod)
    assert len(s._modifiers) == 1
    assert not s._modifiers.pop().stacks()
    
    
def test_calculate_not_stackable_modifiers():
    s = Sword(0)
    s.update(EnhancementModifier(+2), EnhancementModifier(+1))
    assert s.value == 2


def test_calculate_stackable_modifiers():
    vals = range(1, 4)
    s = Sword(0)
    s.update(*[UntypedModifier(i) for i in vals])
    assert s.value == sum(vals)


if __name__ == '__main__':
    import sys
    pytest.main(["-s", "-v"] + sys.argv[1:] + [__file__])

