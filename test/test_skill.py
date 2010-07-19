from statblock.skill import Tumble
from statblock.skill import Balance
from statblock.base import AbstractComponent
from statblock.character import Initiative
from statblock.ability import Strength
from statblock.ability import Dexterity
from statblock.skill import Jump

import py
import os.path


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
    
    assert tumble.value == 8
    assert balance.value == 4
    

if __name__ == '__main__':
    py.cmdline.pytest(["-s", os.path.basename(__file__)])
