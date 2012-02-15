import unittest
from pyramid import testing
from pyramid.interfaces import IResponse
from zope.interface import implementer

class FileViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def _getFUT(self):
        from virginia.views import file_view
        return file_view

    def test___call__(self):
        response = DummyResponse()
        view = make_view(response)
        context = DummyFile('/foo/bar.ext')
        self.config.add_view(view, name='.ext')
        view = self._getFUT()
        request = testing.DummyRequest()
        result = view(context, request)
        self.assertEqual(result, response)

class DirectoryViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def _getFUT(self):
        from virginia.views import directory_view
        return directory_view

    def _getEnviron(self, **kw):
        environ = {'PATH_INFO':'/'}
        environ.update(kw)
        return environ

    def test___call___index_html(self):
        context = DummyDirectory('/',{'index.html':DummyFile('/index.html')})
        response = DummyResponse()
        view = make_view(response)
        self.config.add_view(view, name='.html')
        view = self._getFUT()
        environ = self._getEnviron()
        request = testing.DummyRequest(environ=environ)
        result = view(context, request)
        self.assertEqual(result, response)

    def test___call___index_stx(self):
        context = DummyDirectory('/',{'index.stx':DummyFile('/index.stx')})
        response = DummyResponse()
        view = make_view(response)
        self.config.add_view(view, name='.stx')
        view = self._getFUT()
        environ = self._getEnviron()
        request = testing.DummyRequest(environ=environ)
        result = view(context, request)
        self.assertEqual(result, response)

    def test___call___noindex(self):
        context = DummyDirectory('/',{})
        view = self._getFUT()
        environ = self._getEnviron()
        request = testing.DummyRequest(environ=environ)
        result = view(context, request)
        self.assertEqual(result.app_iter, ['No default view for /'])

    def test___call___redirects_to_slash(self):
        context = DummyDirectory('/',{})
        view = self._getFUT()
        environ = self._getEnviron(PATH_INFO='')
        request = testing.DummyRequest(environ=environ)
        result = view(context, request)
        self.assertEqual(result.status, '302 Found')
        self.assertEqual(result.headers['Location'], '/')

class StructuredTextViewTests(unittest.TestCase):
    def _getFUT(self):
        from virginia.views import structured_text_view
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
                         ('Content-Type', 'text/html; charset=UTF-8')
                         )

class RawViewTests(unittest.TestCase):
    def _getFUT(self):
        from virginia.views import raw_view
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
                         ('Content-Type', 'text/plain; charset=UTF-8')
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

@implementer(IResponse) # dont try to convert to response when returned
class DummyResponse:
    status = '200 OK'
    headerlist = ()
    app_iter = ()

def make_view(response):
    def view(context, request):
        return response
    return view

