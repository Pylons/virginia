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
        if self.filesystem.islink(name):
            realpath = os.path.realpath(os.path.join(self.path, name))
            if realpath.startswith(self.path):
                realdir = os.path.dirname(realpath)
                if len(self.path.split(os.sep)) == len(realdir.split(os.sep)):
                    # if this symlink is in the same directory as the
                    # original, treat it as a primitive alias; use the
                    # link target as the filename so we get the right
                    # renderer (eg. stx vs html).
                    ignored, truename = os.path.split(realpath)
                    return File(self.filesystem, truename)
        elif self.filesystem.isdir(name):
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
