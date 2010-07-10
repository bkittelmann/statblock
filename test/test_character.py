from statblock.character import Character, Size
import py


def test_strength_affected():
    guard = Character()
    guard.wire()
    
    guard.abilities.strength = 16
    assert guard.abilities.strength.value == 16
    assert guard.melee_attack.value == 3
    
    guard.abilities.strength.initial -= 4
    assert guard.abilities.strength.value == 12
    assert guard.melee_attack.value == 1
    
    
def test_dexterity_affected():
    guard = Character()
    guard.wire()
    
    guard.abilities.dexterity = 8
    assert guard.armor_class.value == 9
    assert guard.ranged_attack.value == -1
    assert guard.saving_throws.reflex.value == -1

    
def test_constitution_affected():
    guard = Character()
    guard.wire()
    
    guard.abilities.constitution = 13
    assert guard.hit_points.value == 9
    assert guard.saving_throws.fortitude.value == 1
    
    guard.abilities.constitution = 5
    assert guard.hit_points.value == 5
    
    
def test_wisdom_affected():
    guard = Character()
    guard.wire()
    
    guard.abilities.wisdom = 14
    assert guard.saving_throws.will.value == +2
    
    
def test_base_attack():
    guard = Character()
    guard.wire()
    
    guard.base_attack.value += 1
    guard.abilities.strength = 15
    guard.abilities.dexterity = 12
    
    assert guard.melee_attack.value == 3
    assert guard.ranged_attack.value == 2
    

def test_size_effects():
    guard = Character()
    guard.wire()
    
    guard.size = Size.LARGE
    assert guard.base_attack.value == -1
    assert guard.armor_class.value == 9

    guard.size = Size.MEDIUM
    assert guard.base_attack.value == 0
    assert guard.armor_class.value == 10
 
    

if __name__ == '__main__':
    py.cmdline.pytest(["-k", "test_character", "-s"])