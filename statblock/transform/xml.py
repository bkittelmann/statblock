from lxml import etree
from lxml.builder import ElementMaker


class StatblockTypeMap(dict):
    
    def add_object_as_text(self, elem, item):
        "Transforms object to a string and delegates to ElementMaker's text handling"
        self.get(str)(elem, str(item))
    
    def __nonzero__(self):
        "Necessary to signify in if-checks that this dict is used"
        return True
    
    def copy(self):
        "Return a copy of itself, if not overridden dict.copy would be used"
        return StatblockTypeMap(self.items())
    
    def get(self, key):
        """
        If the key is the type of an object in statblock's module, return a function
        that calls str() on the object first before adding the text output. Same happens
        for 'int' values.
        """   
        if key is int:
            return self.add_object_as_text
        if isinstance(key, object) and "statblock" in key.__module__:
            return self.add_object_as_text
        return super(StatblockTypeMap, self).get(key)
    

class XmlMarshaller():
    
    def __init__(self):
        self.element_maker = ElementMaker(typemap=StatblockTypeMap())

    
    def marshal(self, character):
        xml = self.element_maker
        root = xml.character(
            #--- first section ---
            xml.name(character.name),
            xml.gender(character.gender),
            self.write_type_info(character),
            
            xml.level(character.level),
            xml.alignment(character.alignment),
            xml.size(character.size),
            xml.initiative(character.initiative),
            self.write_skills(character),
            self.write_languages(character),
            
            #--- second section ---
            self.write_armor(character),
            xml("hit-points", character.hit_points),
            xml("hit-dice", self.format_hitdice(character.hit_dice)),
            self.write_saving_throws(character),
            
            #--- third section ---
            
            # this will most likely change with different movement methods
            xml.speed(character.speed),
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
            xml.type(character.type_info.type),
            xml.subtypes(
                *[xml.subtype(s) for s in character.type_info.subtypes]
            )
        )


    def write_skills(self, character):
        xml = self.element_maker
        return xml.skills(
            *[xml.skill(xml.value(s), name=s.name) for s in character.skills]
        )
    
    
    def write_armor(self, character):
        xml = self.element_maker
        return xml("armor-class",
            xml.value(character.armor_class),
            xml.touch(character.touch),
            xml("flat-footed", character.flat_footed)
        )
    
    
    def write_saving_throws(self, character):
        xml = self.element_maker
        return xml("saving-throws",
            xml.fortitude(character.saving_throws.fortitude),
            xml.reflex(character.saving_throws.reflex),
            xml.will(character.saving_throws.will)
        )
    
    
    def write_base_attacks(self, character):
        xml = self.element_maker
        return xml.attack(
            xml.base(character.attack.base),
            xml.grapple(character.attack.grapple)
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
            critical = xml.critical(weapon.critical.multiplier)
        
        return xml.weapon(
            xml.attack(combat.attack),
            xml.damage(combat.damage),
            critical,
            id=weapon.id(),
            name=weapon.name            
        )
    
    
    def write_abilities(self, character):
        xml, _ = self.element_maker, character.abilities
        return xml.abilities(
            xml.strength(_.strength),
            xml.dexterity(_.dexterity),
            xml.constitution(_.constitution),
            xml.intelligence(_.intelligence),
            xml.wisdom(_.wisdom),
            xml.charisma(_.charisma)
        )
    
    
    def write_feats(self, character):
        xml = self.element_maker
        return xml.feats(
            *[xml.feat(name=feat.name) for feat in character.feats]
        )
    

class XmlTransformer(object):
    
    def __init__(self):
        self.marshaller = XmlMarshaller()
    
    def toXml(self, character):
        element = self.toElement(character)
        return etree.tostring(element, pretty_print=True)
    
    def toElement(self, character):                    
        return self.marshaller.marshal(character)
    
    