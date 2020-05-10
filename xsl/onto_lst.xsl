<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                version="1.0">


<!-- (c) 2013 che Wolfram Diestel
     licenco GPL 2.0

     enigo : indekso.xml, kreita per "ant -f $VOKO/ant/indeksoj.xml inx-eltiro"
     eligo : tezauro en TTL lau skemo Voko+SKOS, vd. voko.owl, http://www.w3.org/TR/skos-reference/

-->


<xsl:output method="text" encoding="utf-8" indent="no"/>
<xsl:strip-space elements="kap art drv subdrv snc subsnc trd"/>

<xsl:variable name="apos">'</xsl:variable>
<xsl:variable name="quot">"</xsl:variable>

<xsl:variable name="klasoj">../cfg/klasoj.xml</xsl:variable>
<xsl:variable name="klasoj-root" select="document($klasoj)"/>

<xsl:variable name="root" select="/"/>

<!-- <xsl:key name="klasoj" match="$klasojroot/klasoj//kls" use="@nom"/> -->


<xsl:template match="/">
<xsl:text>@prefix skos: &lt;http://www.w3.org/2004/02/skos/core#&gt; .
@prefix rdf:  &lt;http://www.w3.org/1999/02/22-rdf-syntax-ns#&gt; .
@prefix rdfs: &lt;http://www.w3.org/2000/01/rdf-schema#&gt; .
@prefix owl:  &lt;http://www.w3.org/2002/07/owl#&gt; .
@prefix dct:  &lt;http://purl.org/dc/terms/&gt; .
@prefix voko: &lt;http://purl.org/net/voko#&gt; .
@prefix revo: &lt;http://purl.org/net/voko/revo#&gt; .

</xsl:text>

  <xsl:for-each select="$klasoj-root">
    <xsl:call-template name="klasoj"/>
  </xsl:for-each>
</xsl:template>


<xsl:template name="klasoj">
  <xsl:for-each select="//kls">
     <xsl:variable name="kls" select="concat('voko:',substring-after(@nom,'#'))"/>

     <!-- klasoj povas aperi plurloke en la hierarkio, sed nur unufoje
    traktighu tie chi -->
    <xsl:if test="not(preceding::kls[@nom=current()/@nom]) and $root//ref[@lst=$kls]">

      <xsl:value-of select="concat('&lt;',@nom,'&gt;')"/>
<xsl:text> skos:member 
</xsl:text> 
		  
      <xsl:for-each select="$root">
	<xsl:call-template name="klasanoj">
	  <xsl:with-param name="klaso" select="$kls"/>
	</xsl:call-template>
      </xsl:for-each>

<xsl:text>. 

</xsl:text>
    </xsl:if>
  </xsl:for-each>
</xsl:template>


<xsl:template name="klasanoj">
  <xsl:param name="klaso"/>

  <xsl:for-each select="//ref[@lst=$klaso]">
<!-- ordigo necesas nur che OrderdCollection, sed tiam lau @val 
    <xsl:sort lang="eo"
	      collation="http://saxon.sf.net/collation?class=de.steloj.respiro.EsperantoCollator" 
	      select="translate(k,'-( )','')"/> -->

      <xsl:call-template name="ancestor-mrk"/>
      <xsl:if test="following::ref[@lst=$klaso]">
        <xsl:text>,
</xsl:text>
      </xsl:if>
  </xsl:for-each>
</xsl:template>



<xsl:template name ="ancestor-mrk">
  <xsl:value-of select="concat('revo:',
			translate(
			ancestor-or-self::node()[@mrk][1]/@mrk,
			'.','_'))"/>
</xsl:template>


</xsl:stylesheet>









