<!DOCTYPE xsl:transform>

<xsl:transform
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:saxon="http://saxon.sf.net/"
  version="2.0"
  extension-element-prefixes="saxon" 
>

<!-- xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                version="1.0"
  xmlns:redirect="http://xml.apache.org/xalan/redirect"
    extension-element-prefixes="redirect" -->


<!-- (c) 2006-2018 che Wolfram Diestel
     licenco GPL 2.0

     Klasoj estas vortoj de sama kategorio, ekz. muzikiloj, ĥemiaj elementoj, stelfiguroj, festoj ktp.
     La klasanoj estas trovitaj en la artikoloj per la referenctipoj 'lst' (<ref tip='lst'...)
     De tie ili venas en inter-dosieron, kiu estas la bazo por la tezaŭro tez_ret.xml

     Laŭ la pado lst/r/@l=$klaso ili eltroviĝas tie vd. la ŝablonon (template) "klasoj" malsupre
-->

<xsl:include href="inc/inx_kodigo.inc"/>


<xsl:output method="@format@" encoding="utf-8"/>
<xsl:strip-space elements="k"/>

<!--
<xsl:include href="inx_ordigo2.inc"/> -->
<!-- <xsl:template name="v"/> --> <!-- referencita de inx_ordigo2.inc, sed ne bezonata tie ĉi -->

<xsl:param name="verbose" select="'false'"/>
<xsl:param name="warn-about-dead-refs" select="'false'"/>


<!-- xsl:variable name="fakoj">../cfg/fakoj.xml</xsl:variable -->
<xsl:variable name="enhavo">../cfg/enhavo.xml</xsl:variable>
  <xsl:variable name="inx_paghoj"
		select="count(document($enhavo)//pagho[not(@kashita='jes')])"/>
<xsl:variable name="enhavo-root" select="document($enhavo)"/>

<xsl:variable name="klasoj">../cfg/klasoj.xml</xsl:variable>
<xsl:variable name="klasoj-root" select="document($klasoj)"/>

<xsl:variable name="root" select="/"/>


<!-- <xsl:key name="klasoj" match="$klasojroot/klasoj//kls" use="@nom"/> -->

<xsl:template match="/">
  <xsl:text>XXXX</xsl:text> <!-- dosiero .tempo2 ne estu malplena -->

  <xsl:call-template name="klasoj"/>
</xsl:template>


<xsl:template name="klasoj">
  <xsl:for-each select="$klasoj-root//kls">
    <!-- klasoj povas aperi plurloke en la hierarkio, sed nur unufoje
    traktighu tie chi, integritajn klasojn ne metu en apartan dosieron -->
    <xsl:if test="not(@prezento='integrita' or preceding::kls[@nom=current()/@nom])">

      <xsl:variable name="kls" select="substring-after(@nom,'#')"/>
      <xsl:variable name="ordigita" select="@ordigita"/>
      <xsl:variable name="dosiero">
         <xsl:text>vx_</xsl:text>
         <xsl:call-template name="eo-kodigo">
            <xsl:with-param name="str"><xsl:value-of select="$kls"/></xsl:with-param>
         </xsl:call-template>
         <xsl:text>.html</xsl:text>
       </xsl:variable>

      <xsl:if test="$verbose='true'">
	<xsl:message>skribas al <xsl:value-of select="$dosiero"/></xsl:message>
      </xsl:if>

      <!-- redirect:write select="$dosiero" -->
      <xsl:result-document href="{$dosiero}" method="@format@" encoding="utf-8" indent="yes">
	<html>
	  <head>
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
	    <meta name="viewport" content="width=device-width,initial-scale=1"/>
            <title><xsl:value-of 
	    select="concat('vortlisto: ',translate($kls,'_',' '))"/></title>
            <link title="indekso-stilo" type="text/css" 
		  rel="stylesheet" href="../stl/indeksoj.css"/>
	  </head>
	  <body>
            <table cellspacing="0">
              <xsl:call-template name="menuo-eo"/>
              <tr>
		<td colspan="{$inx_paghoj}" class="enhavo">
		  
		  <h1>
		    <xsl:value-of select="translate($kls,'_',' ')"/>
		  </h1>

		  <!-- prezentu liston de ligoj al subklasoj -->
		  <ul style="padding-left: 0">
                    <xsl:for-each select="kls">
                      <xsl:variable name="refkls"
				    select="substring-after(@nom,'#')"/>
		   
                      <xsl:choose>
                        <xsl:when test="not(@prezento='integrita')">
			  <li>
			    <a>
			      <xsl:attribute name="href">
				<xsl:text>vx_</xsl:text>
				<xsl:call-template name="eo-kodigo">
				  <xsl:with-param name="str"><xsl:value-of select="$refkls"/></xsl:with-param>
				</xsl:call-template>
				<xsl:text>.html</xsl:text>
			      </xsl:attribute>
			      <img border="0" src="../smb/listo.gif"/>
			      <xsl:value-of select="translate($refkls,'_',' ')"/>
			    </a>
			  </li>
			</xsl:when>
			<xsl:otherwise>
			  <li>
			    <a>
			      <xsl:attribute name="href">
				<xsl:text>#</xsl:text>
				<xsl:call-template name="eo-kodigo">
				  <xsl:with-param name="str"><xsl:value-of select="$refkls"/></xsl:with-param>
				</xsl:call-template>
			      </xsl:attribute>  
			      <img border="0" src="../smb/listo.gif"/>
			      <xsl:value-of select="translate($refkls,'_',' ')"/>
			    </a>
			  </li>
			</xsl:otherwise>
		      </xsl:choose>
                    </xsl:for-each>
		  </ul>
		  
		  <!-- rektaj klasanoj -->
		  <xsl:for-each select="$root">
                    <xsl:call-template name="klasanoj">
                      <xsl:with-param name="klaso"
				      select="concat('voko:',$kls)"/>
		      <xsl:with-param name="ordigita"
				      select="$ordigita"/>
                    </xsl:call-template>
		  </xsl:for-each>

                  <!-- anojn de integritaj klasoj prezentu en sama dosiero, sed en propra
		  chapitro -->
                  <xsl:for-each select="kls[@prezento='integrita']">
                     <xsl:variable name="intkls"
				   select="substring-after(@nom,'#')"/>
		     <xsl:variable name="ordigita"
				   select="@ordigita"/>
                     <a>
                      <xsl:attribute name="name">
                        <xsl:call-template name="eo-kodigo">
			  <xsl:with-param name="str"><xsl:value-of select="$intkls"/></xsl:with-param>
			</xsl:call-template>
		      </xsl:attribute>
		     </a>
                     <h2>
		       <xsl:value-of select="translate($intkls,'_',' ')"/>
		     </h2>
	             <xsl:for-each select="$root">
                       <xsl:call-template name="klasanoj">
                         <xsl:with-param name="klaso"
					 select="concat('voko:',$intkls)"/>
			 <xsl:with-param name="ordigita"
					 select="$ordigita"/>
                       </xsl:call-template>
		     </xsl:for-each>
                  </xsl:for-each>

		</td>
              </tr>
            </table>
          </body>
	</html>
	<!-- /redirect:write -->
      </xsl:result-document>
    </xsl:if>
  </xsl:for-each>
</xsl:template>


<xsl:template name="klasanoj">
  <xsl:param name="klaso"/>
  <xsl:param name="ordigita"/>

  <xsl:choose>
    <xsl:when test="$ordigita='jes'">
      <xsl:for-each select="tez/nod[lst/r/@l=$klaso]">
	<xsl:sort select="lst/r[@l=$klaso]/@v" data-type="number"/>
	<p class="tez">
	  <xsl:call-template name="art-ref">
	    <xsl:with-param name="title" select="concat('n-ro: ',lst/r[@l=$klaso]/@v)"/>
	  </xsl:call-template>
	</p>
      </xsl:for-each>
    </xsl:when>
    
    <xsl:otherwise>
      <xsl:for-each select="tez/nod[lst/r/@l=$klaso]">
	<xsl:sort lang="eo"
		  collation="http://saxon.sf.net/collation?class=de.steloj.respiro.EsperantoCollator" 
		  select="translate(k,'-( )','')"/>
	<p class="tez">
	  <xsl:call-template name="art-ref"/>
	</p>
      </xsl:for-each>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>


<xsl:template name="art-ref">
  <xsl:param name="title"/>
  <xsl:choose>
    <xsl:when test="contains(@mrk,'.')">
      <a href="../art/{substring-before(@mrk,'.')}.html#{@mrk}" 
        target="precipa">
	<xsl:if test="$title">
	  <xsl:attribute name="title">
	    <xsl:value-of select="$title"/>
	  </xsl:attribute>
	</xsl:if>
        <xsl:apply-templates select="k"/>
	<xsl:apply-templates select="mlg"/>
      </a>
    </xsl:when>
    <xsl:otherwise>
      <a href="../art/{@mrk}.html" target="precipa">
        <xsl:apply-templates select="k"/>
	<xsl:apply-templates select="mlg"/>
      </a>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>



<xsl:template name="menuo-eo">
  <xsl:variable name="aktiva" select="'_eo.html'"/>
  <tr>
    <xsl:for-each select="$enhavo-root//pagho[not(@kashita='jes')]">
      <xsl:choose>
        <xsl:when test="@dosiero=$aktiva">
          <td class="aktiva">
            <a href="../inx/{@dosiero}">
              <xsl:value-of select="@titolo"/>
            </a>
          </td>
        </xsl:when>
        <xsl:otherwise>
          <td class="fona">
            <a href="../inx/{@dosiero}">
              <xsl:value-of select="@titolo"/>
            </a>
          </td>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:for-each>     
  </tr>
</xsl:template>


<xsl:template match="k">
  <xsl:apply-templates/>
  <xsl:if test="@n"><sup><xsl:value-of select="@n"/></sup></xsl:if>
</xsl:template>

<xsl:template match="mlg">
  <xsl:text> (</xsl:text>
  <xsl:apply-templates/>
  <xsl:text>)</xsl:text>
</xsl:template>

<!-- /xsl:stylesheet -->
</xsl:transform>









