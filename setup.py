__version__ = '0.1'

import os
from setuptools import setup, find_packages

setup(name='repoze.virginia',
      version=__version__,
      description='An obob plugin that publishes filesystem content',
      long_description='',
      classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Zope Public License",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware",
        "Framework :: Zope3",
        ],
      keywords='web application server wsgi zope',
      author="Agendaless Consulting",
      author_email="reopze-dev@lists.repoze.org",
      dependency_links=['http://dist.repoze.org'],
      url="http://www.repoze.org",
      license="ZPL 2.0",
      packages=find_packages(),
      include_package_data=True,
      namespace_packages=['repoze'],
      zip_safe=False,
      tests_require = [
               'zopelib >= 2.10.4.2',
               ],
      install_requires=[
               'PasteScript >= 1.3.6',
               'WSGIUtils >= 0.7',
               'zopelib >= 2.10.4.2',
               ],
      test_suite="repoze.virginia.tests",
      )

