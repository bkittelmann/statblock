from statblock.character import Character
from statblock.character import Size
from statblock.weapon import Longsword
from statblock.dice import d4, d8
from statblock.feat import WeaponFocus
from statblock.weapon import Dagger
from statblock.ability import Strength

import py
import os.path


def test_strength_repr():
    s = Strength(12)
    assert str(s) == "Strength: 12"
    

def test_strength_affected():
    guard = Character()
    
    guard.abilities.strength = 16
    assert guard.abilities.strength.value == 16
    assert guard.attack.melee.value == 3
    
    guard.abilities.strength.initial -= 4
    assert guard.abilities.strength.value == 12
    assert guard.attack.melee.value == 1
    
    
def test_dexterity_affected():
    guard = Character()
    guard.abilities.dexterity = 8
    assert guard.armor_class.value == 9
    assert guard.attack.ranged.value == -1
    assert guard.saving_throws.reflex.value == -1

    
def test_constitution_affected():
    guard = Character()
    guard.abilities.constitution = 13
    assert guard.hit_points.value == 9
    assert guard.saving_throws.fortitude.value == 1
    
    guard.abilities.constitution = 5
    assert guard.hit_points.value == 5
    
    
def test_wisdom_affected():
    guard = Character()
    guard.abilities.wisdom = 14
    assert guard.saving_throws.will.value == +2
    
    
def test_base_attack():
    guard = Character()
    guard.attack.base.value += 1
    guard.abilities.strength = 15
    guard.abilities.dexterity = 12
    
    assert guard.attack.melee.value == 3
    assert guard.attack.ranged.value == 2
    

def test_size_effects():
    guard = Character()
    guard.size = Size.LARGE
    assert guard.attack.base.value == -1
    assert guard.armor_class.value == 9

    guard.size = Size.MEDIUM
    assert guard.attack.base.value == 0
    assert guard.armor_class.value == 10
 
 
def test_adding_a_weapon():
    guard = Character()
    guard.abilities.strength.value = 16
    guard.abilities.dexterity.value = 13
    guard.registry.actions.clear()
    
    sword = Longsword()
    dagger = Dagger()
    guard.weapons.add(sword)
    guard.weapons.add(dagger)
    guard.add(WeaponFocus())
    
    assert sword.melee.attack.value == 4
    assert sword.melee.damage.default == d8
    assert sword.melee.damage.get_combined() == d8+3
    assert sword.is_melee()
    assert not sword.is_ranged()
    
    assert dagger.melee.attack.value == 3
    assert dagger.is_ranged()
    assert dagger.ranged.attack.value == 1
    assert dagger.ranged.damage.get_combined() == d4 
    

if __name__ == '__main__':
    py.cmdline.pytest(["-s", os.path.basename(__file__)])#, "-k", "sword"])