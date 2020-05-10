<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:xt="http://www.jclark.com/xt"
		version="1.0"
                extension-element-prefixes="xt">

<xsl:output method="xml" encoding="utf-8" indent="yes"/>

<!--

(c) 2016, Wolfram Diestel

uzata kiel bibliografia listo por Revo-redaktilo

-->

<xsl:template match="/">
    <xsl:apply-templates/>
</xsl:template>

<!-- art, subart -->

<xsl:template match="bibliografio">
  <bibliografio>
    <xsl:apply-templates select="vrk">
      <xsl:sort select="@mll"/>
    </xsl:apply-templates>
  </bibliografio>
</xsl:template>

<xsl:template match="vrk">
  <vrk>
    <bib>
      <xsl:value-of select="@mll"/>
    </bib>
    <xsl:apply-templates select="url"/>
    <text>
      <xsl:apply-templates select="aut|trd|tit"/>
    </text>
  </vrk>
</xsl:template>

<xsl:template match="url">
  <url>
    <xsl:apply-templates/>
  </url>
</xsl:template>

<xsl:template match="aut">
  <xsl:apply-templates/>
  <xsl:choose>
    <xsl:when test="following-sibling::*[1][self::aut]">
      <xsl:text>; </xsl:text>
    </xsl:when>
    <xsl:when test="following-sibling::*[1][self::trd]">
      <xsl:text>, </xsl:text>
    </xsl:when>
    <xsl:when test="following-sibling::*[1][self::tit]">
      <xsl:text>: </xsl:text>
    </xsl:when>
  </xsl:choose>
</xsl:template>

<xsl:template match="trd">
  <xsl:text>trad. </xsl:text>
  <xsl:apply-templates/>
  <xsl:if test="following-sibling::*[1][self::tit]">
      <xsl:text>: </xsl:text>
  </xsl:if>
</xsl:template>

<xsl:template match="tit">
  <xsl:apply-templates/>
  <!--
  <xsl:if test="following-sibling::*[1][self::eld|self::isbn]">
      <xsl:text>, </xsl:text>
      </xsl:if>
      -->
</xsl:template>

<xsl:template match="ald"/>
<xsl:template match="eld"/>

<!--
<xsl:template match="isbn">
  <xsl:text> ISBN: </xsl:text>
  <xsl:apply-templates/>
  <xsl:if test="following-sibling::*[1][self::eld|self::ald]">
      <xsl:text>, </xsl:text>
  </xsl:if>
</xsl:template>

<xsl:template match="ald">
  (<xsl:apply-templates/>)
  <xsl:if test="following-sibling::*">
      <xsl:text>, </xsl:text>
  </xsl:if>
</xsl:template>

<xsl:template match="eld">
  <xsl:apply-templates/>
  <xsl:text> </xsl:text>
</xsl:template>

<xsl:template match="nom">
  <xsl:apply-templates/>
  <xsl:if test="following-sibling::*">
      <xsl:text>, </xsl:text>
  </xsl:if>
</xsl:template>  

<xsl:template match="lok">
  <xsl:apply-templates/>
  <xsl:if test="following-sibling::*">
    <xsl:text>, </xsl:text>
  </xsl:if>
</xsl:template>

<xsl:template match="dat">
  <xsl:apply-templates/>
</xsl:template>
-->

</xsl:stylesheet>











