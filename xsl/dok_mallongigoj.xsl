<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                version="1.0">


<!-- (c) 2002-2013 che Wolfram Diestel

  transformi la mallongigoliston al HTML

-->

<xsl:include href="inc/inx_menuo.inc"/>

<xsl:output method="html" version="4.0" encoding="utf-8"/>

<xsl:template match="mallongigoj">
  <html>
    <head>
      <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
      <meta name="viewport" content="width=device-width,initial-scale=1"/>
      <title><xsl:value-of select="concat(../@nometo,'-indekso: ',@titolo)"/></title>
      <link title="indekso-stilo" type="text/css" 
            rel="stylesheet" href="../stl/indeksoj.css"/>
    </head>
    <body>
      <table cellspacing="0">
        <xsl:call-template name="menuo-ktp"/>
        <tr>
          <td colspan="{$inx_paghoj}" class="enhavo">

    <h1>mallongigoj</h1>

    <dl compact="compact">
    <xsl:for-each select="mallongigo">
      <a name="{@mll}"/>
      <dt><xsl:value-of select="@mll"/></dt>
      <dd><xsl:value-of select="."/></dd>
    </xsl:for-each>
    </dl>

          </td>
        </tr>
      </table>
    </body>
  </html>

</xsl:template>

</xsl:stylesheet>
    





