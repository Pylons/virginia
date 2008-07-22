import unittest
from zope.component.testing import PlacelessSetup

class FileViewTests(unittest.TestCase, PlacelessSetup):
    def setUp(self):
        PlacelessSetup.setUp(self)

    def tearDown(self):
        PlacelessSetup.tearDown(self)

    def _getFUT(self):
        from repoze.virginia.views import file_view
        return file_view

    def _registerView(self, app, name, *for_):
        import zope.component
        gsm = zope.component.getGlobalSiteManager()
        from repoze.bfg.interfaces import IView
        gsm.registerAdapter(app, for_, IView, name)

    def test___call__(self):
        response = DummyResponse()
        view = make_view(response)
        context = DummyFile('/foo/bar.ext')
        self._registerView(view, '.ext', None, None)
        view = self._getFUT()
        result = view(context, None)
        self.assertEqual(result, response)

class DirectoryViewTests(unittest.TestCase, PlacelessSetup):
    def setUp(self):
        PlacelessSetup.setUp(self)

    def tearDown(self):
        PlacelessSetup.tearDown(self)

    def _getFUT(self):
        from repoze.virginia.views import directory_view
        return directory_view

    def _getEnviron(self, **kw):
        environ = {'PATH_INFO':'/'}
        environ.update(kw)
        return environ

    def _registerView(self, app, name, *for_):
        import zope.component
        gsm = zope.component.getGlobalSiteManager()
        from repoze.bfg.interfaces import IView
        gsm.registerAdapter(app, for_, IView, name)

    def test___call___index_html(self):
        context = DummyDirectory('/',{'index.html':DummyFile('/index.html')})
        response = DummyResponse()
        view = make_view(response)
        self._registerView(view, '.html', None, None)
        view = self._getFUT()
        environ = self._getEnviron()
        request = DummyRequest(environ)
        result = view(context, request)
        self.assertEqual(result, response)

    def test___call___index_stx(self):
        context = DummyDirectory('/',{'index.stx':DummyFile('/index.stx')})
        response = DummyResponse()
        view = make_view(response)
        self._registerView(view, '.stx', None, None)
        view = self._getFUT()
        environ = self._getEnviron()
        request = DummyRequest(environ)
        result = view(context, request)
        self.assertEqual(result, response)

    def test___call___noindex(self):
        context = DummyDirectory('/',{})
        view = self._getFUT()
        environ = self._getEnviron()
        request = DummyRequest(environ)
        result = view(context, request)
        self.assertEqual(result.app_iter, ['No default view for /'])

    def test___call___redirects_to_slash(self):
        context = DummyDirectory('/',{})
        view = self._getFUT()
        environ = self._getEnviron(PATH_INFO='')
        request = DummyRequest(environ)
        result = view(context, request)
        self.assertEqual(result.status, '302 Found')
        self.assertEqual(result.headers['Location'], '/')

class StructuredTextViewTests(unittest.TestCase):
    def _getFUT(self):
        from repoze.virginia.views import structured_text_view
        return structured_text_view

    def test___call__(self):
        context = DummyFile('/foo/bar.ext')
        context.source = 'abcdef'
        response = self._getFUT()(context, None)
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
    def _getFUT(self):
        from repoze.virginia.views import raw_view
        return raw_view

    def test___call__(self):
        context = DummyFile('/foo/bar.txt')
        context.source = 'abcdef'
        response = self._getFUT()(context, None)
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


class DummyRequest:
    def __init__(self, environ):
        self.environ = environ
        
class DummyResponse:
    status = '200 OK'
    headerlist = ()
    app_iter = ()

def make_view(response):
    def view(context, request):
        return response
    return view

