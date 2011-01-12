from statblock.base import Bonus
from statblock.base import EnhancementModifier
from statblock.base import ModifierSet
from statblock.feat import FeatModifier

import pytest


def test_bonus_stacks():
    assert Bonus.UNTYPED.stacks()
    

def test_bonus_stacks_not():
    assert not Bonus.ENHANCEMENT.stacks()
    
    
def test_bonusset_init_set_stacks():
    mod = EnhancementModifier(+2, object())
    bset = ModifierSet([mod])
    assert not bset.stacks()
    assert len(bset) == 1
    
    
def test_bonusset_reject_other_types():
    mod = EnhancementModifier(+2, object())
    bset = ModifierSet([mod])
    pytest.raises(TypeError, bset.add, FeatModifier(+4, object()))
    assert len(bset) == 1
    

def test_bonusset_init_and_reject():
    e_mod = EnhancementModifier(+2, object())
    f_mod = FeatModifier(+4, object())
    pytest.raises(TypeError, ModifierSet, [e_mod, f_mod])
    
    
def test_bonusset_calculate_not_stackable():
    mod1 = EnhancementModifier(+2, object())
    mod2 = EnhancementModifier(+1, object())
    bset = ModifierSet([mod1, mod2])
    assert bset.calculate(0) == 2
    

def test_bonusset_calculate_stackable():
    mod1 = FeatModifier(+2, object())
    mod2 = FeatModifier(+1, object())
    mod3 = FeatModifier(+1, object())
    bset = ModifierSet([mod1, mod2, mod3])
    assert bset.calculate(2) == 6
    

if __name__ == '__main__':
    import sys
    pytest.main(["-s", "-v"] + sys.argv[1:] + [__file__])

