# -*- coding: utf-8 -*-
from words import tld_to_string
from utilities import clean_string

"""Flatten methods, node-specific. We use reflection to pick the right
one.

These methods are catch-alls, but for some nodes (such as definitions)
we have written custom methods outside of this module.

"""

class SkipNodes(Exception):
    """If we have reached a node that we want to skip, and we want to
    skip its children we throw this exception.

    """
    pass
def _flatten_tld(tld_node):
    """<tld/> means the root for this word.

    """
    return tld_to_string(tld_node)

def _flatten_ctl(ctl_node):
    """<ctl> means quotation mark ('citilo'). We've chosen to use the
    same type of quotation mark as the Esperanto wikipedia. Note
    clean_string has to deal with cases where literal quotes are used.

    """
    if ctl_node.text:
        return u"«%s»" % ctl_node.text
    else:
        return ""

def _flatten_ind(ind_node):
    """Relates to a ReVo index somehow. The ReVo index isn't relevant
    to us but the content of the node is.

    """
    if ind_node.text:
        return ind_node.text
    else:
        return ""

def _flatten_fnt(fnt_node):
    """<fnt> is for attribution of examples. We ignore it and all its
    children. 

    """
    raise SkipNodes()

def _flatten_generic(node):
    """Flatten a node for which we don't have any corner cases to deal
    with.

    """
    if node.text:
        return node.text
    else:
        return ""

# high level method:
def flatten_node(node):
    """Return a friendly string representing the contents of this node
    and its children. This method is generic although occasionally we
    need methods which are specific to a certain node type.

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

    def flatten(node):
        """Recursively flatten this structure. If we've defined a
        flatten method for this type of node, we use reflection to get
        it.

        """
        # try to find a method defined for this node type
        flatten_method_name = '_flatten_' + node.tag
        if flatten_method_name in globals():
            flatten_method = globals()[flatten_method_name]
        else:
            print 'Warning: no specific way of handling <%s>' % node.tag
            flatten_method = _flatten_generic

        # apply the flatten method we found
        flat_string = ""

        try:
            flat_string += flatten_method(node)

            # flatten children
            for child in node.getchildren():
                flat_string += flatten(child)

            # add any trailing text
            if node.tail:
                flat_string += node.tail
        except SkipNodes:
            pass

        return flat_string
        

    flat_string = ""

    if node.text:
        flat_string += node.text
    
    for child in node.getchildren():
        flat_string += flatten(child)

    return clean_string(flat_string)

