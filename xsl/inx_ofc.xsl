<!DOCTYPE xsl:transform>

<xsl:transform
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:saxon="http://saxon.sf.net/"
  version="2.0"
  extension-element-prefixes="saxon" 
>


<!-- (c) 2018 che Wolfram Diestel
     permesilo: GPL 2.0
-->

<xsl:param name="verbose" select="false"/>

<xsl:output method="xml" encoding="utf-8" indent="yes"/>
<xsl:strip-space elements="kap rad var"/>

<xsl:template match="/">
  <indekso>

    <!-- oficialaj kapvortoj -->
      <xsl:call-template name="oficialaj">
        <xsl:with-param name="ofc" select="'*'"/>
      </xsl:call-template>
      <xsl:call-template name="oficialaj">
        <xsl:with-param name="ofc" select="'1'"/>
      </xsl:call-template>
      <xsl:call-template name="oficialaj">
        <xsl:with-param name="ofc" select="'2'"/>
      </xsl:call-template>
      <xsl:call-template name="oficialaj">
        <xsl:with-param name="ofc" select="'3'"/>
      </xsl:call-template>
      <xsl:call-template name="oficialaj">
      </xsl:call-template>
      <xsl:call-template name="oficialaj">
        <xsl:with-param name="ofc" select="'4'"/>
      </xsl:call-template>
      <xsl:call-template name="oficialaj">
        <xsl:with-param name="ofc" select="'5'"/>
      </xsl:call-template>
      <xsl:call-template name="oficialaj">
        <xsl:with-param name="ofc" select="'6'"/>
      </xsl:call-template>
      <xsl:call-template name="oficialaj">
        <xsl:with-param name="ofc" select="'7'"/>
      </xsl:call-template>
      <xsl:call-template name="oficialaj">
        <xsl:with-param name="ofc" select="'8'"/>
      </xsl:call-template>
      <xsl:call-template name="oficialaj">
        <xsl:with-param name="ofc" select="'9'"/>
      </xsl:call-template>

  </indekso>
</xsl:template>



<xsl:template name="oficialaj">
  <xsl:param name="ofc"/> 
  <radikoj ofc="{$ofc}">
    <xsl:for-each select="//art/kap[ofc=$ofc]/rad|//art/kap/var/kap[ofc=$ofc]/rad">
      <xsl:sort collation="http://saxon.sf.net/collation?class=de.steloj.respiro.EsperantoCollator" lang="eo" select="."/>
      <r><xsl:apply-templates/></r>
    </xsl:for-each>
  </radikoj>
  <vortoj ofc="{$ofc}">
    <xsl:for-each select="//art//drv/kap[ofc=$ofc]|//art//drv//var/kap[ofc=$ofc]">
      <!-- xsl:sort collation="http://saxon.sf.net/collation?class=de.steloj.respiro.EsperantoCollator" lang="eo" select="text()|tld"/ -->
      <k><xsl:apply-templates select="text()|tld"/></k>
    </xsl:for-each>
  </vortoj>
</xsl:template>

<xsl:template match="tld">
  <xsl:choose>

    <xsl:when test="@lit">
      <xsl:value-of select="concat(@lit,substring(ancestor::art/kap/rad,2))"/>
    </xsl:when>

    <xsl:otherwise>
      <xsl:value-of select="ancestor::art/kap/rad"/>
    </xsl:otherwise>

  </xsl:choose>
</xsl:template>


<xsl:template match="text()">
  <xsl:value-of select="normalize-space(translate(.,',',''))"/>
</xsl:template>

<xsl:template match="fnt|ofc"/>



</xsl:transform>













