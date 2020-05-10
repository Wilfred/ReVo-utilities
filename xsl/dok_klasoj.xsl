<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                version="1.0">


<!-- (c) 2002-2013 che Wolfram Diestel

  transformi la fakoliston al HTML

-->


<xsl:include href="inc/inx_menuo.inc"/>


<xsl:output method="html" version="4.0" encoding="utf-8"/>

<xsl:template match="klasoj">
  <html>
    <head>
      <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
      <meta name="viewport" content="width=device-width,initial-scale=1"/>
      <title>klasoj (vortlistoj)</title>
      <link title="indekso-stilo" type="text/css" 
            rel="stylesheet" href="../stl/indeksoj.css"/>
    </head>
    <body>


    <table cellspacing="0">
      <xsl:call-template name="menuo-ktp"/>
      <tr>
          <td colspan="{$inx_paghoj}" class="enhavo">
      
	    <h1>klasoj (vortlistoj)</h1>

	    <ul style="padding-left: 0; font-weight: 600">
	      <xsl:for-each select="kls">
		<xsl:call-template name="listoj1"/>
	      </xsl:for-each>
	    </ul>

	  </td>
      </tr>
    </table>
  </body>
  </html>
</xsl:template>

<xsl:template name="listoj1">
   <li style="margin-top: 0.4em">
      <xsl:value-of select="concat('voko:',substring-after(@nom,'#'))"/>
      <xsl:for-each select="kls">
        <ul style="font-weight: normal">
          <xsl:call-template name="listoj2"/>
        </ul>
      </xsl:for-each>
    </li>
</xsl:template>

<xsl:template name="listoj2">
   <li>
     <xsl:value-of select="concat('voko:',substring-after(@nom,'#'))"/>
      <xsl:for-each select="kls">
        <ul style="font-weight: normal">
          <xsl:call-template name="listoj2"/>
        </ul>
      </xsl:for-each>
    </li>
</xsl:template>

</xsl:stylesheet>
    





