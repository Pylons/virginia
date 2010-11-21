import os

from zope.interface import implements

from virginia.interfaces import IFile
from virginia.interfaces import IDirectory
from virginia.interfaces import IFilesystem

class Filesystem(object):
    implements(IFilesystem)

    def __init__(self, root_path):
        self.root_path = os.path.abspath(os.path.normpath(root_path))

    join = staticmethod(os.path.join)
    dirname = staticmethod(os.path.dirname)
    realpath = staticmethod(os.path.realpath)
    islink = staticmethod(os.path.islink)
    isfile = staticmethod(os.path.isfile)
    isdir = staticmethod(os.path.isdir)

    def open(self, path):
        if path.startswith(self.root_path):
            return open(path, 'rb')

    def read(self, path):
        return self.open(path).read()

class File(object):
    implements(IFile)

    def __init__(self, filesystem, path):
        self.filesystem = filesystem
        self.path = os.path.abspath(os.path.normpath(path))

    def _source(self):
        return self.filesystem.read(self.path)

    source = property(_source)

class Directory(object):
    file_class = File

    implements(IDirectory)
    def __init__(self, filesystem, path):
        self.filesystem = filesystem
        self.path = os.path.abspath(os.path.normpath(path))

    def __getitem__(self, name):
        nextpath = self.filesystem.join(self.path, name)
        if self.filesystem.islink(nextpath):
            realpath = self.filesystem.realpath(nextpath)
            if  ( realpath.startswith(self.path) and
                  self.filesystem.isfile(realpath) ):
                realdir = self.filesystem.dirname(realpath)
                if len(self.path.split(os.sep)) == len(realdir.split(os.sep)):
                    # if this symlink to a file is in the same
                    # directory as the original file, treat it as a
                    # primitive alias; use the link target as the
                    # filename so we get the right renderer (eg. stx
                    # vs html).
                    return File(self.filesystem, realpath)
                else:
                    raise KeyError(name)
            else:
                raise KeyError(name)
        elif self.filesystem.isdir(nextpath):
            return self.__class__(self.filesystem, nextpath)
        elif self.filesystem.isfile(nextpath):
            return self.file_class(self.filesystem, nextpath)
        else:
            raise KeyError(name)

