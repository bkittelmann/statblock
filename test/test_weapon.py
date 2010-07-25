from statblock.dice import d6
from statblock.weapon import CombinedWeapon
from statblock.weapon import Dagger
from statblock.weapon import Longsword

import os.path
from statblock.dice import d8
import py


def test_init_combined_weapon():
    axe_throwing = CombinedWeapon()
    axe_throwing.id = lambda: "axe-throwing"
    axe_throwing.damage = d6
    
    assert axe_throwing.is_melee()
    assert axe_throwing.melee.attack.value == 0
    assert axe_throwing.melee.damage.value == d6

    assert axe_throwing.is_ranged()
    assert axe_throwing.ranged.attack.value == 0
    assert axe_throwing.ranged.damage.value == d6
    
    
def test_init_meleeweapon():
    longsword = Longsword()
    
    assert longsword.melee.attack.value == 0 
    assert longsword.melee.damage.value == d8
    assert longsword.is_melee()
    assert not longsword.is_ranged()
    

if __name__ == '__main__':
    py.cmdline.pytest(["-s", os.path.basename(__file__)])
