<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                version="1.0">


<!-- (c) 2002-2013 che Wolfram Diestel

  transformi la lingvolisto al HTML

-->

<xsl:include href="inc/inx_menuo.inc"/>

<xsl:output method="html" version="4.0" encoding="utf-8"/>



<xsl:template match="lingvoj">
  <html>
    <head>
      <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
      <meta name="viewport" content="width=device-width,initial-scale=1"/> 
      <title>mallongigoj de lingvoj</title>
      <link title="indekso-stilo" type="text/css" 
            rel="stylesheet" href="../stl/indeksoj.css"/>
    </head>
    <body>
      <table cellspacing="0">
	<xsl:call-template name="menuo-ktp"/>
	<tr>
          <td colspan="{$inx_paghoj}" class="enhavo">
	    <h1>mallongigoj de lingvoj</h1>
	    <p style="font-size: small">
    Por aldoni tradukojn en nova lingvo, bonvolu sendi al la
    administranto de la vortaro informojn pri alfabeto kaj ordigado.
	    </p>

	    <table align="center">
	      <tr><th>kodo</th><th>lingvo</th></tr>
	      <xsl:for-each select="lingvo">
		<tr>
		  <td><code><xsl:value-of select="@kodo"/></code></td>
		  <td>
		    <xsl:value-of select="."/>
		  </td>
		</tr>
	      </xsl:for-each>
	    </table>
	  </td>
	</tr>
      </table>
  </body>
  </html>
</xsl:template>


</xsl:stylesheet>
    





