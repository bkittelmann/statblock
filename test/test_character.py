from statblock.ability import Strength
from statblock.character import ActorBuilder
from statblock.character import Character
from statblock.character import Size
from statblock.dice import d4, d8
from statblock.feat import WeaponFocus
from statblock.weapon import Longsword
from statblock.weapon import Dagger


def test_strength_repr():
    s = Strength(12)
    assert str(s) == "12"
    assert repr(s) == "Strength: 12"
    

def test_strength_affected():
    guard = ActorBuilder().build()
    
    guard.configure("strength", 16)
    assert guard.strength.value == 16
    assert guard.attack.melee.value == 3
    
    guard.configure("strength", 12)
    assert guard.strength.value == 12
    assert guard.attack.melee.value == 1
    
    
def test_dexterity_affected():
    guard = ActorBuilder().build()
    guard.dexterity = 8
    assert guard.armor_class.value == 9
    assert guard.attack.ranged.value == -1
    assert guard.reflex.value == -1

    
def test_constitution_affected():
    guard = Character()
    guard.constitution = 13
    assert guard.hit_points.value == 9
    assert guard.fortitude.value == 1
    
    guard.constitution = 5
    assert guard.hit_points.value == 5
    
    
def test_wisdom_affected():
    guard = Character()
    guard.wisdom = 14
    assert guard.will.value == +2
    
    
def test_base_attack():
    guard = ActorBuilder().build()
    guard.attack.base.value += 1
    assert guard.attack.melee.value == 1
    
    guard.strength = 15
    guard.dexterity = 12
    
    assert guard.attack.melee.value == 3
    assert guard.attack.ranged.value == 2
    

def test_grapple_attack():
    guard = ActorBuilder().build()
    guard.attack.base.value += 3
    guard.strength = 16
    guard.configure("size", Size.LARGE)
    assert guard.size == Size.LARGE
    assert guard.attack.grapple.value == 10
    

def test_size_effects():
    guard = ActorBuilder().build()
    guard.size = Size.LARGE
    assert guard.attack.base.value == -1
    assert guard.armor_class.value == 9

    guard.size = Size.MEDIUM
    assert guard.attack.base.value == 0
    assert guard.armor_class.value == 10
 
 
def test_adding_a_weapon():
    guard = ActorBuilder().build()
    guard.strength.value = 16
    guard.dexterity.value = 13
    
    sword = Longsword()
    dagger = Dagger()
    guard.add_component(sword)
    guard.add_component(dagger)
    guard.add_component(WeaponFocus(sword))
    
    assert sword.melee.attack.value == 4
    assert sword.melee.damage.default == d8
    assert sword.melee.damage.value == d8+3
    
    assert dagger.melee.attack.value == 3
    assert dagger.ranged.attack.value == 1
    assert dagger.ranged.damage.value == d4 
    
    
def test_that_vital_objects_like_dexterity_can_not_be_destroyed():
    guard = ActorBuilder().build()
    guard.dexterity = 12
    assert guard.armor_class.value == 11
    
    guard.remove_component("dexterity")
    assert guard.armor_class.value == 11

    guard.registry.get("skill/jump").value = 5
    guard.configure("skill/tumble", 5)
    guard.remove_component("skill/jump")
    
    assert guard.registry.get("skill/tumble").value == 8
    assert guard.registry.has("skill/jump")
    

if __name__ == '__main__':
    import pytest, sys
    pytest.main(["-s", "-v"] + sys.argv[1:] + [__file__])