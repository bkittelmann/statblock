from statblock.character import Character
from statblock.armor import ChainMail
from statblock.armor import LightSteelShield
from statblock.armor import HeavySteelShield


def test_adding_chainmail():
    guard = Character()
    guard.abilities.dexterity.value = 12
    guard.armor = ChainMail()
    assert guard.armor_class.value == 16
    

def test_adding_shield():
    guard = Character()
    guard.shield = LightSteelShield()
    assert guard.armor_class.value == 11
    

def test_adding_all_armor_types():
    guard = Character()
    guard.abilities.dexterity.value = 13
    guard.natural_armor.value = 2 # got really thick skin
    guard.armor = ChainMail()
    guard.shield = LightSteelShield()
    assert guard.armor_class.value == 19
    
    
def test_flatfooted_armor_class():
    guard = Character()
    guard.abilities.dexterity.value = 12
    
    assert guard.armor_class.value == 11
    assert guard.flat_footed.value == 10


def test_only_armor_low_touch_armor_class():
    guard = Character()
    guard.armor = ChainMail()
    
    assert guard.armor_class.value == 15
    assert guard.touch.value == 10
    
    guard.abilities.dexterity.value = 14
    assert guard.armor_class.value == 17
    assert guard.touch.value == 12
    

def test_that_old_armor_bonus_gets_removed():
    guard = Character()
    guard.shield = HeavySteelShield()
    assert guard.armor_class.value == 12
    
    light = LightSteelShield()
    guard.shield = light
    
    assert guard.armor_class.value == 11
    
    # the proxy should point to the light shield
    assert light.value == guard.shield.value
    
    # and also only one shield component should remain 
    assert len(guard.shield._components) == 1
    

if __name__ == '__main__':
    import pytest, sys
    pytest.main(["-s", "-v"] + sys.argv[1:] + [__file__])
