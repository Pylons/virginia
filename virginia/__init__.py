import os

from pyramid.configuration import Configurator

from virginia.models import Directory
from virginia.models import Filesystem

def main(global_config, **settings):
    root = settings.pop('root', None)
    if root is None:
        raise ValueError('virginia requires a root')
    fs = Filesystem(os.path.abspath(os.path.normpath(root)))
    def get_root(environ):
        return Directory(fs, root)
    config = Configurator(root_factory=get_root, settings=settings)
    config.load_zcml('virginia:configure.zcml')
    return config.make_wsgi_app()

