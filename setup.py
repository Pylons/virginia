##############################################################################
#
# Copyright (c) 2010 Agendaless Consulting and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the BSD-like license at
# http://www.repoze.org/LICENSE.txt.  A copy of the license should accompany
# this distribution.  THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL
# EXPRESS OR IMPLIED WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND
# FITNESS FOR A PARTICULAR PURPOSE
#
##############################################################################

__version__ = "0.0"

import os
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, "README.md")).read()
CHANGELOG = open(os.path.join(here, "CHANGELOG.md")).read()

requires = [
    "pyramid<2",
    "pyramid_debugtoolbar",
    "zope.structuredtext>=4.2.0",
    "waitress",
]

py_version = sys.version_info[:3]
if py_version < (2, 7, 0):
    raise RuntimeError("This application requires Python 2.7")
elif (py_version >= (3, 0, 0) and py_version < (3, 4, 0)) or py_version >= (
    3,
    13,
    0,
):
    raise RuntimeError("This application requires Python 3.4 - 3.12")
elif py_version < (3, 6, 0):
    requires.append("PasteDeploy<3")

setup(
    name="virginia",
    version=__version__,
    description="Serve slightly dynamic filesystem content via Pyramid",
    long_description=README + "\n\nCHANGES\n\n" + CHANGELOG,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    keywords="file server pyramid pylons",
    author="Agendaless Consulting",
    author_email="pylons-devel@googlegroups.com",
    url="http://docs.pylonshq.com",
    license="BSD-derived (http://www.repoze.org/LICENSE.txt)",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    tests_require=requires,
    install_requires=requires,
    test_suite="virginia.tests",
    entry_points="""\
      [paste.app_factory]
      main = virginia:main
      """,
)
