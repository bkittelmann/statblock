from statblock.equipment import BodySlots
from statblock.equipment import OneHanded
from statblock.equipment import TwoHanded
from statblock.equipment import Wearable
from statblock.armor import Shield

class MockDagger(OneHanded):
    pass        
        
class MockSpear(TwoHanded):
    pass

class MockChainMail(Wearable):
    slot = "body"


def test_add_one_handed_weapon_to_armor():
    slots = BodySlots()
    dagger = MockDagger()
    slots.add(MockChainMail())
    c = MockChainMail()
    assert not c.can_be_added(slots)
    assert dagger.can_be_added(slots)


def test_two_handed_weapon_can_not_be_added_aside_one_handed():
    slots = BodySlots()
    slots.add(MockDagger())
    spear = MockSpear()
    assert not spear.can_be_added(slots)


def test_remove_two_handed_to_make_place_for_one_handed_weapon():
    slots = BodySlots()
    spear = MockSpear()
    dagger = MockDagger()

    slots.add(spear)
    assert not dagger.can_be_added(slots)
    
    slots.remove(spear)
    assert spear.can_be_added(slots)
    assert dagger.can_be_added(slots)
    
    slots.add(dagger)
    assert not spear.can_be_added(slots)


def test_shield_can_only_be_worn_once():
    slots = BodySlots()
    shield = Shield("mock")
    slots.add(shield)
    assert not slots.add(shield)
    
def test_clearing_of_slot():
    slots = BodySlots()
    slots.add(MockDagger())
    slots.clear("right-hand")
    assert not slots.get("right-hand")    

if __name__ == '__main__':
    import pytest, sys
    pytest.main(["-s", "-v"] + sys.argv[1:] + [__file__])