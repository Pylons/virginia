# publish a filesystem tree
import os
import sys

from paste import httpexceptions

from zope.interface import implements
from zope.component import getAdapter

from repoze.virginia.filesys import os_filesystem
from repoze.virginia.interfaces import IFile
from repoze.virginia.interfaces import IView

def cleanPath(path):
    # Cleanup the path list
    clean = []
    for item in path.split('/'):
        if not item or item=='.':
            continue
        elif item == '..':
            del clean[-1]
        else:
            clean.append(item)
    return ['/'] + clean


class VirginiaObobHelper:
    def __init__(self, environ, **config):
        self.root = config['root']
        self.encoding = config.get('encoding', 'utf-8')
        self.default_viewname = config.get('default_viewname', 'index.pt')
        self.environ = environ
        self.fs = os_filesystem(self.root)

    def setup(self):
        pass

    def teardown(self):
        pass

    def path_elements(self):
        self.path = cleanPath(self.environ['PATH_INFO'])
        return []

    def before_traverse(self, ob, name):
        pass

    def traverse(self, ob, name):
        pass

    def before_invoke(self, published):
        pass

    def invoke(self, published):
        found = []
        fs = self.fs
        f = None
        while self.path:
            name = self.path.pop(0)
            if fs.isfile(name):
                if self.path:
                    raise httpexceptions.HTTPNotFound(name)
                else:
                    f = File(fs.translate(name))
            elif fs.isdir(name):
                ok = fs.cwd(name)
                if not ok:
                    raise httpexceptions.HTTPForbidden(name)
                if not self.path:
                    if fs.isfile(os.path.join(name, self.default_viewname)):
                        f = File(fs.translate(self.default_viewname))
        if f is None:
            raise RuntimeError(self.path)
        ext = os.path.splitext(f.filename)[1]
        view = getAdapter(f, IView, name=ext)
        return view()

    def map_result(self, result):
        result = result.encode(self.encoding)
        return ('200 OK', [], result)

class File(object):
    implements(IFile)
    def __init__(self, filename):
        self.filename = filename

_context = None

def initialize(**config):
    from zope.configuration import xmlconfig
    here = os.path.dirname(os.path.abspath(__file__))
    import zope.component
    global _context
    _context = xmlconfig.file('meta.zcml', package=zope.component)

    zcml = os.path.join(here, 'configure.zcml')
    import repoze.virginia
    xmlconfig.file(zcml, package=repoze.virginia, context=_context,
                   execute=True)

def get_root(helper):
    return None


