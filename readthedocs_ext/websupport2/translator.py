# -*- coding: utf-8 -*-

# From sphinx.writers.websupport

import hashlib

from sphinx.writers.html import HTMLTranslator
from sphinx.util.websupport import is_commentable


class UUIDTranslator(HTMLTranslator):

    """
    Our custom HTML translator.

    index = node.parent.index(node)
    parent = node.parent
    document = node.document
    text = node.astext()
    source = node.rawsource
    """

    def __init__(self, builder, *args, **kwargs):
        HTMLTranslator.__init__(self, builder, *args, **kwargs)
        self.comment_class = 'sphinx-has-comment'

    def dispatch_visit(self, node):
        if is_commentable(node):
            self.handle_visit_commentable(node)
        HTMLTranslator.dispatch_visit(self, node)

    def hash_node(self, node):
        source = node.rawsource or node.astext()

        try:
            ret = u'md5-%s' % hashlib.md5(source).hexdigest()
        except UnicodeEncodeError:
            ret = u'md5-%s' % hashlib.md5(source.decode('ascii', 'ignore')).hexdigest()
        return ret

    def handle_visit_commentable(self, node):
        # We will place the node in the HTML id attribute. If the node
        # already has an id (for indexing purposes) put an empty
        # span with the existing id directly before this node's HTML.
        self.add_db_node(node)
        if node.attributes['ids']:
            self.body.append('<span id="%s"></span>'
                             % node.attributes['ids'][0])
        node.attributes['ids'] = ['%s' % self.hash_node(node)]
        node.attributes['classes'].append(self.comment_class)

    def add_db_node(self, node):
        storage = self.builder.storage
        _hash = self.hash_node(node)
        if not storage.has_node(_hash):
            storage.add_node(id=_hash,
                             document=self.builder.current_docname,
                             source=node.rawsource or node.astext())