#  Drakkar-Software OctoBot-Commons
#  Copyright (c) Drakkar-Software, All rights reserved.
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3.0 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library.
# from distutils.extension import Extension
import os

from setuptools import dist
dist.Distribution().fetch_build_eggs(['Cython>=0.29.26', 'numpy==1.22.0'])

import numpy as np

try:
    from Cython.Distutils import build_ext
    from Cython.Build import cythonize
except ImportError:
    # create closure for deferred import
    def cythonize(*args, **kwargs):
        from Cython.Build import cythonize
        return cythonize(*args, **kwargs)

    def build_ext(*args, **kwargs):
        from Cython.Distutils import build_ext
        return build_ext(*args, **kwargs)

from setuptools import find_packages
from setuptools import setup, Extension

from octobot_commons import PROJECT_NAME, VERSION

PACKAGES = find_packages(exclude=["tests"])

packages_list = [
    "octobot_commons.async_job",
    "octobot_commons.tree.base_tree",
    "octobot_commons.tree.event_tree",
    "octobot_commons.evaluators_util",
    "octobot_commons.data_util",
    "octobot_commons.list_util",
    "octobot_commons.pretty_printer",
    "octobot_commons.symbols.symbol",
    "octobot_commons.symbols.symbol_util",
    "octobot_commons.time_frame_manager",
    "octobot_commons.singleton.singleton_class",
    "octobot_commons.logging.logging_util",
    "octobot_commons.tentacles_management.class_inspector",
    "octobot_commons.databases.relational_databases.sqlite.cursor_pool",
    "octobot_commons.databases.relational_databases.sqlite.cursor_wrapper",
    "octobot_commons.databases.relational_databases.sqlite.sqlite_database",
    "octobot_commons.databases.run_databases.run_databases_provider",
]

ext_modules = [
    Extension(package, [f"{package.replace('.', '/')}.py"], include_dirs=[np.get_include()])
    for package in packages_list]

# long description from README file
with open('README.md', encoding='utf-8') as f:
    DESCRIPTION = f.read()

REQUIRED = open('requirements.txt').readlines()
REQUIRES_PYTHON = '>=3.8'
CYTHON_DEBUG = False if not os.getenv('CYTHON_DEBUG') else os.getenv('CYTHON_DEBUG')

setup(
    name=PROJECT_NAME,
    version=VERSION,
    url='https://github.com/Drakkar-Software/OctoBot-Commons',
    license='LGPL-3.0',
    author='Drakkar-Software',
    author_email='drakkar-software@protonmail.com',
    description='OctoBot project common modules',
    packages=PACKAGES,
    include_package_data=True,
    long_description=DESCRIPTION,
    include_dirs=[np.get_include()],
    cmdclass={'build_ext': build_ext},
    tests_require=["pytest"],
    test_suite="tests",
    zip_safe=False,
    data_files=[],
    setup_requires=REQUIRED if not CYTHON_DEBUG else [],
    install_requires=REQUIRED,
    ext_modules=cythonize(ext_modules, gdb_debug=CYTHON_DEBUG),
    python_requires=REQUIRES_PYTHON,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
