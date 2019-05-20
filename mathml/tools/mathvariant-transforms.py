#!/usr/bin/python

from __future__ import print_function
from lxml import etree
from utils.misc import downloadWithProgressBar
from utils import mathfont
import json

# Retrieve the unicode.xml file if necessary.
unicodeXML = downloadWithProgressBar("http://www.w3.org/2003/entities/2007xml/unicode.xml")

# Extract the mathvariants transformation.
xsltTransform = etree.XSLT(etree.XML('''\
<xsl:stylesheet version="1.0"
                       xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:strip-space elements="*"/>
  <xsl:template match="charlist">
    <root><xsl:apply-templates select="character"/></root>
  </xsl:template>
  <xsl:template match="character">
    <xsl:if test="surrogate">
      <entry>
        <xsl:attribute name="mathvariant">
            <xsl:value-of select="surrogate/@mathvariant"/>
        </xsl:attribute>
        <xsl:attribute name="baseChar">
          <xsl:value-of select="surrogate/@ref"/>
        </xsl:attribute>
        <xsl:attribute name="transformedChar">
          <xsl:choose>
            <xsl:when test="bmp">
              <xsl:value-of select="bmp/@ref"/>
            </xsl:when>
            <xsl:otherwise>
               <xsl:value-of select="@id"/>
            </xsl:otherwise>
          </xsl:choose>
        </xsl:attribute>
      </entry>
    </xsl:if>
  </xsl:template>
</xsl:stylesheet>'''))

# Put the mathvariant transforms into a Python structure.
mathvariantTransforms = {}
root = xsltTransform(etree.parse(unicodeXML)).getroot()
def parseCodePoint(aHexaString):
    return int("0x%s" % aHexaString[1:], 16)
for entry in root:
    mathvariant = entry.get("mathvariant")
    baseChar = parseCodePoint(entry.get("baseChar"))
    transformedChar = parseCodePoint(entry.get("transformedChar"))
    if mathvariant not in mathvariantTransforms:
        mathvariantTransforms[mathvariant] = {}
    mathvariantTransforms[mathvariant][baseChar] = transformedChar

# There is no "isolated" mathvariant.
del mathvariantTransforms["isolated"]

# Create a WOFF font for each mathvariant.
for mathvariant in mathvariantTransforms:
    font = mathfont.create("mathvariant-%s" % mathvariant)
    for baseChar in mathvariantTransforms[mathvariant]:
        if baseChar not in font:
            mathfont.createGlyphFromValue(font, baseChar)
        transformedChar = mathvariantTransforms[mathvariant][baseChar]
        mathfont.createGlyphFromValue(font, transformedChar)
    mathfont.save(font)

# Create a MathML and CSS test for each mathvariant.
for mathvariant in mathvariantTransforms:
    print("Generating tests for %s..." % mathvariant, end="")
    reftest = open("../relations/css-styling/mathvariant-%s.html" % mathvariant, "w")
    reftestReference = open("../relations/css-styling/mathvariant-%s-ref.html" % mathvariant, "w")
    CSSreftest = open("../../css/css-text/text-transform/text-transform-math-%s-001.tentative.html" % mathvariant, "w")
    CSSreftestReference = open("../../css/css-text/text-transform/text-transform-math-%s-001.tentative-ref.html" % mathvariant, "w")
    source = '\
<!DOCTYPE html>\n\
<html>\n\
<head>\n\
<meta charset="utf-8"/>\n\
<title>%s</title>\n'
    reftest.write(source % ("mathvariant %s" % mathvariant))
    reftestReference.write(source % ("mathvariant %s (reference)" % mathvariant))
    CSSreftest.write(source % ("text-transform math-%s" % mathvariant))
    CSSreftestReference.write(source % ("text-transform math-%s (reference)" % mathvariant))
    source ='\
<link rel="help" href="https://mathml-refresh.github.io/mathml-core/#cssproperties"/>\n\
<link rel="match" href="mathvariant-%s-ref.html"/>\n\
<meta name="assert" content="Verify that a single-char <mtext> with a %s mathvariant is equivalent to an <mtext> with the transformed unicode character.">\n'
    reftest.write(source % (mathvariant, mathvariant))
    source = '\
<link rel="help" href="https://github.com/w3c/csswg-drafts/issues/3745"/>\n\
<link rel="match" href="text-transform-math-%s-001.tentative-ref.html"/>\n\
<meta name="assert" content="Verify that a character with \'text-transform: math-%s\' renders the same as the transformed unicode character.">\n'
    CSSreftest.write(source % (mathvariant, mathvariant))
    source = '\
<style>\n\
  @font-face {\n\
    font-family: TestFont;\n\
    src: url("/fonts/math/mathvariant-%s.woff");\n\
  }\n\
  body > span {\n\
    padding: 10px;\n\
  }\n\
  span > span {\n\
    font-family: monospace;\n\
    font-size: 10px;\n\
  }\n\
  .testfont {\n\
    font-family: TestFont;\n\
    font-size: 10px;\n\
  }\n\
</style>\n\
<body>\n\
  <!-- Generated by mathml/tools/mathvariant.py; DO NOT EDIT. -->\n\
  <p>Test passes if all the equalities below are true.</p>\n' % mathvariant
    reftest.write(source)
    reftestReference.write(source)
    CSSreftest.write(source)
    CSSreftestReference.write(source)
    charIndex = 0
    for baseChar in mathvariantTransforms[mathvariant]:
        transformedChar = mathvariantTransforms[mathvariant][baseChar]
        reftest.write('  <span><math class="testfont"><mtext mathvariant="%s">&#x%0X;</mtext></math>=<span>%05X</span></span>' % (mathvariant, baseChar, transformedChar))
        reftestReference.write('  <span><math class="testfont"><mtext>&#x%0X;</mtext></math>=<span>%05X</span></span>' % (transformedChar, transformedChar))
        CSSreftest.write('  <span><span class="testfont" style="text-transform: math-%s">&#x%0X;</span>=<span>%05X</span></span>' % (mathvariant, baseChar, transformedChar))
        CSSreftestReference.write('  <span><span class="testfont">&#x%0X;</span>=<span>%05X</span></span>' % (transformedChar, transformedChar))
        charIndex += 1
        if charIndex % 10 == 0:
            reftest.write('<br/>')
            reftestReference.write('<br/>')
            CSSreftest.write('<br/>')
            CSSreftestReference.write('<br/>')
        reftest.write('\n')
        reftestReference.write('\n')
        CSSreftest.write('\n')
        CSSreftestReference.write('\n')
    source = '</body>\n</html>\n'
    reftest.write(source)
    reftestReference.write(source)
    CSSreftest.write(source)
    CSSreftestReference.write(source)
    reftest.close()
    reftestReference.close()
    CSSreftest.close()
    CSSreftestReference.close()
    print(" done.")
