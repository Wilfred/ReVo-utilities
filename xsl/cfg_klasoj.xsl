<!DOCTYPE stylesheet [
  <!ENTITY voko "http://purl.org/net/voko#" >
  <!ENTITY skos "http://www.w3.org/2004/02/skos/core#" >
]>


<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
     xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
     xmlns:voko="http://purl.org/net/voko#"
     xmlns:owl="http://www.w3.org/2002/07/owl#"
     xmlns:xsd="http://www.w3.org/2001/XMLSchema#"
     xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
     xmlns:skos="http://www.w3.org/2004/02/skos/core#"
                version="1.0">


<!-- (c) 2013 che Wolfram Diestel
     licenco GPL 2.0

     enigo : voko.rdf, kreita per "ant -f $VOKO/ant/medio.xml med-klasoj"
     eligo : listo de klasoj

-->


<xsl:output method="xml" encoding="utf-8" indent="yes"/>

<xsl:template match="/">
  <klasoj>
  <xsl:call-template name="subklasoj">
    <xsl:with-param
	name="bazoklaso">http://www.w3.org/2004/02/skos/core#Collection</xsl:with-param>
    <xsl:with-param name="indent">  </xsl:with-param>
  </xsl:call-template>
  </klasoj>
</xsl:template>


<xsl:template name="subklasoj">
  <xsl:param name="bazoklaso"/>
  <xsl:param name="indent"/>
  <xsl:for-each
      select="//owl:Class[rdfs:subClassOf/@rdf:resource=$bazoklaso]">
    <xsl:sort lang="eo" select="@rdf:about"/>
    <xsl:value-of select="$indent"/>
    <kls nom="{@rdf:about}">

    <!-- ordigitaj klasanoj? -->
    <xsl:if test="rdfs:subClassOf[@rdf:resource='&skos;OrderedCollection']">
      <xsl:attribute name="ordigita">
        <xsl:value-of select="'jes'"/>
      </xsl:attribute>
    </xsl:if>

    <xsl:if test="rdfs:seeAlso">
      <xsl:attribute name="mrk">
        <xsl:value-of select="rdfs:seeAlso/@rdf:resource"/>
      </xsl:attribute>    
    </xsl:if>

    <xsl:if test="voko:prezento">

      <!-- integrita prezento de klasoj -->
      <xsl:if test="voko:prezento='integrita' and
              count(rdfs:subClassOf[starts-with(@rdf:resource,'&voko;')])>1">
              <xsl:message>
                <xsl:text>AVERTO: integrita prezento de klaso &quot;</xsl:text>
          <xsl:value-of select="@rdf:about"/>
          <xsl:text>&quot; povas kauzi problemojn, char </xsl:text>
          <xsl:text>ghi havas pli ol unu superklason!</xsl:text>
        </xsl:message>
      </xsl:if>

         <xsl:attribute name="prezento">
           <xsl:value-of select="voko:prezento"/>
         </xsl:attribute>
    </xsl:if><xsl:text>
</xsl:text>

    <!-- traktu subklasojn -->
    <xsl:call-template name="subklasoj">
      <xsl:with-param name="bazoklaso">
        <xsl:value-of select="@rdf:about"/>
      </xsl:with-param>
      <xsl:with-param name="indent">
        <xsl:value-of select="concat($indent,'  ')"/>
      </xsl:with-param>
    </xsl:call-template>
  <xsl:value-of select="$indent"/>

  </kls><xsl:text>
</xsl:text>

  </xsl:for-each>
 
</xsl:template>

</xsl:stylesheet>

