from statblock.dice import d6, d8
from statblock.weapon import CombinedWeapon
from statblock.weapon import Javelin
from statblock.weapon import Longsword
from statblock.weapon import SLASHING


def test_init_combined_weapon():
    axe_throwing = CombinedWeapon("axe-throwing")
    axe_throwing.set_damage(d6, SLASHING)
    
    assert axe_throwing.is_melee()
    assert axe_throwing.melee.attack.value == 0
    assert axe_throwing.melee.damage.value == d6
    assert axe_throwing.melee.damage.type == SLASHING

    assert axe_throwing.is_ranged()
    assert axe_throwing.ranged.attack.value == 0
    assert axe_throwing.ranged.damage.value == d6
    assert axe_throwing.ranged.damage.type == SLASHING
    
    
def test_init_melee_weapon():
    longsword = Longsword()
    
    assert longsword.melee.attack.value == 0 
    assert longsword.melee.damage.value == d8
    assert longsword.is_melee()
    assert not longsword.is_ranged()
    

def test_init_ranged_weapon():
    javelin = Javelin()
    
    assert javelin.ranged.attack.value == 0 
    assert javelin.ranged.damage.value == d6
    assert javelin.is_ranged()
    assert not javelin.is_melee()
    

def test_critical_damage():
    longsword = Longsword()
    
    assert longsword.critical.range == range(19, 21)
    assert longsword.critical.multiplier == 2
    

if __name__ == '__main__':
    import pytest, sys
    pytest.main(["-s", "-v"] + sys.argv[1:] + [__file__])