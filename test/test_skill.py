from statblock.skill import Tumble
from statblock.skill import Balance
from statblock.base import AbstractComponent
from statblock.character import Initiative
from statblock.ability import Strength
from statblock.ability import Dexterity
from statblock.skill import Jump
from statblock.skill import Skill

import py
import os.path


def test_skill_general_methods():
    skill = Skill(ranks=4)
    assert skill.ranks == 4
    assert skill.value == 4
    
    skill.ranks = 2.5
    # value must be same as ranks
    assert skill.value == 2.5 
    # but the bonus it provides must be rounded!
    assert skill.bonus.value == 2
    
    # using fractions other than 0.5 are disallowed
    py.test.raises(Exception, "skill.ranks = 4.2")
    

def test_wiring_skills():
    tumble = Tumble(6)
    balance = Balance(0)
    
    character = AbstractComponent()
    character.add(balance)
    character.add(Initiative(0))
    character.add(Strength(8))
    character.add(Dexterity(14))
    character.add(Jump(0))
    character.add(tumble)
    
    assert tumble.bonus.value == 8
    assert balance.value == 4
    

if __name__ == '__main__':
    py.cmdline.pytest(["-s", os.path.basename(__file__)])