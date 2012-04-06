# BEXML, a fast Bugs Everywhere parser with RESTful API and other issue tracker backends
# (C) 2012 Niall Douglas http://www.nedproductions.biz/
# Created: March 2012

from ..xmlparserbase import XMLComment, XMLIssue, XMLParser

import os, logging

log=logging.getLogger(__name__)


class BEXMLComment(XMLComment):
    """A comment loaded from an XML based BE repo"""

    def __init__(self, parentIssue, commentelem):
        XMLComment.__init__(self, parentIssue, commentelem)


class BEXMLIssue(XMLIssue):
    """An issue loaded from an XML based BE repo"""

    def __init__(self, bugelem):
        XMLIssue.__init__(self, bugelem, mapToBE={'created':('time', lambda xmlelem:xmlelem.text), 'extra-string':('extra-strings', lambda xmlelem:xmlelem.text)}, dontprocess=set(['comment']))
        for valueelem in self.element.findall("comment"):
            if valueelem.tag=="comment":
                self.addComment(BEXMLComment(self, valueelem))


class BEXMLParser(XMLParser):
    """Parses an XML based BE repo"""

    @classmethod
    def _schemapath(cls):
        return os.path.join(os.path.dirname(__file__), "bexml.xsd")

    def _XMLIssue(self, bugelem, **pars):
        return BEXMLIssue(bugelem, **pars)

    def __init__(self, uri, encoding="utf-8"):
        XMLParser.__init__(self, uri, encoding)

    def try_location(self, mimetype=None, first256bytes=None):
        score, errmsg=XMLParser.try_location(self, mimetype, first256bytes)
        if score>=0 and first256bytes is not None and '<be-xml>' in first256bytes: score+=100
        return (score, errmsg)

def instantiate(uri, **args):
    return BEXMLParser(uri, **args)
