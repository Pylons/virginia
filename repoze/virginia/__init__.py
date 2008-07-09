# publish a filesystem tree

def make_app(global_config, root=None):
    if root is None:
        raise ValueError('repoze.virginia requires a root')
    import os
    from zope.interface import directlyProvides
    from repoze.bfg.router import make_app
    from repoze.virginia.interfaces import IFilesystem
    from repoze.virginia.models import Directory
    from repoze.virginia.filesys import os_filesystem
    fs = os_filesystem(os.path.abspath(os.path.normpath(root)))
    directlyProvides(fs, IFilesystem)
    def get_root(environ):
        return Directory(fs, root)
    import repoze.virginia
    return make_app(get_root, repoze.virginia)

