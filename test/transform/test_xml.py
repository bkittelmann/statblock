import pytest
from lxml import etree

from statblock.armor import ChainMail
from statblock.bcharacter import Character
from statblock.bcharacter import MeleeAttackCombination
from statblock.bcharacter import RangedAttackCombination
from statblock.feat import PowerAttack
from statblock.feat import WeaponFocus
from statblock.transform.xml import StatblockTypeMap
from statblock.transform.xml import XmlTransformer
from statblock.weapon import Longbow
from statblock.weapon import Longsword
    

def build_character():
    "Test data builder for a simple fighter."
    fighter = Character()
    fighter.name = "Cpl. Tomm Colworn"
    fighter.languages.append("Draconic")
    
    # set some abilities so that we get interesting output in XHTML
    fighter.abilities.dexterity = 12
    fighter.abilities.wisdom = 14
    fighter.abilities.constitution = 14
    fighter.abilities.strength = 16
    
    # add a few weapons
    sword = fighter.weapons.add(Longsword())
    bow = fighter.weapons.add(Longbow())
    
    fighter.melee.append(MeleeAttackCombination(sword))
    fighter.ranged.append(RangedAttackCombination(bow))

    # and some armor
    fighter.armor = ChainMail()
    
    # set some feats
    fighter.feats.add(PowerAttack())
    fighter.feats.add(WeaponFocus(sword))
    return fighter

@pytest.mark.xfail(reason="need base rewrite")    
def test_xml():
    xml = XmlTransformer().toXml(build_character())
    output = etree.fromstring(xml)
    assert output.xpath("count(//language)") == 2
    assert output.xpath("string(//size)") == "Medium"
    assert output.xpath("number(//initiative)") == 1


def test_typemap_copies_itself():
    first = StatblockTypeMap()
    assert isinstance(first.copy(), StatblockTypeMap)


def test_typemap_is_treated_as_true_in_boolean_context():
    assert bool(StatblockTypeMap()) is True


if __name__ == '__main__':
    import pytest, sys
    pytest.main(["-s", "-v"] + sys.argv[1:] + [__file__])
