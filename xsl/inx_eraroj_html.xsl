<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                version="1.0">

<!-- (c) 2006 che Wolfram Diestel
     licenco GPL 2.0
-->

<xsl:include href="inc/inx_menuo.inc"/>

<xsl:output method="html" encoding="utf-8" indent="no"/>

<xsl:param name="verbose" select="'false'"/>

<xsl:variable name="root" select="/"/>


<xsl:template match="/">

  <html>
    <head>
      <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
      <meta name="viewport" content="width=device-width,initial-scale=1"/>     
      <title><xsl:text>eraroraporto</xsl:text></title>
      <link title="indekso-stilo" type="text/css" 
            rel="stylesheet" href="../stl/indeksoj.css"/>
    </head>
    <body>
      <table cellspacing="0">
        <xsl:call-template name="menuo-ktp"/>
        <tr>
          <td colspan="{$inx_paghoj}" class="enhavo">
            <h1><xsl:text>eraroraporto</xsl:text></h1>
	    <p>
              Jen troviĝas listo de eraroj, kiujn la kontrolo per la dokumenttipdifino (DTD) ne trovas, 
              sed kiuj tamen estas korektendaj: Precipe neregule formitaj markoj, kaj sencelaj referencoj. 
              Tio povas esti mistajpoj, sed ankaŭ ekzemple aldonita referenco al vorto, kiu ankoraŭ mankas
              en la vortaro kaj do estas aldonenda.
	    </p>
            <p>
              Konsideru ankaŭ pliajn trovaĵojn en la listo <a href="relax_eraroj.html">neregulaĵoj 
              trovitaj per RelaxNG</a> kaj la rezultojn de la 
              <a target="_new" href="http://h1838790.stratoserver.net/revokontrolo/">vortokontrolo</a>
              kun <a target="_new" href="http://h1838790.stratoserver.net/revokontrolo/klarigoj.html">klarigoj</a>
              pri enhava analizo de la vortaro.
            </p>
            <xsl:variable name="n-sen-ekz"><xsl:value-of select="count(//art/ero[@tip='dos-sen-ekz'])"/></xsl:variable>
            <xsl:if test="$n-sen-ekz &gt; 300">
                <p>
                    Estas entute <xsl:value-of select="$n-sen-ekz"/> artikoloj sen ekzemplo.
                    Pro koncizeco nur la lastaj 300 estas listigitaj.
                </p>
            </xsl:if>
            <xsl:choose>
              <xsl:when test="//art[ero]">
                <dl>
                  <xsl:apply-templates select="//art[ero]">
                    <xsl:sort select="@dat" order="descending"/>
                  </xsl:apply-templates>
                </dl>
              </xsl:when>
              <xsl:otherwise>
                 <p>(<em>Ne troviĝis strukturaj eraroj kontrolitaj tie ĉi.</em>)</p>
              </xsl:otherwise>
            </xsl:choose>
          </td>
        </tr>
      </table>
    </body>
  </html>
</xsl:template>

<xsl:template match="art">
    <xsl:if test="ero[not(@tip='dos-sen-ekz')] or position() &lt; 201">
      <dt>
        <a href="{concat('../art/',@dos,'.html')}" target="precipa"><b><xsl:value-of select="@dos"/></b></a>
      </dt>
      <dd>      
        <xsl:apply-templates select="ero"/>
      </dd>
    </xsl:if>
</xsl:template>

<xsl:template match="ero">
  <p>
    <span class="dato">
      <xsl:value-of select="concat('en &lt;',@kie,' mrk=&quot;',@mrk,'&quot;&gt;:')"/>
    </span>
    <br/>
    <xsl:choose>

      <xsl:when test="@tip='art-sen-mrk'">
        Mankas atributo "mrk" en artikolo.
      </xsl:when>
      <xsl:when test="@tip='art-mrk-sgn'">
        Dosieronomo enhavu nur signojn el literoj, ciferoj kaj substreko.
      </xsl:when>

      <xsl:when test="@tip='mrk-ne-dos'">
        Unua parto de la atributo "mrk" ne egalas al la dosiernomo.
      </xsl:when>
      <xsl:when test="@tip='mrk-prt'">
        Atributo "mrk" ne havas partojn.
      </xsl:when>
      <xsl:when test="@tip='mrk-nul'">
        Dua parto de la atributo "mrk" ne enhavas la signon "0".
      </xsl:when>
        
      <xsl:when test="@tip='dos-sen-ekz'">
        Mankas ekzemplo en la artikolo. Ĉiu vorto bezonas almenaŭ unu ne-vortaran fonton (citaĵon) por montri ĝian uzon.
      </xsl:when>

      <xsl:when test="@tip='uzo-fak'">
        Fako "<xsl:value-of select="@arg"/>" ne estas difinita.
      </xsl:when>
      <xsl:when test="@tip='uzo-stl'">
        Stilo "<xsl:value-of select="@arg"/>" ne estas difinita.
      </xsl:when>
      <xsl:when test="@tip='trd-lng'">
        Lingvo "<xsl:value-of select="@arg"/>" ne estas difinita.
      </xsl:when>

      <xsl:when test="@tip='ref-sen-cel'">
        Referenco sen atributo "cel".
      </xsl:when>
      <xsl:when test="@tip='ref-cel-nul'">
        Dua parto de la atributo "cel" de referenco ne enhavas la signon "0":
        "<xsl:value-of select="@arg"/>"
      </xsl:when>
      <xsl:when test="@tip='ref-cel-dos'">
        Referenco celas al dosiero "<xsl:call-template name="dosiero"/>",
        kiu ne ekzistas.
      </xsl:when>
      <xsl:when test="@tip='ref-cel-mrk'">
        Referenco celas al "<xsl:value-of select="@arg"/>", kiu ne ekzistas en
        dosiero "<xsl:call-template name="dosiero"/>".
      </xsl:when>
      <xsl:when test="@tip='ref-tip-lst'">
        Referenco havas tipon 'lst', sed mankas atributo 'lst="..."').
      </xsl:when>
      <xsl:when test="@tip='ref-lst'">
        Referenco donas liston "<xsl:value-of select="@arg"/>", kiu ne
	ekzistas.
      </xsl:when>
      <xsl:when test="@tip='drv-sen-var'">
        Variaĵo en art/kap/var ne indeksiĝas, necesas aldoni ĝin kiel drv/kap/var.
      </xsl:when>
      <xsl:otherwise>
        Nekonata eraro de la tipo "<xsl:value-of select="@tip"/>".
      </xsl:otherwise>
    </xsl:choose>
  </p>
</xsl:template>

<xsl:template name="dosiero">
    <xsl:choose>
      <xsl:when test="contains(@arg,'.')">
        <xsl:value-of select="concat(substring-before(@arg,'.'),'.xml')"/>
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="concat(@arg,'.xml')"/>
      </xsl:otherwise>
    </xsl:choose>
</xsl:template>


</xsl:stylesheet>










