import unittest
from zope.component.testing import PlacelessSetup

class FileViewTests(unittest.TestCase, PlacelessSetup):
    def setUp(self):
        PlacelessSetup.setUp(self)

    def tearDown(self):
        PlacelessSetup.tearDown(self)

    def _getTargetClass(self):
        from repoze.virginia.browser import FileView
        return FileView

    def _makeOne(self, *arg, **kw):
        klass = self._getTargetClass()
        return klass(*arg, **kw)

    def _registerViewFactory(self, app, name, *for_):
        import zope.component
        gsm = zope.component.getGlobalSiteManager()
        from repoze.bfg.interfaces import IViewFactory
        gsm.registerAdapter(app, for_, IViewFactory, name)

    def test___call__(self):
        response = DummyResponse()
        viewfactory = make_view_factory(response)
        context = DummyFile('/foo/bar.ext')
        self._registerViewFactory(viewfactory, '.ext', None, None)
        view = self._makeOne(context, None)
        self.assertEqual(view(), response)

class DirectoryViewTests(unittest.TestCase, PlacelessSetup):
    def setUp(self):
        PlacelessSetup.setUp(self)

    def tearDown(self):
        PlacelessSetup.tearDown(self)

    def _getTargetClass(self):
        from repoze.virginia.browser import DirectoryView
        return DirectoryView

    def _makeOne(self, *arg, **kw):
        klass = self._getTargetClass()
        return klass(*arg, **kw)

    def _registerViewFactory(self, app, name, *for_):
        import zope.component
        gsm = zope.component.getGlobalSiteManager()
        from repoze.bfg.interfaces import IViewFactory
        gsm.registerAdapter(app, for_, IViewFactory, name)

    def test___call___index_html(self):
        context = DummyDirectory('/',{'index.html':DummyFile('/index.html')})
        response = DummyResponse()
        viewfactory = make_view_factory(response)
        self._registerViewFactory(viewfactory, '.html', None, None)
        view = self._makeOne(context, None)
        self.assertEqual(view(), response)

    def test___call___index_stx(self):
        context = DummyDirectory('/',{'index.stx':DummyFile('/index.stx')})
        response = DummyResponse()
        viewfactory = make_view_factory(response)
        self._registerViewFactory(viewfactory, '.stx', None, None)
        view = self._makeOne(context, None)
        self.assertEqual(view(), response)

    def test___call___noindex(self):
        context = DummyDirectory('/',{})
        view = self._makeOne(context, None)
        response = view()
        self.assertEqual(response.app_iter, ['No default view for /'])

class StructuredTextViewTests(unittest.TestCase):
    def _getTargetClass(self):
        from repoze.virginia.browser import StructuredTextView
        return StructuredTextView

    def _makeOne(self, *arg, **kw):
        klass = self._getTargetClass()
        return klass(*arg, **kw)

    def test___call__(self):
        context = DummyFile('/foo/bar.ext')
        context.source = 'abcdef'
        view = self._makeOne(context, None)
        response = view()
        self.assertEqual(response.app_iter,
                         ['<html>\n<body>\n<p>abcdef</p>\n</body>\n</html>\n']
                         )
        headers = response.headerlist
        self.assertEqual(headers[0],
                         ('Content-Length', '44')
                         )
        self.assertEqual(headers[1],
                         ('content-type', 'text/html; charset=UTF-8')
                         )

class RawViewTests(unittest.TestCase):
    def _getTargetClass(self):
        from repoze.virginia.browser import RawView
        return RawView

    def _makeOne(self, *arg, **kw):
        klass = self._getTargetClass()
        return klass(*arg, **kw)

    def test___call__(self):
        context = DummyFile('/foo/bar.txt')
        context.source = 'abcdef'
        view = self._makeOne(context, None)
        response = view()
        self.assertEqual(response.app_iter, ['abcdef'])
        headers = response.headerlist
        self.assertEqual(headers[0],
                         ('Content-Length', '6')
                         )
        self.assertEqual(headers[1],
                         ('content-type', 'text/plain; charset=UTF-8')
                         )
        
class DummyDirectory:
    def __init__(self, path, subs):
        self.path = path
        self.subs = subs

    def __getitem__(self, name):
        return self.subs[name]

class DummyFile:
    source = None
    def __init__(self, path):
        self.path = path
    
class DummyResponse:
    status = '200 OK'
    headerlist = ()
    app_iter = ()

def make_view_factory(response):
    class DummyViewFactory:
        def __init__(self, context, request):
            self.context = context
            self.request = request

        def __call__(self):
            return response
    return DummyViewFactory
