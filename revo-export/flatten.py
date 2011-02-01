# -*- coding: utf-8 -*-
from utilities import (clean_string, tld_to_string,
                       expand_bibliography_abbreviation)

"""Flatten methods, node-specific. We use reflection to pick the right
one.

These methods are catch-alls, but for some nodes (such as definitions)
we have written custom methods outside of this module.

"""

def _flatten_tld(tld_node, **kwargs):
    """<tld/> means the root for this word.

    """
    return tld_to_string(tld_node)

def _flatten_ind(ind_node, **kwargs):
    """Relates to a ReVo index somehow. The ReVo index isn't relevant
    to us but the content of the node is.

    """
    if ind_node.text:
        return ind_node.text
    else:
        return ""

def _flatten_rim(rim_node, **kwargs):
    """A remark.

    Example input:

    <rim>
      La vorto aperas en la Fundamento nur en la formo
      <ctl>L. L. Zamenhof</ctl>.
    </rim>
    (from zamenhof.xml)

    """
    remark_string = "Rimarko: "
    if rim_node.text:
        remark_string += rim_node.text

    return remark_string

def _flatten_refgrp(refgrp_node, **kwargs):
    """A <refgrp> holds a collection of references (<ref>s). We only
    label the reference type here, using plurals if there are multiple
    references of a given type.

    """
    # occasionally contains text making some comment (e.g. absorb.xml)
    # in which case we don't label by type of reference
    if refgrp_node.text and refgrp_node.text.strip():
        return refgrp_node.text

    if kwargs.get('label_references', True):
        if refgrp_node.attrib.get('tip') == 'dif':
            return "Vidu: "

        if refgrp_node.attrib.get('tip') == 'vid':
            return u"Vidu ankaŭ: "

        if refgrp_node.attrib.get('tip') == 'sin':
            child_references = refgrp_node.findall('ref')
            if len(child_references) > 1:
                return "Sinonimoj: "
            else:
                return "Sinonimo: "

        if refgrp_node.attrib.get('tip') == 'ant':
            child_references = refgrp_node.findall('ref')
            if len(child_references) > 1:
                return "Antonimoj: "
            else:
                return "Antonimo: "

        if refgrp_node.attrib.get('tip') == 'super':
            child_references = refgrp_node.findall('ref')
            if len(child_references) > 1:
                return "Supernocioj: "
            else:
                return "Supernocio: "

        if refgrp_node.attrib.get('tip') == 'sub':
            child_references = refgrp_node.findall('ref')
            if len(child_references) > 1:
                return "Subnocioj: "
            else:
                return "Subnocio: "

    return ""

def _flatten_ref(ref_node, **kwargs):
    """A <ref> is a reference to another word. This may be an inline
    reference that we just treat as text, or may be a 'see also' /
    synonym / antonym which we add text to say so (ReVo just uses
    symbols for this).

    <ref>s that we just treat as text are often labelled as to how
    they relate (e.g. x is a part of y uses tip='prt') but this is not
    relevant to us.

    """
    reference = ""

    if ref_node.text:
        reference += ref_node.text

    if kwargs.get('label_references', True):
        # add 'see', in other words this term is defined elsewhere
        if ref_node.attrib.get('tip') == 'dif':
            return "Vidu: " + reference.strip()

        # add 'see also'
        if ref_node.attrib.get('tip') == 'vid':
            return u"Vidu ankaŭ: " + reference.strip()

        # add synonym note if appropriate
        if ref_node.attrib.get('tip') == 'sin':
            reference = "Sinonimo: " + reference.strip()

        # add antonym note if appropriate
        if ref_node.attrib.get('tip') == 'ant':
            reference = "Antonimo: " + reference.strip()

        # supernotion/subnotion
        if ref_node.attrib.get('tip') == 'super':
            reference = "Supernocio: " + reference.strip()
        if ref_node.attrib.get('tip') == 'sub':
            reference = "Subnocio: " + reference.strip()

    return reference

def _flatten_bib(node, **kwargs):
    if node.text:
        return expand_bibliography_abbreviation(node.text)
    else:
        return ""

def _flatten_generic(node, **kwargs):
    """Flatten a node for which we don't have any corner cases to deal
    with.

    """
    if node.text:
        return node.text
    else:
        return ""

def get_flatten_method(node):
    """Use reflection to find a node type specific flattener if
    one exists, otherwise return a generic flattener.
    
    """
    # try to find a method defined for this node type
    flatten_method_name = '_flatten_' + node.tag
    if flatten_method_name in globals():
        return globals()[flatten_method_name]
    else:
        return _flatten_generic

def _flatten(node, skip_tags=None, label_references=True):
    """Recursively flatten this structure. If we've defined a
    flatten method for this type of node, we use reflection to get
    it.

    We must handle quotes (citiloj = <ctl>) at this level, since we
    need to be able to handle situations such as

    <ctl>Foo <tld/> bar</ctl> 

    which require everything inside to be flattened. Note clean_string
    handles literal quotation marks.

    """
    if skip_tags:
        if node.tag in skip_tags:
            if node.tail:
                return node.tail
            return ""

    # get and apply the matching flatten method
    flatten_method = get_flatten_method(node)
    flat_string = flatten_method(node, label_references=label_references)

    # flatten children
    for child in node.getchildren():
        flat_string += _flatten(child, skip_tags, label_references)

    # deal with quotes now the string is flat
    if node.tag == 'ctl':
        flat_string = u"«%s»" % flat_string

    # add any trailing text
    if node.tail:
        flat_string += node.tail

    return flat_string

# high level method:
def flatten_node(node, skip_tags=None, label_references=True):
    """Return a friendly string representing the contents of this node
    and its children. This method is generic although occasionally we
    need methods which are specific to a certain node type.

    skip_tags specifies node tags for a node which we don't recurse
    into (although we will collect its tail, since that is outside).

    label_references specifies whether <ref>s are preceded with text
    describing them ('vidu ankaŭ', 'sinonimoj' and so on).

    Some examples:

    <rim>
      La tuta terminologio pri <tld/>oj, <tld/>-vektoroj kaj -subspacoj
      de endomorfio ekzistas anka&ubreve; 
      por <frm>(<k>n</k>,<k>n</k>)</frm>-matrico, konvencie
      identigita kun la endomorfio, kies matrico rilate al la kanona bazo
      de <frm><g>K</g><sup><k>n</k></sup></frm> &gcirc;i estas.
    </rim>
    (from ajgen.xml)

    <ekz>
      <ctl>popolo</ctl>, <ctl>foliaro</ctl>, <ctl>herbo</ctl>,
      <ctl>armeo</ctl> estas ar<tld/>oj.
    </ekz>
    (from vort.xml)

    <ekz>
      <ind>saluton!</ind>
      [...]
    </ekz>
    (from salut.xml)

    <klr>(de <ref cel="polino.0o">polinomo</ref>)</klr>
    (from radik.xml)

    """
    flatten_method = get_flatten_method(node)

    flat_string = flatten_method(node, label_references=label_references)
    
    for child in node.getchildren():
        flat_string += _flatten(child, skip_tags,
                                label_references=label_references)

    return clean_string(flat_string)

