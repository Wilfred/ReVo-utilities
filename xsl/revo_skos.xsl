<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                version="1.0">


<!-- (c) 2013 che Wolfram Diestel
     licenco GPL 2.0

     enigo : indekso.xml, kreita per "ant -f $VOKO/ant/indeksoj.xml inx-eltiro"
     eligo : tezauro en formato SKOS, vd. http://www.w3.org/TR/skos-reference/

     SKOS tamen estas tro "baza" por bildigi chiujn rilatojn de Revo tauge,
     aparte ne eblas distingi inter super/sub kaj malprt/prt. Tial pli bone
     uzu skemon voko.owl etendanta la skemon SKOS. Transformreguloj estas en revo_onto.xsl

-->


<xsl:output method="text" encoding="utf-8" indent="no"/>
<xsl:strip-space elements="kap art drv subdrv snc subsnc trd"/>

<xsl:key name="retro" match="ref" use="@cel"/>

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
   dct:title "Tezauro de Reta Vortaro"@eo. 

revo:revoScheme owl:imports &lt;http://www.w3.org/2004/02/skos/core&gt; .
</xsl:text>
  <xsl:apply-templates/>
</xsl:template>

<xsl:template match="art">
  <xsl:apply-templates select="subart|drv|snc"/>
</xsl:template>

<xsl:template match="subart|drv|subdrv">
  <xsl:apply-templates select="drv|subdrv|snc|subsnc"/>
</xsl:template>

<xsl:template match="drv[count(snc)=1]">
  <!-- kreu ununuran nodon por derivajhoj kun nur unu senco -->
  <xsl:variable name="mrk"><xsl:value-of select="@mrk"/></xsl:variable>
  <xsl:if test=".//tezrad or .//ref or key('retro',@mrk) or key('retro',snc/@mrk)">
  revo:<xsl:value-of select="@mrk"/> rdf:type skos:Concept ;
<!--      <xsl:if test="snc/@mrk">
        <xsl:attribute name="mrk2">
          <xsl:value-of select="snc/@mrk"/>
        </xsl:attribute>
      </xsl:if>
-->

   skos:prefLabel "<xsl:apply-templates
 select="ancestor-or-self::node()[self::art or self::drv][kap][1]/kap"/>"@eo .

      <xsl:if test=".//tezrad">
         <xsl:comment>###TEZRAD###</xsl:comment>
      </xsl:if>
      <xsl:if test=".//uzo">
         <xsl:comment>### UZO: <xsl:value-of select=".//uzo"/> ###</xsl:comment>
      </xsl:if>
 
      <xsl:for-each select="(trd|snc/trd)[@lng='de' or @lng='en' or @lng='ru'
			    or @lng='fr' or @lng='hu' or @lng='nl']">
        revo:<xsl:value-of select="$mrk"/> skos:altLabel "<xsl:value-of
	select="translate(normalize-space(.),$quot,$apos)"/>"@<xsl:value-of select="@lng"/> .
      </xsl:for-each>

      <xsl:call-template name="super2"/>
      <xsl:call-template name="sub2"/>
<!--      <xsl:call-template name="sin2"/>
      <xsl:call-template name="vid2"/>
      <xsl:call-template name="ant2"/>
      <xsl:call-template name="malprt2"/>
      <xsl:call-template name="prt2"/>
      <xsl:call-template name="ekz2"/>
      <xsl:call-template name="lst2"/>
-->
  </xsl:if>
</xsl:template>


<xsl:template match="drv[count(snc)!=1]|snc|subsnc">
  <!--  <xsl:if test="tezrad or ref or key('retro',@mrk)"> -->
    <xsl:variable name="mrk"><xsl:value-of select="@mrk"/></xsl:variable>

    <!-- kreu novan nodon -->
revo:<xsl:call-template name="tez-mrk-n"/> rdf:type skos:Concept ;

  skos:prefLabel "<xsl:apply-templates
  select="ancestor-or-self::node()[self::art or self::drv][kap][1]/kap"/>
  <xsl:if test="count(../snc)+count(../subsnc) &gt; 1"><xsl:text> </xsl:text>
            <xsl:number from="drv|subart" level="multiple" count="snc|subsnc" format="1.a"/>
        </xsl:if>"@eo .

      <xsl:if test=".//tezrad">
         <xsl:comment>###TEZRAD###</xsl:comment>
      </xsl:if>
      <xsl:if test=".//uzo">
         <xsl:comment>### UZO: <xsl:value-of select=".//uzo"/> ###</xsl:comment>
      </xsl:if>


      <xsl:for-each select="trd[@lng='de' or @lng='en' or @lng='ru'
			    or @lng='fr' or @lng='hu' or @lng='nl']">
        revo:<xsl:value-of select="$mrk"/> skos:altLabel "<xsl:value-of
	select="translate(normalize-space(.),$quot,$apos)"/>"@<xsl:value-of select="@lng"/> .
      </xsl:for-each>

      <xsl:call-template name="super"/>
      <xsl:call-template name="sub"/>
<!--      <xsl:call-template name="sin"/>
      <xsl:call-template name="vid"/>
      <xsl:call-template name="ant"/>
      <xsl:call-template name="malprt"/>
      <xsl:call-template name="prt"/>
      <xsl:call-template name="ekz"/>
      <xsl:call-template name="lst"/>-->
  <!--   </xsl:if> -->
  <xsl:apply-templates select="snc|subsnc"/>
</xsl:template>


<xsl:template name="tez-mrk-n">
   <xsl:choose>
      <xsl:when test="@mrk">
        <xsl:value-of select="@mrk"/>
      </xsl:when>

      <xsl:otherwise>
          <xsl:value-of select="ancestor::node()[@mrk][1]/@mrk"/>
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
       skos:broader revo:<xsl:value-of select="@cel"/> .
    </xsl:for-each>
 <!--   <xsl:for-each select="key('retro',@mrk)[@tip='sub']">
       <r c="{ancestor-or-self::node()[@mrk][1]/@mrk}"/>
    </xsl:for-each> -->

</xsl:template>


<xsl:template name="super2">
    <xsl:for-each select=".//ref[@tip='super']">
revo:<xsl:call-template name="ancestor-mrk"/>
       skos:broader revo:<xsl:value-of select="@cel"/> .
    </xsl:for-each>
<!--    <xsl:for-each select="key('retro',@mrk)[@tip='sub']|key('retro',snc/@mrk)[@tip='sub']">
       <r c="{ancestor-or-self::node()[@mrk][1]/@mrk}"/>
    </xsl:for-each> -->
</xsl:template>


<xsl:template name="sub">
    <xsl:for-each select="ref[@tip='sub']">
revo:<xsl:call-template name="ancestor-mrk"/>
       skos:narrower revo:<xsl:value-of select="@cel"/> .
    </xsl:for-each>
<!--    <xsl:for-each select="key('retro',@mrk)[@tip='super']">
       <r c="{ancestor-or-self::node()[@mrk][1]/@mrk}"/>
    </xsl:for-each> -->
</xsl:template>


<xsl:template name="sub2">
    <xsl:for-each select=".//ref[@tip='sub']">
revo:<xsl:call-template name="ancestor-mrk"/>
       skos:narrower revo:<xsl:value-of select="@cel"/> .
    </xsl:for-each>
<!--    <xsl:for-each select="key('retro',@mrk)[@tip='super']|key('retro',snc/@mrk)[@tip='super']">
      <r c="{ancestor-or-self::node()[@mrk][1]/@mrk}"/>
    </xsl:for-each>
 -->
</xsl:template>


<xsl:template name="sin">
    <xsl:for-each select="ref[@tip='sin']">
revo:<xsl:call-template name="ancestor-mrk"/>
  skos:related revo:<xsl:value-of select="@cel"/> .
    </xsl:for-each>
<!--    <xsl:for-each select="key('retro',@mrk)[@tip='sin' or @tip='dif']">
       <r c="{ancestor-or-self::node()[@mrk][1]/@mrk}"/>
    </xsl:for-each>
 -->
</xsl:template>


<xsl:template name="sin2">
    <xsl:for-each select=".//ref[@tip='sin']">
revo:<xsl:call-template name="ancestor-mrk"/>
       skos_related revo:<xsl:value-of select="@cel"/> .
    </xsl:for-each>
<!--    <xsl:for-each select="key('retro',@mrk)[@tip='sin' or @tip='dif']
          |key('retro',snc/@mrk)[@tip='sin' or @tip='dif']">
       <r c="{ancestor-or-self::node()[@mrk][1]/@mrk}"/>
    </xsl:for-each> -->
</xsl:template>


<xsl:template name="ant">
    <xsl:for-each select="ref[@tip='ant']">
revo:<xsl:call-template name="ancestor-mrk"/>
       skos:related <xsl:value-of select="@cel"/> .
    </xsl:for-each>
<!--    <xsl:for-each select="key('retro',@mrk)[@tip='ant']">
       <r c="{ancestor-or-self::node()[@mrk][1]/@mrk}"/>
    </xsl:for-each> -->
</xsl:template>


<xsl:template name="ant2">
    <xsl:for-each select=".//ref[@tip='ant']">
revo:<xsl:call-template name="ancestor-mrk"/>
       skos:related <xsl:value-of select="@cel"/> .
    </xsl:for-each>
<!--
    <xsl:for-each select="key('retro',@mrk)[@tip='ant']|key('retro',snc/@mrk)[@tip='ant']">
       <r c="{ancestor-or-self::node()[@mrk][1]/@mrk}"/>
    </xsl:for-each>
 -->
</xsl:template>


<xsl:template name="vid">
    <xsl:for-each select="ref[@tip='vid' or not(@tip) or @tip='']">
revo:<xsl:call-template name="ancestor-mrk"/>
       skos:related <xsl:value-of select="@cel"/> .
    </xsl:for-each>
<!--    <xsl:for-each select="key('retro',@mrk)[@tip='vid' or not(@tip) or @tip='']">
       <r c="{ancestor-or-self::node()[@mrk][1]/@mrk}"/>
    </xsl:for-each> -->
</xsl:template>


<xsl:template name="vid2">
    <xsl:for-each select=".//ref[@tip='vid' or not(@tip) or @tip='']">
revo:<xsl:call-template name="ancestor-mrk"/>
       skos:related <xsl:value-of select="@cel"/> .
    </xsl:for-each>
<!--
    <xsl:for-each select="key('retro',@mrk)[@tip='vid' or not(@tip) or @tip='']
        |key('retro',snc/@mrk)[@tip='vid' or not(@tip) or @tip='']">
       <r c="{ancestor-or-self::node()[@mrk][1]/@mrk}"/>
    </xsl:for-each> -->
</xsl:template>


<xsl:template name="malprt">
    <xsl:for-each select="ref[@tip='malprt']">
revo:<xsl:call-template name="ancestor-mrk"/>
  skos:related <xsl:value-of select="@cel"/> .
    </xsl:for-each>
<!--    <xsl:for-each select="key('retro',@mrk)[@tip='prt']">
       <r c="{ancestor-or-self::node()[@mrk][1]/@mrk}"/>
    </xsl:for-each> -->
</xsl:template>


<xsl:template name="malprt2">
    <xsl:for-each select=".//ref[@tip='malprt']">
revo:<xsl:call-template name="ancestor-mrk"/>
  skos:related <xsl:value-of select="@cel"/> .
    </xsl:for-each>
<!--
    <xsl:for-each select="key('retro',@mrk)[@tip='prt']|key('retro',snc/@mrk)[@tip='prt']">
       <r c="{ancestor-or-self::node()[@mrk][1]/@mrk}"/>
    </xsl:for-each>
-->
</xsl:template>


<xsl:template name="prt">
    <xsl:for-each select="ref[@tip='prt']">
revo:<xsl:call-template name="ancestor-mrk"/>
       skos:related <xsl:value-of select="@cel"/> .
    </xsl:for-each>
<!--    <xsl:for-each select="key('retro',@mrk)[@tip='malprt']">
       <r c="{ancestor-or-self::node()[@mrk][1]/@mrk}"/>
    </xsl:for-each> -->
</xsl:template>


<xsl:template name="prt2">
    <xsl:for-each select=".//ref[@tip='prt']">
revo:<xsl:call-template name="ancestor-mrk"/>
       skos:related <xsl:value-of select="@cel"/> .
    </xsl:for-each>
<!--
    <xsl:for-each select="key('retro',@mrk)[@tip='malprt']|key('retro',snc/@mrk)[@tip='malprt']">
       <r c="{ancestor-or-self::node()[@mrk][1]/@mrk}"/>
    </xsl:for-each>
-->
</xsl:template>


<xsl:template name="ekz">
    <xsl:for-each select="ref[@tip='ekz']">
revo:<xsl:call-template name="ancestor-mrk"/>
       skos:related <xsl:value-of select="@cel"/> .
    </xsl:for-each>
<!--    <xsl:for-each select="key('retro',@mrk)[@tip='lst']">
       <r c="{ancestor-or-self::node()[@mrk][1]/@mrk}"/>
    </xsl:for-each> -->
</xsl:template>


<xsl:template name="ekz2">
    <xsl:for-each select=".//ref[@tip='ekz']">
revo:<xsl:call-template name="ancestor-mrk"/>
       skos:related <xsl:value-of select="@cel"/> .
    </xsl:for-each>
<!--
    <xsl:for-each select="key('retro',@mrk)[@tip='lst']|key('retro',snc/@mrk)[@tip='lst']">
       <r c="{ancestor-or-self::node()[@mrk][1]/@mrk}"/>
    </xsl:for-each>
-->
</xsl:template>


<xsl:template name="lst">
<!-- uzu skos:Collection tie chi -->
    <xsl:for-each select="ref[@tip='lst']">
revo:<xsl:call-template name="ancestor-mrk"/>
       skos:narrower <xsl:value-of select="@cel"/> .
    </xsl:for-each>
<!--    <xsl:for-each select="key('retro',@mrk)[@tip='ekz']">
       <r c="{ancestor-or-self::node()[@mrk][1]/@mrk}"/>
    </xsl:for-each> -->
</xsl:template>


<xsl:template name="lst2">
<!-- uzu skos:Collection tie chi -->
    <xsl:for-each select=".//ref[@tip='lst']">
revo:<xsl:call-template name="ancestor-mrk"/>
       skos:narrower <xsl:value-of select="@cel"/> .
    </xsl:for-each>
<!--
    <xsl:for-each select="key('retro',@mrk)[@tip='ekz']|key('retro',snc/@mrk)[@tip='ekz']">
       <r c="{ancestor-or-self::node()[@mrk][1]/@mrk}"/>
    </xsl:for-each>
-->
</xsl:template>

<!-- subpremu -->
<!-- <xsl:template match="trd"/> -->

<xsl:template name ="ancestor-mrk">
  <xsl:value-of select="ancestor-or-self::node()[@mrk][1]/@mrk"/>
</xsl:template>


</xsl:stylesheet>










