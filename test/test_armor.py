from statblock.character import Character
from statblock.armor import ChainMail
from statblock.armor import LightSteelShield

import py
import os.path

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
    

if __name__ == '__main__':
    py.cmdline.pytest(["-s", os.path.basename(__file__)])
