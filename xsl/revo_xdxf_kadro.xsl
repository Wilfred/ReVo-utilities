<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
		version="1.0">


<!-- (c) 2015 che Wolfram Diestel 
     licenco GPL 2.0

reguloj por XDXF universala vortar-intershangha formato

-->

<xsl:output method="xml" encoding="utf-8"/>

<xsl:template match="/xml">
<!--
<!DOCTYPE xdxf SYSTEM
"https://raw.github.com/soshial/xdxf_makedict/master/format_standard/xdxf_strict.dtd">
-->
  <xdxf lang_from="EPO" lang_to="EPO" format="logical" revision="032beta">
    <meta_info>
        <title>Reta Vortaro</title>
        <full_title>Reta Vortaro</full_title>
        <description>Reta Vortaro de Esperanto kun difinoj kaj tradukoj</description>
        <abbreviations>
          <abbr_def><abbr_k>tr.</abbr_k> <abbr_v>transitiva verbo</abbr_v></abbr_def>
          <abbr_def><abbr_k>ntr.</abbr_k> <abbr_v>netransitiva verbo</abbr_v></abbr_def>
        </abbreviations>
        <file_version>001</file_version>
        <creation_date>2015-04-14</creation_date>
    </meta_info>
    <lexicon>
      <xsl:copy-of select="*"/>
    </lexicon>
  </xdxf>
 
</xsl:template>

</xsl:stylesheet>












