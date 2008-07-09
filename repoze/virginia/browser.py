import os
import mimetypes

mimetypes.add_type('text/html', '.stx')

from zope.component import getMultiAdapter
from zope.structuredtext import stx2html

from webob import Response

from repoze.bfg.interfaces import IViewFactory

class BrowserView(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

class FileView(BrowserView):
    def __call__(self, *arg, **kw):
        dirname, filename = os.path.split(self.context.path)
        name, ext = os.path.splitext(filename)
        renderer = getMultiAdapter((self.context, self.request),
                                   IViewFactory, name=ext)
        result = renderer()
        response = Response(result)
        mt, encoding = mimetypes.guess_type(filename)
        response.content_type = mt or 'text/plain'
        return Response(result)

class DirectoryView(BrowserView):
    defaults = ('index.html', 'index.stx')
    def __call__(self, *arg, **kw):
        index = None
        for name in self.defaults:
            try:
                index = self.context[name]
            except KeyError:
                pass
        if index is None:
            response = Response('No default view for %s' % self.context.path)
        else:
            fileview = FileView(index, self.request)
            return fileview()
        
class StructuredTextView(BrowserView):
    """ Filesystem-based STX view
    """
    def __call__(self, *arg, **kw):
        """ Render source as STX.
        """
        return stx2html(self.context.source)

class HTMLView(BrowserView):
    """ Filesystem-based HTML view
    """
    def __call__(self, *arg, **kw):
        """ Render html.
        """
        return self.context.source
