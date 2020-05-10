<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
		version="1.0">


<!-- (c) 1999-2003 che Wolfram Diestel 
     licenco GPL 2.0

eltiras informojn por la sercho. Uzas la eltirilon por la
indeksoj, sed aldonas iujn regulojn

-->

<xsl:import href="inx_eltiro.xsl"/>

<xsl:template match="uzo[@tip]">
  <xsl:copy-of select="."/>
</xsl:template>

<xsl:template match="art">
  <art mrk="{substring-after(substring-before(@mrk,'.xml'),'Id: ')}">
  <xsl:apply-templates select="kap|subart|drv|snc|trdgrp|trd|uzo|bld|dif|ekz|
tezrad|gra"/>
  </art>
</xsl:template>

<xsl:template match="subart|drv|subdrv|snc|subsnc">
  <xsl:copy>
  <xsl:apply-templates select="@mrk|kap|drv|subdrv|snc|subsnc|trdgrp|trd
          |uzo|bld|dif|ekz|mlg|refgrp|ref|tezrad|gra"/>
  </xsl:copy>
</xsl:template>

<xsl:template match="gra">
  <xsl:apply-templates select="vspec"/>
</xsl:template>

<xsl:template match="vspec">
  <xsl:copy-of select="."/>
</xsl:template>

</xsl:stylesheet>
