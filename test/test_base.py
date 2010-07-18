from statblock.base import AbstractComponent
from statblock.ability import Dexterity
import py

from statblock.ability import Strength

from statblock.skill import Balance
from statblock.skill import Tumble
from statblock.skill import Jump

from statblock.feat import FeatModifier
from statblock.feat import ImprovedInitiative

from statblock.base import Registry
from statblock.base import Bonus
from statblock.base import EnhancementModifier
from statblock.base import ModifierSet

from statblock.character import Initiative


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
    py.test.raises(TypeError, bset.add, FeatModifier(+4, object()))
    assert len(bset) == 1
    

def test_bonusset_init_and_reject():
    e_mod = EnhancementModifier(+2, object())
    f_mod = FeatModifier(+4, object())
    py.test.raises(TypeError, ModifierSet, [e_mod, f_mod])
    
    
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
    

def test_wiring_skills():
    t = Tumble(6)
    b = Balance(0)
    
    bus = AbstractComponent()
    bus.add(b)
    bus.add(Initiative(0))
    bus.add(Strength(8))
    bus.add(Dexterity(14))
    bus.add(Jump(0))
    bus.add(t)
    
    assert t.value == 8
    assert b.value == 4
    
    
def test_strength_repr():
    s = Strength(12)
    assert str(s) == "Strength: 12"
    

if __name__ == '__main__':
    py.cmdline.pytest(["-s", "test_base.py"])

