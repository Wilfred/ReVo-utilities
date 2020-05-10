<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                version="1.0">


<!-- (c) 2006 che Wolfram Diestel
     licenco GPL 2.0
-->

<xsl:param name="verbose" select="false"/>

<xsl:output method="xml" encoding="utf-8" indent="yes"/>
<xsl:strip-space elements="kap uzo trd"/>

<xsl:variable name="fakcfg">../cfg/fakoj.xml</xsl:variable>
<xsl:variable name="lngcfg">../cfg/lingvoj.xml</xsl:variable>

<xsl:key name="fakoj" match="//uzo" use="."/>
<xsl:key name="lingvoj" match="//trd[@lng]" use="@lng"/>



<xsl:template match="/">
  <indekso>

    <!-- kapvortoj -->

    <kap-oj lng="eo">
      <tez> <!-- tezauro-radikoj -->
        <xsl:apply-templates select="//tezrad[not(@fak)]" mode="tez"/>
      </tez>

      <xsl:apply-templates select="//art/kap|//drv/kap" mode="kapvortoj"/>
    </kap-oj>

    <xsl:variable name="root" select="."/>

    <!-- fakoj -->

    <xsl:for-each select="document($fakcfg)/fakoj/fako">
      <xsl:variable name="fak" select="@kodo"/>
   
      <xsl:if test="$verbose='true'">
        <xsl:message>progreso: traktas fakon <xsl:value-of select="$fak"/>...</xsl:message>
      </xsl:if>

      <xsl:for-each select="$root">
        <xsl:if test="key('fakoj',$fak)">
          <fako fak="{$fak}" n="{count(key('fakoj',$fak))}">

            <tez> <!-- tezauro-radikoj -->
              <xsl:apply-templates select="//tezrad[@fak=$fak]" mode="tez"/>
            </tez>

            <xsl:apply-templates select="key('fakoj',$fak)"/>
          </fako>
        </xsl:if>
      </xsl:for-each>
    </xsl:for-each>

    <!-- tradukoj -->

    <xsl:variable name="trd-snc" select="count(//drv[
                       (not (child::snc 
                          or child::stl[text()='EVI' or text()='ARK']))])
                + count(//snc[
                       (not (child::stl[text()='EVI' or text()='ARK'])) 
                   and (not (../stl[text()='EVI' or text()='ARK']))])
             "/>  <!-- = sumo de tradukendaj sencoj kaj derivajhoj -->

    <trd-snc p="{$trd-snc}"/>

    <xsl:for-each select="document($lngcfg)/lingvoj/lingvo">
      <xsl:variable name="lng" select="@kodo"/>
      <xsl:variable name="ptrd">
         <xsl:for-each select="$root">
            <xsl:value-of select="count(//drv[
                       (not (child::snc 
                          or child::stl[text()='EVI' or text()='ARK'])) 
                   and child::trd[@lng=$lng]])
                + count(//snc[
                       (not (child::stl[text()='EVI' or text()='ARK'])) 
                   and (not (../stl[text()='EVI' or text()='ARK']))
                   and (child::trd[@lng=$lng] or ../trd[@lng=$lng])])
             "/>  <!-- = nombro de tradukitaj sencoj kaj derivajhoj --> 
        </xsl:for-each>
      </xsl:variable>

      <xsl:if test="$verbose='true'">
        <xsl:message>progreso: traktas tradukojn <xsl:value-of select="."/>jn...</xsl:message>
      </xsl:if>

      <xsl:for-each select="$root">
        <xsl:variable name="n" select="count(key('lingvoj',$lng))"/>
        <xsl:if test="$n &gt; 0">
          <!-- tradukoj de tiu lingvo --> 
          <trd-oj lng="{$lng}" n="{$n}" p="{$ptrd}">
            <xsl:apply-templates select="key('lingvoj',$lng)"/>
          </trd-oj>
          <!-- kelkaj netradukitaj sencoj de tiu lingvo -->
          <xsl:if test="($trd-snc - $ptrd) div $trd-snc &lt; 0.7">
             <mankoj lng="{$lng}">
                <xsl:for-each select="(//drv[
                       (not (child::snc 
                          or child::stl[text()='EVI' or text()='ARK'])) 
                   and not (child::trd[@lng=$lng])]
                | //snc[
                       (not (child::stl[text()='EVI' or text()='ARK'])) 
                   and (not (../stl[text()='EVI' or text()='ARK']))
                   and not (child::trd[@lng=$lng] or ../trd[@lng=$lng])])[position() &lt;= 777]">
                   <v mrk="{ancestor-or-self::node()[@mrk][1]/@mrk}">
                     <xsl:if test="self::snc and count(../snc)>1">
                       <xsl:attribute name="n">
                         <xsl:number/>
                       </xsl:attribute>
                     </xsl:if>
                     <xsl:apply-templates
                       select="ancestor-or-self::node()[self::art or self::drv][kap][1]/kap"/>
                   </v>
                </xsl:for-each>
             </mankoj>
          </xsl:if>
        </xsl:if>
      </xsl:for-each>
    </xsl:for-each>

    <!-- bildoj -->

    <xsl:if test="//bld">
      <bld-oj>
        <xsl:apply-templates select="//bld" mode="bildoj"/>
      </bld-oj>
    </xsl:if>

    <!-- mallongigoj -->

    <xsl:if test="//mlg">
      <mlg-oj>
        <xsl:apply-templates select="//mlg"/>
      </mlg-oj>
    </xsl:if>

    <!-- statistiko -->
    <stat>
      <ero s="kap" t="artikoloj" n="{count(//art)}"/>
      <ero s="kap" t="deriva&#x0135;oj" n="{count(//drv)}"/>
      <ero s="kap" t="sencoj" n="{count(//snc)+count(//drv[not(child::snc)])}"/>
      <ero s="kap" t="bildoj" n="{count(//bld)}"/>
      <ero s="kap" t="mallongigoj" n="{count(//mlg)}"/> 

      <ero s="rad" t="fundamentaj (1905)" n="{count(//art/kap//ofc[.='*'])}/2768"/>
      <ero s="rad" t="oficialaj (1a, 1909)" n="{count(//art/kap//ofc[.='1'])}/860"/>
      <ero s="rad" t="oficialaj (2a, 1919)" n="{count(//art/kap//ofc[.='2'])}/591"/>
      <ero s="rad" t="oficialaj (3a, 1921)" n="{count(//art/kap//ofc[.='3'])}/204"/>
      <ero s="rad" t="oficialaj (4a, 1929)" n="{count(//art/kap//ofc[.='4'])}/118"/>
      <ero s="rad" t="oficialaj (5a, 1934)" n="{count(//art/kap//ofc[.='5'])}/8"/>
      <ero s="rad" t="oficialaj (6a, 1935)" n="{count(//art/kap//ofc[.='6'])}/21"/>
      <ero s="rad" t="oficialaj (7a, 1958)" n="{count(//art/kap//ofc[.='7'])}/159"/>
      <ero s="rad" t="oficialaj (8a, 1974)" n="{count(//art/kap//ofc[.='8'])}/213"/>
      <ero s="rad" t="oficialaj (9a, 2007)" n="{count(//art/kap//ofc[.='9'])}/209"/>

<!-- lau Michel...    
    
U.V = 2629 U.V radikoj + 141 fundamentaj (60+80+1) = 2770 (<>2768 r. !)    + 303 U.V. kunmetajxoj  +  ? fundamentaj kunmetajxoj
1OA =  805 radikoj  => + 55 fundamentaj  = 860  (+ 2  1OA-kunmetajxoj ) 
2OA = 587 radikoj  => + 4 fundamentaj  = 591
3OA = 203 radikoj => +1 fundamentaj  = 204
4OA = 118 radikoj
5OA = 8 radikoj 
6OA = 21 radikoj 
7OA = 31 radikoj => + 80 fund-7OA + ( 44 fund-1OA + 4 fund-2OA)  =  159
8OA = 200 radikoj => + 1 fund-8OA + ( 11 fund-1OA + 1 fund-3OA)  =  213
9OA = 209 radikoj + 66 derivataj kunmetajxoj = 275

-->
        
        
      <!-- statistiko de la tradukoj -->
<!--      <trd-snc p="{$trd-snc}"/> --> <!-- = sumo de tradukendaj sencoj kaj derivajhoj -->
<!--  count(//drv[
                       (not (child::snc 
                          or child::uzo[text()='EVI' or text()='ARK']))])
                + count(//snc[
                       (not (child::uzo[text()='EVI' or text()='ARK'])) 
                   and (not (../uzo[text()='EVI' or text()='ARK']))])
             }"/ -->  <!-- = sumo de tradukendaj sencoj kaj derivajhoj -->

<!--      <xsl:for-each select="document($lngcfg)/lingvoj/lingvo">
        <xsl:variable name="lng" select="@kodo"/>
   
        <xsl:for-each select="$root">
          <xsl:if test="key('lingvoj',$lng)">

            <trd lng="{$lng}" n="{count(key('lingvoj',$lng))}"
               p="{count(//drv[
                       (not (child::snc 
                          or child::uzo[text()='EVI' or text()='ARK'])) 
                   and child::trd[@lng=$lng]])
                + count(//snc[
                       (not (child::uzo[text()='EVI' or text()='ARK'])) 
                   and (not (../uzo[text()='EVI' or text()='ARK']))
                   and (child::trd[@lng=$lng] or ../trd[@lng=$lng])])
             }" "/ -->  <!-- = nombro de tradukitaj sencoj kaj derivajhoj -->
<!--          </xsl:if>
        </xsl:for-each>
      </xsl:for-each -->


      <!-- statistiko de la fakoj -->
      <!-- xsl:for-each select="document($fakcfg)/fakoj/fako">
        <xsl:variable name="fak" select="@kodo"/>
   
        <xsl:for-each select="$root">
          <xsl:if test="key('fakoj',$fak)">
            <fak fak="{$fak}" n="{count(key('fakoj',$fak))}"/>
          </xsl:if>
        </xsl:for-each>
      </xsl:for-each -->

    </stat>

  </indekso>
</xsl:template>

<xsl:template match="kap[rad]" mode="kapvortoj">
  <v>
    <xsl:attribute name="mrk">
      <xsl:value-of select="ancestor::node()[@mrk][1]/@mrk"/>
    </xsl:attribute>
    <r> <!-- inversigita radiko por la inversa indekso -->
      <xsl:call-template name="reverse">
        <xsl:with-param name="string" select="rad"/>
      </xsl:call-template>
    </r>
    <k>
      <xsl:call-template name="kap-kap"/> 
          <!-- apply-templates select="text()|rad"/ -->
    </k>
    <k1> <!-- kun "/" post radiko por la inversa indekso -->
      <xsl:call-template name="kap-inv"/> 
          <!-- apply-templates select="text()|rad" mode="inv"/ -->
    </k1>
  </v>
  <xsl:apply-templates select="var" mode="kapvortoj"/>
</xsl:template>

<xsl:template name="reverse"> 
   <xsl:param name="string"/> 
   <xsl:choose> 
     <xsl:when test="string-length($string) = 0 or string-length($string) = 1"> 
       <xsl:value-of select="$string"/> 
     </xsl:when> 
     <xsl:otherwise> 
       <xsl:value-of select="substring($string,string-length($string), 1)"/> 
       <xsl:call-template name="reverse"> 
         <xsl:with-param name="string" select="substring($string, 1, 
           string-length($string) - 1)"/> 
       </xsl:call-template> 
    </xsl:otherwise> 
  </xsl:choose> 
</xsl:template> 
 

<xsl:template match="drv/kap|drv/kap/var/kap" mode="kapvortoj">
  <!-- ellasu la derivajhon kun sama kapvorto kiel la artikolo -->
      <xsl:variable name="art-kap"><xsl:for-each
        select="ancestor::node()[self::art]/kap"
        ><xsl:call-template name="kap-komparo"
        /></xsl:for-each></xsl:variable>
      <xsl:variable name="drv-kap"><xsl:call-template name="kap-komparo"
        /></xsl:variable>
      <xsl:if test="$art-kap != $drv-kap">
        <v>
          <xsl:attribute name="mrk">
            <xsl:value-of select="ancestor::node()[@mrk][1]/@mrk"/>
          </xsl:attribute>
          <k>
            <xsl:call-template name="kap-kap"/> <!-- apply-templates select="text()|tld"/ -->
          </k>
        </v>
      </xsl:if>
  <xsl:apply-templates select="var" mode="kapvortoj"/>
</xsl:template>

<xsl:template name="kap-komparo">
   <xsl:variable name="kap"><xsl:apply-templates select="text()|rad|tld"/></xsl:variable>
   <xsl:value-of select="translate(normalize-space($kap),'/,','')"/>
</xsl:template>

<xsl:template name="kap-kap">
   <xsl:variable name="kap"><xsl:apply-templates select="text()|rad|tld"/></xsl:variable>
   <xsl:value-of select="translate(normalize-space($kap),'/,','')"/>
</xsl:template>

<xsl:template name="kap-inv">
   <xsl:variable name="kap"><xsl:apply-templates select="text()|rad"/></xsl:variable>
   <xsl:value-of select="normalize-space($kap)"/>
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

<!-- xsl:template match="kap/text()">
  <xsl:value-of select="translate(normalize-space(.),'/,','')"/>
</xsl:template -->

<!-- xsl:template match="kap/text()" mode="inv">
  <xsl:value-of select="normalize-space(.)"/>
</xsl:template -->

<xsl:template match="rad" mode="inv">
  <xsl:apply-templates/>
</xsl:template>

<!-- xsl:template match="ofc|fnt"/ -->

<xsl:template match="kap">
    <xsl:call-template name="kap-kap"/> 
       <!-- apply-templates select="text()|rad|tld"/ -->
</xsl:template>

<xsl:template match="uzo">
  <v>
    <xsl:attribute name="mrk">
      <xsl:value-of select="ancestor::node()[@mrk][1]/@mrk"/>
    </xsl:attribute>

     <xsl:apply-templates
  select="(ancestor::art|ancestor::drv)[last()]/kap"/>

  </v>
</xsl:template>

<xsl:template match="stl"/> <!-- ignoru stil-indikojn, ne necesos en postaj ŝtupoj -->

<xsl:template match="bld" mode="bildoj">
  <v>
    <xsl:attribute name="mrk">
      <xsl:value-of select="ancestor::node()[@mrk][1]/@mrk"/>
    </xsl:attribute>
    <t>
      <xsl:apply-templates select="text()|ind|klr|tld"/>
    </t>
    <k>
     <xsl:apply-templates
  select="(ancestor::art/kap|ancestor::drv/kap)[last()]"/>
    </k>
  </v>
</xsl:template>


<xsl:template match="trd|mlg|bld">
  <v>
    <xsl:attribute name="mrk">
      <xsl:value-of select="ancestor::node()[@mrk][1]/@mrk"/>
    </xsl:attribute>
    <t>
      <xsl:value-of select="normalize-space(text()|mll)"/>
    </t>
    <xsl:if test="klr">
      <t1>
        <xsl:apply-templates/>
      </t1>
    </xsl:if>
    <k>
     <xsl:apply-templates
  select="(ancestor::art/kap|ancestor::drv/kap|ancestor::ekz/ind|ancestor::bld/ind)[last()]"/>
    </k>
  </v>
</xsl:template>

<xsl:template match="trd[.//ind]">
  <v>
    <xsl:attribute name="mrk">
      <xsl:value-of select="ancestor::node()[@mrk][1]/@mrk"/>
    </xsl:attribute>
    <t>
      <xsl:value-of select="normalize-space(.//ind)"/>
    </t>
    <t1>
      <xsl:apply-templates/>
    </t1>
    <k>
     <xsl:apply-templates
  select="(ancestor::art/kap|ancestor::drv/kap|ancestor::ekz/ind|ancestor::bld/ind)[last()]"/>
    </k>
  </v>
</xsl:template>

<xsl:template match="trd/ind|mll/ind">
  <u>
    <xsl:apply-templates/>
  </u>
</xsl:template>

<xsl:template match="mll">
  <xsl:if test="@tip='kom' or @tip='mez'">...</xsl:if>
  <xsl:apply-templates/>
  <xsl:if test="@tip='fin' or @tip='mez'">...</xsl:if>
</xsl:template>

<xsl:template match="trd/klr">
  <xsl:apply-templates/>
</xsl:template> 

<xsl:template match="tezrad" mode="tez">
  <v>
    <xsl:attribute name="mrk">
      <xsl:choose>
         <xsl:when test="ancestor::drv[count(snc)=1]">
           <xsl:value-of select="ancestor::drv/@mrk"/>
         </xsl:when>
         <xsl:when test="../@mrk">
            <xsl:value-of select="../@mrk"/>
         </xsl:when>
         <xsl:otherwise>
            <xsl:value-of select="ancestor::node()[@mrk][1]/@mrk"/><xsl:text>.</xsl:text>
            <xsl:number from="drv|subart" level="multiple" count="snc|subsnc" format="1.a"/>
         </xsl:otherwise>
      </xsl:choose>
    </xsl:attribute>
    <xsl:apply-templates
       select="ancestor-or-self::node()[self::art or self::drv][kap][1]/kap"/>
  </v>
</xsl:template>


</xsl:stylesheet>













