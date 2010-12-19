from lxml import etree
from lxml.builder import ElementMaker
from xsl import XslRenderer

class XmlMarshaller():
    
    def __init__(self):
        self.element_maker = ElementMaker()

    
    def marshal(self, character):
        xml = self.element_maker
        root = xml.character(
            #--- first section ---
            xml.name(character.name),
            xml.gender(character.gender),
            self.write_type_info(character),
            
            xml.level(character.level),
            xml.alignment(str(character.alignment)),
            xml.size(str(character.size)),
            xml.initiative(str(character.initiative.value)),
            self.write_skills(character),
            self.write_languages(character),
            
            #--- second section ---
            self.write_armor(character),
            xml("hit-points", str(character.hit_points.value)),
            xml("hit-dice", self.format_hitdice(character.hit_dice)),
            self.write_saving_throws(character),
            
            #--- third section ---
            
            # this will most likely change with different movement methods
            xml.speed(str(character.speed)),
            self.write_base_attacks(character),
            self.write_melee(character),
            self.write_ranged(character),
            
            #--- fourth section --
            self.write_abilities(character),
            self.write_feats(character),
            xml.equipment("")
        )
        
        etree.cleanup_namespaces(root)
        return root
    
    
    def format_hitdice(self, hit_dice):
        return "%s HD" % hit_dice.multiplicator
    
    
    def write_languages(self, character):
        xml = self.element_maker
        return xml.languages(
            *[xml.language(lang) for lang in character.languages]
        )
    
    
    def write_type_info(self, character):
        xml = self.element_maker
        return xml("type-info",
            xml.name(character.type_info.name),
            xml.type(str(character.type_info.type)),
            xml.subtypes(
                *[xml.subtype(s) for s in character.type_info.subtypes]
            )
        )


    def write_skills(self, character):
        xml = self.element_maker
        return xml.skills(
            *[xml.skill(xml.value(str(s.value)), name=s.name) for s in character.skills]
        )
    
    
    def write_armor(self, character):
        xml = self.element_maker
        return xml("armor-class",
            xml.value(str(character.armor_class.value)),
            xml.touch(str(character.touch.value)),
            xml("flat-footed", str(character.flat_footed.value))
        )
    
    
    def write_saving_throws(self, character):
        xml = self.element_maker
        return xml("saving-throws",
            xml.fortitude(str(character.saving_throws.fortitude.value)),
            xml.reflex(str(character.saving_throws.reflex.value)),
            xml.will(str(character.saving_throws.will.value))
        )
    
    
    def write_base_attacks(self, character):
        xml = self.element_maker
        return xml.attack(
            xml.base(str(character.attack.base.value)),
            xml.grapple(str(character.attack.grapple.value))
        )       

    
    def write_melee(self, character):
        melee = etree.Element("melee")
        self.write_single_attacks(melee, character.melee, "melee")
        return melee


    def write_ranged(self, character):
        ranged = etree.Element("ranged")
        self.write_single_attacks(ranged, character.ranged, "ranged")
        return ranged
    
    
    def write_single_attacks(self, container, attack_list, kind):
        for attack in attack_list:
            attack_elem = etree.Element("attack")
            for weapon in attack.weapons:
                attack_elem.append(self.write_weapon(weapon, kind))
            container.append(attack_elem)


    def write_weapon(self, weapon, kind):
        xml = self.element_maker
        combat = weapon.ranged if kind == "ranged" else weapon.melee
        
        if len(weapon.critical.range) > 1:
            critical = xml.critical("%s-%s" % (weapon.critical.range[0], weapon.critical.range[-1]))
        elif weapon.critical.multiplier > 1:
            critical = xml.critical(str(weapon.critical.multiplier))
        
        return xml.weapon(
            xml.attack(str(combat.attack.value)),
            xml.damage(str(combat.damage.value)),
            critical,
            id=weapon.id(),
            name=weapon.name            
        )
    
    
    def write_abilities(self, character):
        xml = self.element_maker
        return xml.abilities(
            xml.strength(str(character.abilities.strength.value)),
            xml.dexterity(str(character.abilities.dexterity.value)),
            xml.constitution(str(character.abilities.constitution.value)),
            xml.intelligence(str(character.abilities.intelligence.value)),
            xml.wisdom(str(character.abilities.wisdom.value)),
            xml.charisma(str(character.abilities.charisma.value))
        )
    
    
    def write_feats(self, character):
        xml = self.element_maker
        return xml.feats(
            *[xml.feat(name=feat.name) for feat in character.feats]
        )
    

class XmlTransformer(object):
    
    def __init__(self):
        self.marshaller = XmlMarshaller()
        self.xsl = XslRenderer()
    
    def toXml(self, character):
        element = self.toElement(character)
        return etree.tostring(element, pretty_print=True)
    
    
    def toXhtml(self, character):
        element = self.toElement(character)
        output = self.xsl.render(element, "styles/xhtml.xsl")
        return etree.tostring(output, pretty_print=True)
    
    
    def toElement(self, character):                    
        return self.marshaller.marshal(character)
    
    