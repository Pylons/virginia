import unittest

class FilesystemTests(unittest.TestCase):
    def _getTargetClass(self):
        from virginia.models import Filesystem
        return Filesystem

    def _makeOne(self, *arg, **kw):
        klass = self._getTargetClass()
        return klass(*arg, **kw)

    def test_open_allows(self):
        import os
        import tempfile
        f = tempfile.NamedTemporaryFile()
        f.write('hello')
        f.flush()
        fs = self._makeOne(os.path.abspath(os.path.dirname(f.name)))
        self.assertEqual(fs.open(f.name).read(), 'hello')
        f.close()

    def test_open_denies(self):
        import os
        import tempfile
        tempdir = tempfile.tempdir
        fs = self._makeOne(tempdir)
        here = os.path.abspath(__file__)
        self.assertEqual(fs.open(here), None)

    def test_read(self):
        import os
        import tempfile
        f = tempfile.NamedTemporaryFile()
        f.write('hello')
        f.flush()
        fs = self._makeOne(os.path.dirname(f.name))
        self.assertEqual(fs.open(f.name).read(), 'hello')
        f.close()

class DirectoryTests(unittest.TestCase):
    def _getTargetClass(self):
        from virginia.models import Directory
        return Directory

    def _makeOne(self, *arg, **kw):
        klass = self._getTargetClass()
        return klass(*arg, **kw)
    
    def test_getitem_islink_tofile_samedir(self):
        links = {'/foo/bar':'/foo/baz'}
        files= ['/foo/baz']
        fs = DummyFilesystem(links, files)
        directory = self._makeOne(fs, '/foo')
        result = directory['bar']
        from virginia.models import File
        self.failUnless(isinstance(result, File))
        self.assertEqual(result.path, '/foo/baz')

    def test_getitem_islink_tofile_diffdir(self):
        links = {'/foo/bar':'/buz/baz'}
        fs = DummyFilesystem(links)
        directory = self._makeOne(fs, '/foo')
        self.assertRaises(KeyError, directory.__getitem__, 'bar')

    def test_getitem_isdir(self):
        fs = DummyFilesystem(dirs=['/foo/dir'])
        directory = self._makeOne(fs, '/foo')
        result = directory['dir']
        from virginia.models import Directory
        self.failUnless(isinstance(result, Directory))
        self.assertEqual(result.path, '/foo/dir')

    def test_getitem_isfile(self):
        fs = DummyFilesystem(files=['/foo/file'])
        directory = self._makeOne(fs, '/foo')
        result = directory['file']
        from virginia.models import File
        self.failUnless(isinstance(result, File))
        self.assertEqual(result.path, '/foo/file')

class FileTests(unittest.TestCase):
    def _getTargetClass(self):
        from virginia.models import File
        return File

    def _makeOne(self, *arg, **kw):
        klass = self._getTargetClass()
        return klass(*arg, **kw)

    def test_source(self):
        import tempfile
        named = tempfile.NamedTemporaryFile()
        named.write('silly')
        named.flush()
        name = named.name
        fs = DummyFilesystem()
        f = self._makeOne(fs, name)
        self.assertEqual(f.source, 'silly')
        named.close()
    
class DummyFilesystem:
    import os
    dirname = staticmethod(os.path.dirname)
    join = staticmethod(os.path.join)
    def __init__(self, links=None, files=(), dirs=()):
        if links is None:
            links = {}
        self.links = links
        self.files = files
        self.dirs = dirs

    def islink(self, path):
        return path in self.links.keys()

    def isdir(self, path):
        return path in self.dirs

    def isfile(self, path):
        return path in self.files
    
    def realpath(self, path):
        return self.links[path]

    def read(self, path):
        return open(path, 'rb').read()
    
