<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"
    xmlns:py="http://github/bkittelmann/statblock"
    exclude-result-prefixes="py"
>
    <xsl:output method="xml" indent="yes"/>
    <xsl:variable name="value-format" select="'+#;-#'"/>
    
    <xsl:template match="/">
        <html>
            <head>
                <title>Statblock</title>
                <!--<link rel="stylesheet" type="text/css" href="styles/default.css"/>-->
                <style type="text/css">
                    <xsl:value-of select="document('default.css')"/>
                </style>
            </head>
            <body>
                <div id="stats">
                    <xsl:apply-templates/>
                </div>
            </body>
        </html>            
    </xsl:template>
    
    <xsl:template match="character">
        <div style="margin-left:0;">
            <h1>
                <xsl:value-of select="name"/>
            </h1>
            <xsl:call-template name="section-general"/>
            <hr/>
            <xsl:call-template name="section-defense"/>
            <hr/>
            <xsl:call-template name="section-attack"/>
            <hr/>
            <xsl:call-template name="section-abilities"/>
            <hr/>
        </div>
    </xsl:template>
    
    <!-- section bases -->
    
    <xsl:template name="section-general">
        <xsl:call-template name="basic-information"/>
        <br/>
        <xsl:call-template name="alignment-and-type"/>
        <br/>
        <xsl:call-template name="initiative-and-senses"/>
        <br/>
        <xsl:call-template name="languages"/>
    </xsl:template>
    
    <xsl:template name="section-defense">
        <xsl:call-template name="armor">
            <xsl:with-param name="node" select="armor-class"/>
        </xsl:call-template>
        <br/>
        <xsl:call-template name="hit-points"/>
        <br/>
        <xsl:call-template name="saving-throws"/>
    </xsl:template>
    
    <xsl:template name="section-attack">
        <xsl:call-template name="speed"/>
        <br/>
        <xsl:apply-templates select="melee"/>
        <br/>
        <xsl:apply-templates select="ranged"/>
        <br/>
        <xsl:call-template name="base-attacks"/>
    </xsl:template>
    
    <xsl:template name="section-abilities">
        <xsl:apply-templates select="abilities"/>
        <br/>
        <xsl:apply-templates select="feats"/>
        <br/>
        <xsl:call-template name="filtered-skills"/>
        <br/>
        <xsl:apply-templates select="equipment"/>
    </xsl:template>
    
    <!-- first section -->
    
    <xsl:template name="basic-information">
        <span>
            <xsl:value-of select="gender"/>
            <xsl:text> </xsl:text>
            <xsl:value-of select="type-info/name"/>
            <xsl:text> </xsl:text>
            <xsl:value-of select="level"/>
        </span>
    </xsl:template>
    
    <xsl:template name="alignment-and-type">
        <span>
            <xsl:value-of select="alignment"/>
            <xsl:text> </xsl:text>
            
            <xsl:value-of select="size"/>
            <xsl:text> </xsl:text>
            
            <xsl:value-of select="type-info/type"/>
            
            <xsl:if test="type-info/subtypes">
                <xsl:text> (</xsl:text>
                <xsl:value-of select="py:join(', ', type-info/subtypes/subtype)"/>
                <xsl:text>)</xsl:text>
            </xsl:if>
        </span>
    </xsl:template>
    
    <xsl:template name="initiative-and-senses">
        <span>
            <b>Init</b>
            <xsl:value-of select="concat(' ', format-number(initiative, $value-format), '; ')"/> 
            <b>Senses</b>
            <xsl:text> Listen </xsl:text>
            <xsl:value-of select="format-number(skills/skill[@name='Listen']/value, $value-format)"/>
            <xsl:text>, Spot </xsl:text>
            <xsl:value-of select="format-number(skills/skill[@name='Spot']/value, $value-format)"/>
        </span>
    </xsl:template>
    
    <xsl:template name="languages">
        <span>
            <b>Languages</b>
            <xsl:text> </xsl:text>
            <xsl:value-of select="py:join(', ', languages/language)"/>
        </span>
    </xsl:template>
    
    <!-- second section -->
    
    <xsl:template name="armor">
        <xsl:param name="node"/>
        <span>
            <b>AC</b>
            <xsl:text> </xsl:text>
            <xsl:value-of select="$node/value"/>
            <xsl:text>, touch </xsl:text>
            <xsl:value-of select="$node/touch"/>
            <xsl:text>, flat-footed </xsl:text>
            <xsl:value-of select="$node/flat-footed"/>
        </span>
    </xsl:template>
    
    <xsl:template name="hit-points">
        <span>
            <b>hp</b>
            <xsl:text> </xsl:text>
            <xsl:value-of select="hit-points"/>
            <xsl:text> (</xsl:text>
            <xsl:value-of select="hit-dice"/>
            <xsl:text>)</xsl:text>
        </span>
    </xsl:template>
    
    <xsl:template name="saving-throws">
        <span>
            <b>Fort</b>
            <xsl:text> </xsl:text>
            <xsl:value-of select="format-number(saving-throws/fortitude, $value-format)"/>
            <xsl:text>, </xsl:text>
            <b>Ref</b>
            <xsl:text> </xsl:text>
            <xsl:value-of select="format-number(saving-throws/reflex, $value-format)"/>
            <xsl:text>, </xsl:text>
            <b>Will</b>
            <xsl:text> </xsl:text>
            <xsl:value-of select="format-number(saving-throws/will, $value-format)"/>
        </span>
    </xsl:template>
    
    <!-- third section -->
    
    <xsl:template name="speed">
        <span>
            <b>Speed</b>
            <xsl:text> </xsl:text>
            <xsl:value-of select="speed"/>
            <xsl:text> ft.</xsl:text>
        </span>
    </xsl:template>
    
    <xsl:template match="melee/attack">
        <span>
            <b>Melee</b> 
            <xsl:text> </xsl:text>
            <xsl:apply-templates select="weapon"/>                
        </span>
    </xsl:template>
    
    <xsl:template match="ranged/attack">
        <span>
            <b>Ranged</b> 
            <xsl:text> </xsl:text>
            <xsl:apply-templates select="weapon"/>                
        </span>
    </xsl:template>
    
    <xsl:template match="weapon">
        <xsl:value-of select="@name"/>
        <xsl:text> </xsl:text>
        <xsl:value-of select="format-number(attack, $value-format)"/>
        <xsl:text> (</xsl:text>
        <xsl:value-of select="damage"/>
        <xsl:apply-templates select="critical"/>
        <xsl:text>)</xsl:text>
    </xsl:template>
    
    <xsl:template match="critical">
        <xsl:text>/</xsl:text>
        <!-- check if the value is a multiplier -->
        <xsl:if test="not(contains(., '-'))">
            <xsl:text>x</xsl:text>
        </xsl:if>
        <xsl:value-of select="."/>
    </xsl:template>
    
    <xsl:template name="base-attacks">
        <span>
            <b>Base Atk</b> 
            <xsl:text> </xsl:text>
            <xsl:value-of select="format-number(attack/base, $value-format)"/>
            <xsl:text>; </xsl:text>
            <b>Grp</b> 
            <xsl:text> </xsl:text>
            <xsl:value-of select="format-number(attack/grapple, $value-format)"/>
        </span>
    </xsl:template>
    
    <!-- fourth section -->
    
    <xsl:template match="abilities">
        <span>
            <b>Abilities</b>
            <xsl:for-each select="*">
                <xsl:text> </xsl:text>
                <xsl:value-of select="py:upper(substring(name(), 1, 1))"/>
                <xsl:value-of select="concat(substring(name(), 2, 2), ' ', .)"/>
                <xsl:if test="position() != last()">
                    <xsl:text>, </xsl:text>
                </xsl:if>
            </xsl:for-each>
        </span>
    </xsl:template>
    
    <xsl:template match="feats">
        <span>
            <b>Feats</b>
            <xsl:for-each select="*">
                <xsl:value-of select="@name"/>
                <xsl:if test="position() != last()">
                    <xsl:text>, </xsl:text>
                </xsl:if>
            </xsl:for-each>
        </span>
    </xsl:template>
    
    <xsl:template name="filtered-skills">
        <span>
            <b>Skills</b>
            <xsl:text> </xsl:text>
            <xsl:for-each select="skills/skill[number(value) >= 2]">
                <xsl:value-of select="@name"/>
                <xsl:text> </xsl:text>
                <xsl:value-of select="format-number(value, $value-format)"/>
                <xsl:if test="position() != last()">
                    <xsl:text>, </xsl:text>
                </xsl:if>
            </xsl:for-each>
        </span>
    </xsl:template>
    
    <xsl:template match="equipment">
        <!-- TODO        
        <span>
            <b>Posessions</b>
        </span>
        -->
    </xsl:template>
    
</xsl:stylesheet>
