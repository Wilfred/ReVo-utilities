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

<xsl:template match="/">
<xsl:text>@prefix skos: &lt;http://www.w3.org/2004/02/skos/core#&gt; .
@prefix rdf:  &lt;http://www.w3.org/1999/02/22-rdf-syntax-ns#&gt; .
@prefix rdfs: &lt;http://www.w3.org/2000/01/rdf-schema#&gt; .
@prefix owl:  &lt;http://www.w3.org/2002/07/owl#&gt; .
@prefix dct:  &lt;http://purl.org/dc/terms/&gt; .
@prefix voko: &lt;http://purl.org/net/voko#&gt; .
@prefix revo: &lt;http://purl.org/net/voko/revo#&gt; .

revo:revoScheme rdf:type skos:ConceptScheme;
   dct:title "Teza&#x016d;ro de Reta Vortaro"@eo. 

revo:revoScheme owl:imports &lt;http://purl.org/net/voko&gt; .
</xsl:text>
  <xsl:apply-templates/>
</xsl:template>

<xsl:template match="art">
  <xsl:apply-templates select="subart|drv|snc"/>
</xsl:template>

<xsl:template match="subart|drv|subdrv">
  <xsl:apply-templates select="drv|subdrv|snc|subsnc"/>
</xsl:template>


<xsl:template match="drv">
  <xsl:variable name="mrk"><xsl:value-of
  select="translate(@mrk,'.','_')"/></xsl:variable>

  <xsl:if test=".//tezrad or .//ref">
revo:<xsl:value-of select="$mrk"/> rdf:type voko:deriva&#x0135;o ;
  voko:kap "<xsl:apply-templates
 select="ancestor-or-self::node()[self::art or self::drv][kap][1]/kap"/>"@eo .
      <xsl:if test=".//tezrad">
         <xsl:comment>###TEZRAD###</xsl:comment>
      </xsl:if>
      <xsl:if test=".//uzo">
<!-- TODO: distingu fak, stl kaj alia uzo -->
revo:<xsl:value-of select="$mrk"/> voko:uzo "<xsl:value-of select=".//uzo"/>" .
      </xsl:if>
 
      <xsl:for-each select="(trd|snc/trd)[@lng='de' or @lng='en' or @lng='ru'
			    or @lng='fr' or @lng='hu' or @lng='nl' or @lng='la']">
revo:<xsl:value-of select="$mrk"/> voko:trd "<xsl:value-of
	select="translate(normalize-space(.),$quot,$apos)"/>"@<xsl:value-of select="@lng"/> .
      </xsl:for-each>

      <xsl:call-template name="super"/>
      <xsl:call-template name="sub"/>
      <xsl:call-template name="sin"/>
      <xsl:call-template name="dif"/>
      <xsl:call-template name="vid"/>
      <xsl:call-template name="ant"/>
      <xsl:call-template name="malprt"/>
      <xsl:call-template name="prt"/>
      <xsl:call-template name="ekz"/>
      <xsl:call-template name="lst"/>
  </xsl:if>

  <xsl:apply-templates select="snc"/>
</xsl:template>


<xsl:template match="snc|subsnc">

<!-- TODO: chu ghustas, ke foje @mrk, foje tez-mrk-n estas uzata tie chi
sekve? Vershajne funkcias nur se cheestas @mrk, do prefere uzu tez-mrk-n 
chie en tiu chi template! -->
    <xsl:variable name="mrk"><xsl:value-of select="translate(@mrk,'.','_')"/></xsl:variable>

    <!-- kreu novan nodon -->
revo:<xsl:call-template name="tez-mrk-n"/> rdf:type voko:senco ;
  <!-- el sencoj referencu al la derivajho -->
  voko:drv revo:<xsl:value-of 
    select="translate(ancestor-or-self::node()[self::art or self::drv][1]/@mrk,'.','_')"/> ;

<!-- TODO: kapvorto sufichas che derivajho, che sencoj, kaj nur tie, aldonu
sencnumeron -->
  voko:kap "<xsl:apply-templates
  select="ancestor-or-self::node()[self::art or self::drv][kap][1]/kap"/>"@eo .

  <xsl:if test="count(../snc)+count(../subsnc) &gt; 1">
revo:<xsl:value-of select="$mrk"/> voko:snc-n-ro "<xsl:number from="drv|subart"
level="multiple" count="snc|subsnc" format="1.a"/>" .
  </xsl:if> 

      <xsl:if test=".//tezrad">
         <xsl:comment>###TEZRAD###</xsl:comment>
      </xsl:if>
      <xsl:if test=".//uzo">
<!-- TODO: distingu fak, stl kaj alia uzo! -->
revo:<xsl:value-of select="$mrk"/> voko:uzo "<xsl:value-of select=".//uzo"/>" .
      </xsl:if>

      <xsl:for-each select="trd[@lng='de' or @lng='en' or @lng='ru'
			    or @lng='fr' or @lng='hu' or @lng='nl' or @lng='la']">
revo:<xsl:value-of select="$mrk"/> voko:trd "<xsl:value-of
	select="translate(normalize-space(.),$quot,$apos)"/>"@<xsl:value-of select="@lng"/> .
      </xsl:for-each>

      <xsl:call-template name="super"/>
      <xsl:call-template name="sub"/>
      <xsl:call-template name="sin"/>
      <xsl:call-template name="dif"/>
      <xsl:call-template name="vid"/>
      <xsl:call-template name="ant"/>
      <xsl:call-template name="malprt"/>
      <xsl:call-template name="prt"/>
      <xsl:call-template name="ekz"/>
      <xsl:call-template name="lst"/>
  <!--   </xsl:if> -->
  <xsl:apply-templates select="subsnc"/>
</xsl:template>


<xsl:template name="tez-mrk-n">
   <xsl:choose>
      <xsl:when test="@mrk">
        <xsl:value-of select="translate(@mrk,'.','_')"/>
      </xsl:when>

      <xsl:otherwise>
          <xsl:value-of select="translate(ancestor::node()[@mrk][1]/@mrk,'.','_')"/>
          <xsl:text>.</xsl:text>
          <xsl:number from="drv|subart" level="multiple" count="snc|subsnc" format="1.a"/>
      </xsl:otherwise>
   </xsl:choose>
</xsl:template>

<!-- xsl:template match="snc|subsnc"/ --> <!-- ignoru sen @mrk -->


<xsl:template match="kap">
   <xsl:variable name="kap"><xsl:apply-templates select="text()|rad|tld"/></xsl:variable>
   <xsl:value-of select="translate(normalize-space($kap),'/,','')"/>
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


<xsl:template name="super">
    <xsl:for-each select="ref[@tip='super']">
revo:<xsl:call-template name="ancestor-mrk"/>
       voko:super revo:<xsl:value-of select="translate(@cel,'.','_')"/> .
    </xsl:for-each>
</xsl:template>


<xsl:template name="sub">
    <xsl:for-each select="ref[@tip='sub']">
revo:<xsl:call-template name="ancestor-mrk"/> voko:sub revo:<xsl:value-of select="translate(@cel,'.','_')"/> .
    </xsl:for-each>
</xsl:template>

<xsl:template name="sin">
    <xsl:for-each select="ref[@tip='sin']">
revo:<xsl:call-template name="ancestor-mrk"/> voko:sin revo:<xsl:value-of select="translate(@cel,'.','_')"/> .
    </xsl:for-each>
</xsl:template>

<xsl:template name="dif">
    <xsl:for-each select="ref[@tip='dif']">
revo:<xsl:call-template name="ancestor-mrk"/> voko:dif revo:<xsl:value-of select="translate(@cel,'.','_')"/> .
    </xsl:for-each>
</xsl:template>

<xsl:template name="ant">
    <xsl:for-each select="ref[@tip='ant']">
revo:<xsl:call-template name="ancestor-mrk"/> voko:ant revo:<xsl:value-of select="translate(@cel,'.','_')"/> .
    </xsl:for-each>
</xsl:template>

<xsl:template name="vid">
    <xsl:for-each select="ref[@tip='vid' or not(@tip) or @tip='']">
revo:<xsl:call-template name="ancestor-mrk"/> voko:vid revo:<xsl:value-of select="translate(@cel,'.','_')"/> .
    </xsl:for-each>
</xsl:template>

<xsl:template name="malprt">
    <xsl:for-each select="ref[@tip='malprt']">
revo:<xsl:call-template name="ancestor-mrk"/> voko:malprt revo:<xsl:value-of select="translate(@cel,'.','_')"/> .
    </xsl:for-each>
</xsl:template>

<xsl:template name="prt">
    <xsl:for-each select="ref[@tip='prt']">
revo:<xsl:call-template name="ancestor-mrk"/> voko:prt revo:<xsl:value-of select="translate(@cel,'.','_')"/> .
    </xsl:for-each>
</xsl:template>

<xsl:template name="ekz">
    <xsl:for-each select="ref[@tip='ekz']">
revo:<xsl:call-template name="ancestor-mrk"/> voko:ekz revo:<xsl:value-of select="translate(@cel,'.','_')"/> .
    </xsl:for-each>
</xsl:template>

<xsl:template name="lst">
<!-- uzu skos:Collection tie chi -->
    <xsl:for-each select="ref[@tip='lst']">
revo:<xsl:call-template name="ancestor-mrk"/> voko:lst revo:<xsl:value-of select="translate(@cel,'.','_')"/> .
    </xsl:for-each>
</xsl:template>

<!-- subpremu -->
<!-- <xsl:template match="trd"/> -->

<xsl:template name ="ancestor-mrk">
  <xsl:value-of select="translate(ancestor-or-self::node()[@mrk][1]/@mrk,'.','_')"/>
</xsl:template>


</xsl:stylesheet>










