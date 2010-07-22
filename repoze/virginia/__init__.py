# publish a filesystem tree

def make_app(global_config, root=None):
    if root is None:
        raise ValueError('repoze.virginia requires a root')
    import os
    from repoze.virginia.models import Directory
    from repoze.virginia.models import Filesystem
    fs = Filesystem(os.path.abspath(os.path.normpath(root)))
    def get_root(environ):
        return Directory(fs, root)
    from repoze.bfg.configuration import Configurator
    config = Configurator(root_factory=get_root)
    config.begin()
    config.load_zcml('repoze.virginia:configure.zcml')
    config.end()
    return config.make_wsgi_app()

