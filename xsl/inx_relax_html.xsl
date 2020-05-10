<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                version="1.0">

<!-- (c) 2016 che Wolfram Diestel
     licenco GPL 2.0
-->

<xsl:include href="inc/inx_menuo.inc"/>

<xsl:output method="html" encoding="utf-8" indent="no"/>

<xsl:param name="verbose" select="'false'"/>

<xsl:variable name="root" select="/"/>


<xsl:template match="/">

  <html>
    <head><title>Strukturaj neregulaĵoj trovitaj per RelaxNG (jing)</title></head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <meta name="viewport" content="width=device-width,initial-scale=1"/>
    <link title="indekso-stilo" type="text/css" rel="stylesheet" href="../stl/indeksoj.css"/>
  
    <body>
      <table cellspacing="0">
        <xsl:call-template name="menuo-ktp"/>
        <tr>
          <td colspan="{$inx_paghoj}" class="enhavo">
            <h1>Strukturaj neregulaĵoj trovitaj per RelaxNG (jing)</h1>

        <p>
          La struktura kontrolo per <a target="_new" href="../dtd/vokoxml.rnc">vokoxml.rnc</a>
          (RelaxNG) estas pli strikta ol la kontrolo per la 
          <a target="_new" href="../dtd/vokoxml.dtd">dokumenttipdifino</a> (DTD).
          La malsupraj trovaĵoj do striktasence ne estas eraroj. Sed la neregulaĵoj povas
          montri erarojn, ekz. mislokitajn tradukojn inter sencoj atribuitaj al la derivaĵo 
          anstataŭ al la senco. Aŭ ili povas konfuzi postajn redaktantojn, kiuj ne atendas 
          la informojn en nekutima loko.
        </p>
        <p>
          La kontrolo ankaŭ trovas markojn neregule formitajn, gramatikajn informojn malĝuste etikeditajn
          kiel vortospeco k.a.
        </p>
        <p>
          La RelaxNG-strukturo estas ankoraŭ iom eksperimenta kaj do diskutinda. Do eble ne 
          ĉiu malsupra trovita neregulaĵo meritas korekton. 
        </p>

            <xsl:choose>
              <xsl:when test="//eraro">
              <dl>
                  <xsl:apply-templates select="//eraro">
                    <xsl:sort select="@dos"/>
                  </xsl:apply-templates>
              </dl>
              </xsl:when>
                <xsl:otherwise>
                  <p>(<em>Ne troviĝis strukturaj eraroj kontrolitaj tie ĉi.</em>)</p>
                </xsl:otherwise>
            </xsl:choose>
            <xsl:apply-templates select="//date"/>
          </td>
        </tr>
      </table>
    </body>
  </html>
</xsl:template>

<xsl:template match="eraro">
  <dt>
    <a href="{concat('../art/',@dos,'.html')}" target="precipa">
      <b>
         <xsl:value-of select="@dos"/>:<xsl:value-of select="@lin"/>:<xsl:value-of select="@kol"/>
      </b>
    </a>
  </dt>
  <dd>
    <xsl:value-of select="."/>
  </dd>
</xsl:template>

<xsl:template match="date">
  <p>Generita je <xsl:value-of select="."/></p>
</xsl:template>

</xsl:stylesheet>










