from statblock.base import Bonus
from statblock.base import Component
from statblock.base import Modifier
from statblock.base import VirtualGroup

import math

class SkillModifier(Modifier):
    
    def __init__(self, skill):
        Modifier.__init__(self, Bonus.UNTYPED, skill.ranks, skill)
        
    @property
    def value(self):
        return math.floor(self.source.value)
        

class SynergyModifier(Modifier):
    
    def __init__(self, skill):
        Modifier.__init__(self, Bonus.UNTYPED, skill.ranks, skill)
        
    @property
    def value(self):
        return +2 if self.source.ranks >= 5 else 0


class SynergyAction(object):
    
    def __init__(self, component, target_id):
        self.done = False
        self.component = component
        self.target_id = target_id
    
    def execute(self, registry):
        other = registry.get(self.target_id)
        self.component.modified_component_ids.add(self.target_id)
        other.update(SynergyModifier(self.component))
        self.done = True
        
        
class Skill(Component):
    
    def __init__(self, ranks=0):
        super(Skill, self).__init__(initial=ranks)
        self.bonus = SkillModifier(self)
        
    @property
    def armor_check_penalty(self):
        return 0

    @property
    def untrained(self):
        return True
    
    @property
    def value(self):
        return super(Skill, self).value
        
    @value.setter
    def value(self, other):
        if (other % 0.5) != 0:
            raise Exception("Only fractions of 0.5 can be set as ranks")
        self.initial = other
        
    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.value)
        
    @property
    def ranks(self):
        return self.initial
    
    @ranks.setter
    def ranks(self, new_value):
        self.value = new_value
    
    
#--- concrete skill implementations -----------------------------------

class Appraise(Skill):
    
    @property
    def name(self):
        return "Appraise"
    
    def id(self):
        return "skill/appraise"
    
    def declare_dependencies(self):
        self.affected_component_ids.add("intelligence")
            

class Balance(Skill):
    
    @property
    def name(self):
        return "Balance"
    
    @property
    def armor_check_penalty(self):
        return 1
    
    def id(self):
        return "skill/balance"
    
    def declare_dependencies(self):
        self.affected_component_ids.add("dexterity")
        
        
class Bluff(Skill):
    
    @property
    def name(self):
        return "Bluff"
    
    def id(self):
        return "skill/bluff"
    
    def declare_dependencies(self):
        self.affected_component_ids.add("charisma")
        self.registry.add_action(SynergyAction(self, "skill/diplomacy"))
        self.registry.add_action(SynergyAction(self, "skill/disguise"))
        self.registry.add_action(SynergyAction(self, "skill/intimidate"))
        self.registry.add_action(SynergyAction(self, "skill/sleight-of-hand"))
        

class Climb(Skill):
    
    @property
    def name(self):
        return "Climb"
    
    @property
    def armor_check_penalty(self):
        return 1
    
    def id(self):
        return "skill/climb"
    
    def declare_dependencies(self):
        self.affected_component_ids.add("strength")
        

class Concentration(Skill):
    
    @property
    def name(self):
        return "Concentration"
    
    def id(self):
        return "skill/concentration"
    
    def declare_dependencies(self):
        self.affected_component_ids.add("constitution")
                
        
class Craft(Skill):

    def __init__(self, qualifier, ranks=0):
        super(Craft, self).__init__(ranks=ranks)
        self.qualifier = qualifier
        
    @property
    def name(self):
        return "Craft (%s)" % self.qualifier
    
    def id(self):
        return "skill/craft-" + self.qualifier
    
    def declare_dependencies(self):
        self.affected_component_ids.add("intelligence")
        

class DecipherScript(Skill):
    
    @property
    def name(self):
        return "Decipher Script"
    
    @property
    def untrained(self):
        return False
    
    def id(self):
        return "skill/decipher-script"
    
    def declare_dependencies(self):
        self.affected_component_ids.add("intelligence")


class Diplomacy(Skill):
    
    @property
    def name(self):
        return "Diplomacy"
    
    def id(self):
        return "skill/diplomacy"
    
    def declare_dependencies(self):
        self.affected_component_ids.add("charisma")


class DisableDevice(Skill):

    @property
    def name(self):
        return "Disable Device"

    @property
    def untrained(self):
        return False
    
    def id(self):
        return "skill/disable-device"
    
    def declare_dependencies(self):
        self.affected_component_ids.add("intelligence")


class Disguise(Skill):
    
    @property
    def name(self):
        return "Disguise"
    
    def id(self):
        return "skill/disguise"
    
    def declare_dependencies(self):
        self.affected_component_ids.add("charisma")


class EscapeArtist(Skill):
    
    @property
    def name(self):
        return "Escape Artist"
    
    @property
    def armor_check_penalty(self):
        return 1
        
    def id(self):
        return "skill/escape-artist"
    
    def declare_dependencies(self):
        self.affected_component_ids.add("dexterity")


class Forgery(Skill):
    
    @property
    def name(self):
        return "Forgery"
    
    def id(self):
        return "skill/forgery"
    
    def declare_dependencies(self):
        self.affected_component_ids.add("intelligence")


class GatherInformation(Skill):
    
    @property
    def name(self):
        return "Gather Information"
    
    def id(self):
        return "skill/gather-information"
    
    def declare_dependencies(self):
        self.affected_component_ids.add("charisma")


class HandleAnimal(Skill):
    
    @property
    def name(self):
        return "Handle Animal"
    
    @property
    def untrained(self):
        return False
    
    def id(self):
        return "skill/handle-animal"
    
    def declare_dependencies(self):
        self.affected_component_ids.add("charisma")
        self.registry.add_action(SynergyAction(self, "skill/ride"))


class Heal(Skill):
    
    @property
    def name(self):
        return "Heal"
    
    def id(self):
        return "skill/heal"
    
    def declare_dependencies(self):
        self.affected_component_ids.add("wisdom")


class Hide(Skill):
    
    @property
    def name(self):
        return "Hide"
    
    @property
    def armor_check_penalty(self):
        return 1
    
    def id(self):
        return "skill/hide"
    
    def declare_dependencies(self):
        self.affected_component_ids.add("dexterity")


class Intimidate(Skill):
    
    @property
    def name(self):
        return "Intimidate"
    
    def id(self):
        return "skill/intimidate"
    
    def declare_dependencies(self):
        self.affected_component_ids.add("charisma")


class Jump(Skill):
    
    @property
    def name(self):
        return "Jump"
    
    @property
    def armor_check_penalty(self):
        return 1
    
    def id(self):
        return "skill/jump"
        
    def declare_dependencies(self):
        self.affected_component_ids.add("strength")
        self.registry.add_action(SynergyAction(self, "skill/tumble"))


class KnowledgeArcana(Skill):
    
    @property
    def name(self):
        return "Knowledage (Arcana)"
    
    @property
    def untrained(self):
        return False
    
    def id(self):
        return "skill/knowledge-arcana"
    
    def declare_dependencies(self):
        self.affected_component_ids.add("intelligence")
        self.registry.add_action(SynergyAction(self, "skill/spellcraft"))


class KnowledgeArchitecture(Skill):
    
    @property
    def name(self):
        return "Knowledge (Architecture)"
    
    @property
    def untrained(self):
        return False
    
    def id(self):
        return "skill/knowledge-architecture"
    
    def declare_dependencies(self):
        self.affected_component_ids.add("intelligence")


class KnowledgeDungeoneering(Skill):
    
    @property
    def name(self):
        return "Knowledge (Dungeoneering)"
    
    @property
    def untrained(self):
        return False
    
    def id(self):
        return "skill/knowledge-dungeoneering"
    
    def declare_dependencies(self):
        self.affected_component_ids.add("intelligence")


class KnowledgeGeography(Skill):
    
    @property
    def name(self):
        return "Knowledge (Geography)"
    
    @property
    def untrained(self):
        return False
    
    def id(self):
        return "skill/knowledge-geography"
    
    def declare_dependencies(self):
        self.affected_component_ids.add("intelligence")


class KnowledgeHistory(Skill):
    
    @property
    def name(self):
        return "Knowledge (History)"
    
    @property
    def untrained(self):
        return False
    
    def id(self):
        return "skill/knowledge-history"
    
    def declare_dependencies(self):
        self.affected_component_ids.add("intelligence")


class KnowledgeLocal(Skill):
    
    @property
    def name(self):
        return "Knowledge (Local)"
    
    @property
    def untrained(self):
        return False
    
    def id(self):
        return "skill/knowledge-local"
    
    def declare_dependencies(self):
        self.affected_component_ids.add("intelligence")
        self.registry.add_action(SynergyAction(self, "skill/gather-information"))


class KnowledgeNature(Skill):
    
    @property
    def name(self):
        return "Knowledge (Nature)"
    
    @property
    def untrained(self):
        return False
    
    def id(self):
        return "skill/knowledge-nature"
    
    def declare_dependencies(self):
        self.affected_component_ids.add("intelligence")


class KnowledgeNobility(Skill):
    
    @property
    def name(self):
        return "Knowledge (Nobility)"
    
    @property
    def untrained(self):
        return False
    
    def id(self):
        return "skill/knowledge-nobility"
    
    def declare_dependencies(self):
        self.affected_component_ids.add("intelligence")
        self.registry.add_action(SynergyAction(self, "skill/diplomacy"))


class KnowledgeReligion(Skill):
    
    @property
    def name(self):
        return "Knowledge (Religion)"
    
    @property
    def untrained(self):
        return False
    
    def id(self):
        return "skill/knowledge-religion"
    
    def declare_dependencies(self):
        self.affected_component_ids.add("intelligence")


class KnowledgePlanes(Skill):
    
    @property
    def name(self):
        return "Knowledge (Planes)"
    
    @property
    def untrained(self):
        return False
    
    def id(self):
        return "skill/knowledge-planes"
    
    def declare_dependencies(self):
        self.affected_component_ids.add("intelligence")


class Listen(Skill):
    
    @property
    def name(self):
        return "Listen"
    
    def id(self):
        return "skill/listen"
    
    def declare_dependencies(self):
        self.affected_component_ids.add("wisdom")


class MoveSilently(Skill):

    @property
    def name(self):
        return "Move Silently"
    
    @property
    def armor_check_penalty(self):
        return 1
    
    def id(self):
        return "skill/move-silently"
    
    def declare_dependencies(self):
        self.affected_component_ids.add("dexterity")


class OpenLock(Skill):
    
    @property
    def name(self):
        return "Open Lock"
    
    @property
    def untrained(self):
        return False
    
    def id(self):
        return "skill/open-lock"
    
    def declare_dependencies(self):
        self.affected_component_ids.add("dexterity")


class Perform(Skill):

    def __init__(self, qualifier, ranks=0):
        super(Craft, self).__init__(ranks=ranks)
        self.qualifier = qualifier
    
    @property
    def name(self):
        return "Perform (%s)" % self.qualifier
    
    def id(self):
        return "skill/perform-" + self.qualifier
    
    def declare_dependencies(self):
        self.affected_component_ids.add("charisma")


class Profession(Skill):

    def __init__(self, qualifier, ranks=0):
        super(Craft, self).__init__(ranks=ranks)
        self.qualifier = qualifier

    @property
    def name(self):
        return "Profession (%s)" % self.qualifier

    @property
    def untrained(self):
        return False
    
    def id(self):
        return "skill/profession-" + self.qualifier
    
    def declare_dependencies(self):
        self.affected_component_ids.add("wisdom")        
        

class Ride(Skill):
    
    @property
    def name(self):
        return "Ride"
    
    def id(self):
        return "skill/ride"
    
    def declare_dependencies(self):
        self.affected_component_ids.add("dexterity")


class Search(Skill):
    
    @property
    def name(self):
        return "Search"
    
    def id(self):
        return "skill/search"
    
    def declare_dependencies(self):
        self.affected_component_ids.add("intelligence")


class SenseMotive(Skill):
    
    @property
    def name(self):
        return "Sense Motive"
    
    def id(self):
        return "skill/sense-motive"
    
    def declare_dependencies(self):
        self.affected_component_ids.add("wisdom")
        self.registry.add_action(SynergyAction(self, "skill/diplomacy"))
        
        
class SleightOfHand(Skill):
    
    @property
    def name(self):
        return "Sleight Of Hand"
    
    @property
    def armor_check_penalty(self):
        return 1
    
    def id(self):
        return "skill/sleight-of-hand"
    
    def declare_dependencies(self):
        self.affected_component_ids.add("dexterity")


class Spellcraft(Skill):
    
    @property
    def name(self):
        return "Spellcraft"
    
    @property
    def untrained(self):
        return False
    
    def id(self):
        return "skill/spellcraft"
    
    def declare_dependencies(self):
        self.affected_component_ids.add("intelligence")
        

class Spot(Skill):
    
    @property
    def name(self):
        return "Spot"
    
    def id(self):
        return "skill/spot"
    
    def declare_dependencies(self):
        self.affected_component_ids.add("wisdom")


class Survival(Skill):
    
    @property
    def name(self):
        return "Survival"
    
    def id(self):
        return "skill/survival"
    
    def declare_dependencies(self):
        self.affected_component_ids.add("wisdom")
        self.registry.add_action(SynergyAction(self, "skill/knowledge-nature"))


class Swim(Skill):
    
    @property
    def name(self):
        return "Swim"
    
    @property
    def armor_check_penalty(self):
        return 2

    def id(self):
        return "skill/swim"
    
    def declare_dependencies(self):
        self.affected_component_ids.add("strength")


class Tumble(Skill):

    @property
    def name(self):
        return "Tumble"

    @property
    def armor_check_penalty(self):
        return 1

    @property
    def untrained(self):
        return False
    
    def id(self):
        return "skill/tumble"
    
    def declare_dependencies(self):
        self.affected_component_ids.add("dexterity")
        self.registry.add_action(SynergyAction(self, "skill/balance"))
        self.registry.add_action(SynergyAction(self, "skill/jump"))


class UseMagicDevice(Skill):
    
    @property
    def name(self):
        return "Use Magic Device"
    
    @property
    def untrained(self):
        return False
    
    def id(self):
        return "skill/use-magic-device"
    
    def declare_dependencies(self):
        self.affected_component_ids.add("charisma")


class UseRope(Skill):
    
    @property
    def name(self):
        return "Use Rope"
    
    def id(self):
        return "skill/use-rope"
    
    def declare_dependencies(self):
        self.affected_component_ids.add("dexterity")


#--- Group object or use in Character ---------------------------------

class SkillsGroup(VirtualGroup):
    
    def __init__(self):
        super(SkillsGroup, self).__init__()
        self.appraise = self.add(Appraise(0))
        self.balance = self.add(Balance(0))
        self.bluff = self.add(Bluff(0))
        self.climb = self.add(Climb(0))
        self.concentration = self.add(Concentration(0))
        self.diplomacy = self.add(Diplomacy(0))
        self.disguise = self.add(Disguise(0))
        self.escape_artist = self.add(EscapeArtist(0))
        self.forgery = self.add(Forgery(0))
        self.gather_information = self.add(GatherInformation(0))
        self.heal = self.add(Heal(0))
        self.hide = self.add(Hide(0))
        self.intimidate = self.add(Intimidate(0))
        self.jump = self.add(Jump(0))
        self.listen = self.add(Listen(0))
        self.move_silently = self.add(MoveSilently(0))
        self.open_lock = self.add(OpenLock(0))
        self.ride = self.add(Ride(0))
        self.search = self.add(Search(0))
        self.sense_motive = self.add(SenseMotive(0))
        self.spot = self.add(Spot(0))
        self.survival = self.add(Survival(0))
        self.swim = self.add(Swim(0))
        self.use_rope = self.add(UseRope(0))
    
    def __iter__(self):
        return iter(self._components)
    