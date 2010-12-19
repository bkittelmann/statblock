from lxml import etree

import os.path

class CssDocumentResolver(etree.Resolver):
    "Returns the content of a resolved document as a raw text node."
    
    def __init__(self, base_dir):
        self.base_dir = base_dir
        
    def resolve(self, url, public_id, context):
        css = open(os.path.join(self.base_dir, url)).read()
        css_elem = etree.Element("css")
        css_elem.text = str(css)
        # needs to return a complete XML node, client can extract CSS from text content
        return self.resolve_string(etree.tostring(css_elem), context)


class XslRenderer(object):
    "Renders an XML character document to an XHTML representation."
    
    def render(self, document, stylesheet):
        def upper(context, value): 
            return value.upper()
        
        def join(context, separator, nodes):
            return separator.join([n.text for n in nodes])
                
        ns = etree.FunctionNamespace('http://github/bkittelmann/statblock')
        ns.prefix = 'py'
        ns['upper'] = upper
        ns['join'] = join
        
        base_dir = os.path.dirname(__file__)
        style_path = os.path.join(base_dir, stylesheet)
        
        parser = etree.XMLParser()
        parser.resolvers.add(CssDocumentResolver(base_dir))
        xslt_doc = etree.parse(open(style_path), parser)
        
        transform = etree.XSLT(xslt_doc)
        return transform(document)

