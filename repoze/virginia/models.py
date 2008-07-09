import os

from zope.interface import implements

from repoze.virginia.interfaces import IFile
from repoze.virginia.interfaces import IDirectory

class Directory(object):
    implements(IDirectory)
    def __init__(self, filesystem, path):
        self.filesystem = filesystem
        self.path = path

    def __getitem__(self, name):
        self.filesystem.cwd(self.path)
        nextpath = os.path.join(self.path, name)
        if self.filesystem.isdir(name):
            return Directory(self.filesystem, nextpath)
        elif self.filesystem.isfile(name):
            return File(self.filesystem, nextpath)
        else:
            raise KeyError(name)

class File(object):
    implements(IFile)
    def __init__(self, filesystem, path):
        self.filesystem = filesystem
        self.path = path

    def _source(self):
        dir, name = os.path.split(self.path)
        self.filesystem.cwd(dir)
        return self.filesystem.open(name, 'r').read()
        
    source = property(_source)
