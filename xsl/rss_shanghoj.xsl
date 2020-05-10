<!DOCTYPE xsl:transform>

<xsl:transform
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:xs="http://www.w3.org/2001/XMLSchema"
  xmlns:saxon="http://saxon.sf.net/"
  version="2.0"
  extension-element-prefixes="saxon" 
>

<!-- xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                version="1.0"
    xmlns:redirect="http://xml.apache.org/xalan/redirect"
    extension-element-prefixes="redirect" -->


<!-- (c) 2015 che Wolfram Diestel
     licenco GPL 2.0
-->

<xsl:param name="kreotempo"/>
<xsl:param name="channel"/>

<xsl:output method="xml" encoding="utf-8" indent="yes"/>
<xsl:variable name="baseurl">http://retavortaro.de/revo/art</xsl:variable>

<!--
<xsl:key name="autoroj" match="//entry" use="substring-before(msg,':')"/>
-->

<xsl:template match="/">
  <rss version="2.0">
    <xsl:choose>
      <xsl:when test="$channel='novaj'">
	<xsl:call-template name="novaj"/>
      </xsl:when>
      <xsl:otherwise>
	<xsl:call-template name="shanghoj"/> 
      </xsl:otherwise>
    </xsl:choose>

  </rss>
</xsl:template>


<xsl:template name="shanghoj">
  <channel>
      <title>Reta Vortaro - laste &#x015d;an&#x011d;itaj artikoloj</title>
      <link>http://retavortaro.de</link>
      <description>Listo de lasta ŝanĝitaj artikoloj de Reta
      Vortaro</description>
      <language>eo</language>
      <pubDate>
	<xsl:value-of select="$kreotempo"/>
      </pubDate>
      <image>
	<url>http://www.reta-vortaro.de/revo/reto.gif</url>
	<title>Reta Vortaro</title>
      </image>


      <xsl:apply-templates/>
  </channel>
</xsl:template>


<xsl:template name="novaj">
  <channel>
      <title>Reta Vortaro - novaj artikoloj</title>
      <link>http://retavortaro.de</link>
      <description>Listo de novaj artikoloj de Reta
      Vortaro</description>
      <language>eo</language>
      <pubDate>
	<xsl:value-of select="$kreotempo"/>
      </pubDate>
      <image>
	<url>http://www.reta-vortaro.de/revo/reto.gif</url>
	<title>Reta Vortaro</title>
      </image>


      <xsl:apply-templates select="//entry[file/revision='1.1']"/>
  </channel>
</xsl:template>

<xsl:template match="entry">
  <item>
    <xsl:apply-templates/>
  </item>
</xsl:template>

<xsl:template match="file">
  <title>
    <xsl:value-of select="substring-before(name,'.xml')"/>
  </title>
  <guid>
    <xsl:value-of select="name"/>
    <xsl:text> versio </xsl:text>
    <xsl:value-of select="revision"/>
  </guid>
  <link>
    <xsl:value-of select="concat($baseurl,'/',substring-before(name,'.xml'),'.html')"/>
  </link>
</xsl:template>

<xsl:template match="msg">
  <author>
    <xsl:choose>
      <xsl:when test="substring-before(.,':')">
        <xsl:value-of select="substring-before(.,':')"/>
      </xsl:when>
      <xsl:otherwise>
	<xsl:value-of select="../author"/>
      </xsl:otherwise>
    </xsl:choose>
  </author>
  <description>
    <xsl:choose>
      <xsl:when test="substring-after(.,':')">
        <xsl:value-of select="normalize-space(substring-after(.,':'))"/>
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="."/>
      </xsl:otherwise>
    </xsl:choose>
  </description>
</xsl:template>

<xsl:template match="author"/>

<xsl:template match="date">
  <pubDate>
    <xsl:value-of select="."/>
    <xsl:text> </xsl:text>
    <xsl:value-of select="../time"/>
  </pubDate>
</xsl:template>

<xsl:template match="time"/>

<!--
                  <xsl:attribute name="name">
                    <xsl:call-template name="autoro">
                      <xsl:with-param name="spaco" select="'_'"/>
                    </xsl:call-template>
                  </xsl:attribute>
                </a>
                <h2>
                  <xsl:call-template name="autoro">
                    <xsl:with-param name="spaco" select="' '"/>
                  </xsl:call-template>
                </h2>


<xsl:template name="autoro">
  <xsl:param name="spaco"/>
  <xsl:choose>
    <xsl:when test="substring-before(ancestor-or-self::entry/msg,':')">
      <xsl:value-of select="translate(substring-before(ancestor-or-self::entry/msg,':'),' ',$spaco)"/>
    </xsl:when>
    <xsl:otherwise>
      <xsl:text>revo</xsl:text>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template match="entry">
  <xsl:apply-templates select="file"/>
</xsl:template>

<xsl:template match="entry/file">
  <dt>
    <a target="precipa">
     <xsl:attribute name="href">
       <xsl:text>../art/</xsl:text>
       <xsl:value-of select="substring-before(name,'.xml')"/>
       <xsl:text>.html</xsl:text>
     </xsl:attribute>
     <b><xsl:value-of select="substring-before(name,'.xml')"/></b>
    </a> 
    <xsl:text> </xsl:text>
    <span class="dato"><xsl:value-of select="../date"/></span>
  </dt>
  <dd>
    <xsl:choose>
      <xsl:when test="substring-after(../msg,':')">
        <xsl:value-of select="substring-after(../msg,':')"/>
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="../msg"/>
      </xsl:otherwise>
    </xsl:choose>
  </dd>
</xsl:template>


<xsl:template name="nova_artikolo">
  <dt>
    <a target="precipa">
     <xsl:attribute name="href">
       <xsl:text>../art/</xsl:text>
       <xsl:value-of select="substring-before(name,'.xml')"/>
       <xsl:text>.html</xsl:text>
     </xsl:attribute>
     <b><xsl:value-of select="substring-before(name,'.xml')"/></b>
    </a> 
    <xsl:text> </xsl:text>
    <span class="dato"><xsl:value-of select="../date"/></span>
  </dt>
  <dd>
    <xsl:text>de </xsl:text>
    <xsl:call-template name="autoro">
      <xsl:with-param name="spaco" select="' '"/>
    </xsl:call-template>
  </dd>
</xsl:template>

-->


<!-- /xsl:stylesheet -->
</xsl:transform>



