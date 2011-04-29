import math

from statblock.base import Component
from statblock.base import LinkBuilder
from statblock.base import Modifier


class SkillModifier(Modifier):
    stackable = True
    
    def __init__(self, skill):
        Modifier.__init__(self, skill.ranks, skill)
        
    @property
    def value(self):
        return math.floor(self.source.value)
        

class SynergyModifier(Modifier):
    stackable = True
    
    def __init__(self, skill):
        Modifier.__init__(self, skill.ranks, skill)
        
    @property
    def value(self):
        return +2 if self.source.ranks >= 5 else 0


# Should skills be destroyable or not destroyable? Untrained ones would always
# be usable by any character regardless of ranks. So they should exist always.
# But should other skills be lost... this could only happen if the player
# reassigns skill ranks. Probably an advanced feature.   
class Skill(Component):
    
    def __init__(self, id, ranks=0):
        super(Skill, self).__init__(id, initial=ranks)
        self._default_bonus = SkillModifier(self)
        
    @property
    def armor_check_penalty(self):
        return 0

    def is_destroyable(self):
        return False

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
        self._initial = other
        
    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.value)
        
    @property
    def ranks(self):
        return self._initial
    
    @ranks.setter
    def ranks(self, new_value):
        self.value = new_value
    
    
#--- concrete skill implementations -----------------------------------

class Appraise(Skill):
    
    def __init__(self, ranks=0):
        super(Appraise, self).__init__("skill/appraise", ranks)
        LinkBuilder(self).is_modified_by("intelligence")
    
    @property
    def name(self):
        return "Appraise"
            

class Balance(Skill):
    
    def __init__(self, ranks=0):
        super(Balance, self).__init__("skill/balance", ranks)
        LinkBuilder(self).is_modified_by("dexterity")
    
    @property
    def name(self):
        return "Balance"
    
    @property
    def armor_check_penalty(self):
        return 1
    
        
class Bluff(Skill):
    
    def __init__(self, ranks=0):
        super(Bluff, self).__init__("skill/bluff", ranks)
        LinkBuilder(self).is_modified_by("charisma").modifies(
            "skill/diplomacy", "skill/disguise",
            "skill/intimidate", "skill/sleight-of-hand",
            bonus=SynergyModifier(self)
        )
    
    @property
    def name(self):
        return "Bluff"
          

class Climb(Skill):
    
    def __init__(self, ranks=0):
        super(Climb, self).__init__("skill/climb", ranks)
        LinkBuilder(self).is_modified_by("strength")
    
    @property
    def name(self):
        return "Climb"
    
    @property
    def armor_check_penalty(self):
        return 1
    

class Concentration(Skill):
    
    def __init__(self, ranks=0):
        super(Concentration, self).__init__("skill/concentration", ranks)
        LinkBuilder(self).is_modified_by("constitution")
    
    @property
    def name(self):
        return "Concentration"
    
        
class Craft(Skill):

    def __init__(self, qualifier, ranks=0):
        super(Craft, self).__init__("skill/craft-" + self.qualifier.lower(), ranks=ranks)
        LinkBuilder(self).is_modified_by("intelligence")
        self.qualifier = qualifier
        
    @property
    def name(self):
        return "Craft (%s)" % self.qualifier
        

class DecipherScript(Skill):
    
    def __init__(self, ranks=0):
        super(DecipherScript, self).__init__("skill/decipherScript", ranks)
        LinkBuilder(self).is_modified_by("intelligence")
    
    @property
    def name(self):
        return "Decipher Script"
    
    @property
    def untrained(self):
        return False


class Diplomacy(Skill):

    def __init__(self, ranks=0):
        super(Diplomacy, self).__init__("skill/diplomacy", ranks)
        LinkBuilder(self).is_modified_by("charisma")
    
    @property
    def name(self):
        return "Diplomacy"


class DisableDevice(Skill):

    def __init__(self, ranks=0):
        super(DisableDevice, self).__init__("skill/disable-device", ranks)
        LinkBuilder(self).is_modified_by("intelligence")

    @property
    def name(self):
        return "Disable Device"

    @property
    def untrained(self):
        return False
    

class Disguise(Skill):
    
    def __init__(self, ranks=0):
        super(Disguise, self).__init__("skill/disguise", ranks)
        LinkBuilder(self).is_modified_by("charisma")
        
    @property
    def name(self):
        return "Disguise"
    

class EscapeArtist(Skill):

    def __init__(self, ranks=0):
        super(EscapeArtist, self).__init__("skill/escape-artist", ranks)
        LinkBuilder(self).is_modified_by("dexterity")
    
    @property
    def name(self):
        return "Escape Artist"
    
    @property
    def armor_check_penalty(self):
        return 1
        

class Forgery(Skill):
    
    def __init__(self, ranks=0):
        super(Forgery, self).__init__("skill/forgery", ranks)
        LinkBuilder(self).is_modified_by("intelligence")
    
    @property
    def name(self):
        return "Forgery"
    

class GatherInformation(Skill):

    def __init__(self, ranks=0):
        super(GatherInformation, self).__init__("skill/gather-information", ranks)
        LinkBuilder(self).is_modified_by("charisma")
    
    @property
    def name(self):
        return "Gather Information"
    

class HandleAnimal(Skill):
    
    def __init__(self, ranks=0):
        super(HandleAnimal, self).__init__("skill/handle-animal", ranks)
        LinkBuilder(self).is_modified_by("charisma")
        LinkBuilder(self).modifies("skill/ride", bonus=SynergyModifier(self))
        
    @property
    def name(self):
        return "Handle Animal"
    
    @property
    def untrained(self):
        return False
    

class Heal(Skill):
    
    def __init__(self, ranks=0):
        super(Heal, self).__init__("skill/heal", ranks)
        LinkBuilder(self).is_modified_by("wisdom")
    
    @property
    def name(self):
        return "Heal"
    

class Hide(Skill):
    
    def __init__(self, ranks=0):
        super(Hide, self).__init__("skill/hide", ranks)
        LinkBuilder(self).is_modified_by("dexterity")
        
    @property
    def name(self):
        return "Hide"
    
    @property
    def armor_check_penalty(self):
        return 1


class Intimidate(Skill):

    def __init__(self, ranks=0):
        super(Intimidate, self).__init__("skill/intimidate", ranks)
        LinkBuilder(self).is_modified_by("charisma")
    
    @property
    def name(self):
        return "Intimidate"
    
    
class Jump(Skill):
    
    def __init__(self, ranks=0):
        super(Jump, self).__init__("skill/jump", ranks)
        LinkBuilder(self).is_modified_by("strength")
        LinkBuilder(self).modifies("skill/tumble", bonus=SynergyModifier(self))
    
    @property
    def name(self):
        return "Jump"
    
    @property
    def armor_check_penalty(self):
        return 1


class KnowledgeArcana(Skill):
    
    def __init__(self, ranks=0):
        super(KnowledgeArcana, self).__init__("skill/knowledge-arcana", ranks)
        LinkBuilder(self).is_modified_by("intelligence")
        LinkBuilder(self).modifies("skill/spellcraft", bonus=SynergyModifier(self))
    
    @property
    def name(self):
        return "Knowledage (Arcana)"
    
    @property
    def untrained(self):
        return False
    

class KnowledgeArchitecture(Skill):
    
    def __init__(self, ranks=0):
        super(KnowledgeArchitecture, self).__init__("skill/knowledge-architecture", ranks)
        LinkBuilder(self).is_modified_by("intelligence")
    
    @property
    def name(self):
        return "Knowledge (Architecture)"
    
    @property
    def untrained(self):
        return False
    

class KnowledgeDungeoneering(Skill):

    def __init__(self, ranks=0):
        super(KnowledgeDungeoneering, self).__init__("skill/knowledge-dungeoneering", ranks)
        LinkBuilder(self).is_modified_by("intelligence")
    
    @property
    def name(self):
        return "Knowledge (Dungeoneering)"
    
    @property
    def untrained(self):
        return False


class KnowledgeGeography(Skill):
    
    def __init__(self, ranks=0):
        super(KnowledgeGeography, self).__init__("skill/knowledge-geography", ranks)
        LinkBuilder(self).is_modified_by("intelligence")
        
    @property
    def name(self):
        return "Knowledge (Geography)"
    
    @property
    def untrained(self):
        return False


class KnowledgeHistory(Skill):
    
    def __init__(self, ranks=0):
        super(KnowledgeHistory, self).__init__("skill/knowledge-history", ranks)
        LinkBuilder(self).is_modified_by("intelligence")
    
    @property
    def name(self):
        return "Knowledge (History)"
    
    @property
    def untrained(self):
        return False
    

class KnowledgeLocal(Skill):

    def __init__(self, ranks=0):
        super(KnowledgeLocal, self).__init__("skill/knowledge-local", ranks)
        LinkBuilder(self).is_modified_by("intelligence")
        LinkBuilder(self).modifies("skill/gather-information", bonus=SynergyModifier(self))
    
    @property
    def name(self):
        return "Knowledge (Local)"
    
    @property
    def untrained(self):
        return False
    

class KnowledgeNature(Skill):
    
    def __init__(self, ranks=0):
        super(KnowledgeNature, self).__init__("skill/knowledge-nature", ranks)
        LinkBuilder(self).is_modified_by("intelligence")
    
    @property
    def name(self):
        return "Knowledge (Nature)"
    
    @property
    def untrained(self):
        return False


class KnowledgeNobility(Skill):

    def __init__(self, ranks=0):
        super(KnowledgeNobility, self).__init__("skill/knowledge-nobility", ranks)
        LinkBuilder(self).is_modified_by("intelligence")
        LinkBuilder(self).modifies("skill/diplomacy", bonus=SynergyModifier(self))
    
    @property
    def name(self):
        return "Knowledge (Nobility)"
    
    @property
    def untrained(self):
        return False


class KnowledgeReligion(Skill):
    
    def __init__(self, ranks=0):
        super(KnowledgeReligion, self).__init__("skill/knowledge-religion", ranks)
        LinkBuilder(self).is_modified_by("intelligence")
        
    @property
    def name(self):
        return "Knowledge (Religion)"
    
    @property
    def untrained(self):
        return False
    

class KnowledgePlanes(Skill):
    
    def __init__(self, ranks=0):
        super(KnowledgePlanes, self).__init__("skill/knowledge-planes", ranks)
        LinkBuilder(self).is_modified_by("intelligence")
        
    @property
    def name(self):
        return "Knowledge (Planes)"
    
    @property
    def untrained(self):
        return False


class Listen(Skill):
    
    def __init__(self, ranks=0):
        super(Listen, self).__init__("skill/listen", ranks)
        LinkBuilder(self).is_modified_by("wisdom")
            
    @property
    def name(self):
        return "Listen"


class MoveSilently(Skill):
    
    def __init__(self, ranks=0):
        super(MoveSilently, self).__init__("skill/move-silently", ranks)
        LinkBuilder(self).is_modified_by("dexterity")

    @property
    def name(self):
        return "Move Silently"
    
    @property
    def armor_check_penalty(self):
        return 1
    

class OpenLock(Skill):
    
    def __init__(self, ranks=0):
        super(OpenLock, self).__init__("skill/open-lock", ranks)
        LinkBuilder(self).is_modified_by("dexterity")
        
    @property
    def name(self):
        return "Open Lock"
    
    @property
    def untrained(self):
        return False


class Perform(Skill):
    
    def __init__(self, qualifier, ranks=0):
        super(Craft, self).__init__("skill/perform-" + qualifier.lower(), ranks=ranks)
        LinkBuilder(self).is_modified_by("charisma")
        self.qualifier = qualifier
    
    @property
    def name(self):
        return "Perform (%s)" % self.qualifier

    
class Profession(Skill):

    def __init__(self, qualifier, ranks=0):
        super(Craft, self).__init__("skill/profession-" + self.qualifier.lower(), ranks=ranks)
        LinkBuilder(self).is_modified_by("wisdom")
        self.qualifier = qualifier

    @property
    def name(self):
        return "Profession (%s)" % self.qualifier

    @property
    def untrained(self):
        return False


class Ride(Skill):
    
    def __init__(self, ranks=0):
        super(Ride, self).__init__("skill/ride", ranks)
        LinkBuilder(self).is_modified_by("dexterity")
        
    @property
    def name(self):
        return "Ride"
    

class Search(Skill):

    def __init__(self, ranks=0):
        super(Search, self).__init__("skill/search", ranks)
        LinkBuilder(self).is_modified_by("intelligence")
    
    @property
    def name(self):
        return "Search"
    

class SenseMotive(Skill):
    
    def __init__(self, ranks=0):
        super(SenseMotive, self).__init__("skill/sense-motive", ranks)
        LinkBuilder(self).is_modified_by("wisdom")
        LinkBuilder(self).modifies("skill/diplomacy", bonus=SynergyModifier(self))
        
    @property
    def name(self):
        return "Sense Motive"
    
        
class SleightOfHand(Skill):

    def __init__(self, ranks=0):
        super(SleightOfHand, self).__init__("skill/sleight-of-hand", ranks)
        LinkBuilder(self).is_modified_by("dexterity")
    
    @property
    def name(self):
        return "Sleight Of Hand"
    
    @property
    def armor_check_penalty(self):
        return 1


class Spellcraft(Skill):

    def __init__(self, ranks=0):
        super(Spellcraft, self).__init__("skill/spellcraft", ranks)
        LinkBuilder(self).is_modified_by("intelligence")
    
    @property
    def name(self):
        return "Spellcraft"
    
    @property
    def untrained(self):
        return False
    

class Spot(Skill):
    
    def __init__(self, ranks=0):
        super(Spot, self).__init__("skill/spot", ranks)
        LinkBuilder(self).is_modified_by("wisdom")
        
    @property
    def name(self):
        return "Spot"
    

class Survival(Skill):
    
    def __init__(self, ranks=0):
        super(Survival, self).__init__("skill/survival", ranks)
        LinkBuilder(self).is_modified_by("wisdom")
        LinkBuilder(self).modifies("skill/knowledge-nature", bonus=SynergyModifier(self))
        
    @property
    def name(self):
        return "Survival"
    

class Swim(Skill):

    def __init__(self, ranks=0):
        super(Swim, self).__init__("skill/swim", ranks)
        LinkBuilder(self).is_modified_by("strength")
    
    @property
    def name(self):
        return "Swim"
    
    @property
    def armor_check_penalty(self):
        return 2


class Tumble(Skill):
    
    def __init__(self, ranks=0):
        super(Tumble, self).__init__("skill/tumble", ranks)
        LinkBuilder(self).is_modified_by("dexterity")
        LinkBuilder(self).modifies("skill/balance", "skill/jump", bonus=SynergyModifier(self))

    @property
    def name(self):
        return "Tumble"

    @property
    def armor_check_penalty(self):
        return 1

    @property
    def untrained(self):
        return False
    

class UseMagicDevice(Skill):
    
    def __init__(self, ranks=0):
        super(UseMagicDevice, self).__init__("skill/use-magic-device", ranks)
        LinkBuilder(self).is_modified_by("charisma")
        
    @property
    def name(self):
        return "Use Magic Device"
    
    @property
    def untrained(self):
        return False


class UseRope(Skill):
    
    def __init__(self, ranks=0):
        super(UseRope, self).__init__("skill/use-rope", ranks)
        LinkBuilder(self).is_modified_by("dexterity")
        
    @property
    def name(self):
        return "Use Rope"
    

def get_all_skill_classes():
    """Convenience function to return all Skill classes in an iterable."""
    from inspect import getmembers, getmodule, isclass
    classes = getmembers(getmodule(Skill), isclass)
    return [t[1] for t in classes if Skill in t[1].__bases__]
