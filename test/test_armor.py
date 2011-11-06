from statblock.armor import ChainMail
from statblock.armor import LightSteelShield
from statblock.armor import HeavySteelShield
from statblock.character import ActorBuilder


def test_adding_chainmail():
    guard = ActorBuilder().build()
    guard.dexterity.value = 12
    guard.add_component(ChainMail())
    assert guard.armor_class.value == 16
    

def test_adding_shield():
    guard = ActorBuilder().build()
    guard.add_component(LightSteelShield())
    assert guard.armor_class.value == 11
    

def test_adding_all_armor_types():
    guard = ActorBuilder().build()
    guard.dexterity.value = 13
    guard.natural_armor.value = 2 # got really thick skin
    guard.add_component(ChainMail())
    guard.add_component(LightSteelShield())
    assert guard.armor_class.value == 19
    
    
def test_flatfooted_armor_class():
    guard = ActorBuilder().build()
    guard.dexterity.value = 12
    
    assert guard.armor_class.value == 11
    assert guard.flat_footed.value == 10


def test_only_armor_low_touch_armor_class():
    guard = ActorBuilder().build()
    guard.add_component(ChainMail())
    
    assert guard.armor_class.value == 15
    assert guard.touch.value == 10
    
    guard.dexterity.value = 14
    assert guard.armor_class.value == 17
    assert guard.touch.value == 12
    

def test_that_old_armor_bonus_gets_removed():
    guard = ActorBuilder().build()

    heavy_shield = HeavySteelShield()
    guard.add_equipment(heavy_shield)
    assert guard.activate_equipment(heavy_shield.id)
    assert guard.armor_class.value == 12

    light_shield = LightSteelShield()
    guard.add_equipment(light_shield)
    
    guard.deactivate_equipment(heavy_shield.id)
    assert guard.activate_equipment(light_shield.id)
    assert guard.armor_class.value == 11
    

if __name__ == '__main__':
    import pytest, sys
    pytest.main(["-s", "-v"] + sys.argv[1:] + [__file__])
