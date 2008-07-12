# publish a filesystem tree

def make_app(global_config, root=None):
    if root is None:
        raise ValueError('repoze.virginia requires a root')
    import os
    from repoze.bfg import make_app
    from repoze.virginia.models import Directory
    from repoze.virginia.models import Filesystem
    fs = Filesystem(os.path.abspath(os.path.normpath(root)))
    def get_root(environ):
        return Directory(fs, root)
    import repoze.virginia
    return make_app(get_root, repoze.virginia)

