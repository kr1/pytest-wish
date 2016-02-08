# -*- coding: utf-8 -*-
#
# Copyright (c) 2015-2016 Alessandro Amici
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

# python 2 support via python-future
from __future__ import absolute_import, unicode_literals
from builtins import dict, zip

import argparse
import collections
import logging
import sys

import pytest

from . import collect
from . import utils


def pytest_addoption(parser):
    group = parser.getgroup('wish')
    group.addoption(
        '--wish-from-stdlib', action='store_true',
        help="Collects objects form the Python standard library.")
    group.addoption(
        '--wish-from-installed', action='store_true',
        help="Collects objects form all installed packages.")
    group.addoption(
        '--wish-from-all', action='store_true',
        help="Collects objects form the Python standard library and all installed packages.")
    group.addoption(
        '--wish-from-specs', default=[], nargs='+',
        help="Collects objects from installed packages. Space separated list of ``pip`` specs.")
    group.addoption(
        '--wish-from-modules', default=[], nargs='+',
        help="Collects objects from installed modules. Space separated list of module names.")
    group.addoption(
        '--wish-includes', nargs='+',
        help="Space separated list of regexs matching full object names to include, "
             "defaults to include all objects collected via ``--wish-from-*``.")
    group.addoption(
        '--wish-excludes', default=[collect.INTERNAL_USE_PATTERN], nargs='+',
        help="Space separated list of regexs matching full object names to exclude, "
             "defaults to match 'internal use' names %r" % collect.INTERNAL_USE_PATTERN)
    group.addoption(
        '--wish-objects-from', type=argparse.FileType('r'),
        help="File name of full object names to include.")
    group.addoption(
        '--wish-predicate', default='builtins:callable',
        help="Full name of the predicate passed to ``inspect.getmembers``, "
             "defaults to ``builtins.callable``.")
    group.addoption('--wish-timeout', default=1, help="Test timeout.")
    group.addoption('--wish-fail', action='store_true', help="Show wish failures.")


def wish_ensuresession(config):
    if hasattr(config, '_wish_index_items'):
        return

    # take over collect logging
    collect.logger.propagate = False
    collect.logger.setLevel(logging.DEBUG)  # FIXME: loglevel should be configurable
    collect.logger.addHandler(utils.EmitHandler(config._warn))

    # build the object index
    distributions = collections.OrderedDict()

    if config.getoption('wish_from_stdlib') or config.getoption('wish_from_all'):
        distributions.update(collect.collect_stdlib_distributions())

    if config.getoption('wish_from_installed') or config.getoption('wish_from_all'):
        distributions.update(collect.collect_installed_distributions())

    distributions.update(collect.collect_distributions(config.getoption('wish_from_specs')))

    if config.getoption('wish_from_modules'):
        distributions['unknown distribution'] = config.getoption('wish_from_modules')

    imported_module_names = collect.import_distributions(distributions.items())

    wish_includes = config.getoption('wish_includes') or imported_module_names
    wish_excludes = config.getoption('wish_excludes')
    wish_predicate = config.getoption('wish_predicate')

    config._warn('%r' % locals())

    # NOTE: 'copy' is needed here because indexing may unexpectedly trigger a module load
    modules = sys.modules.copy()
    object_index = dict(
        collect.generate_objects_from_modules(modules, wish_includes, wish_excludes,
                                              wish_predicate)
    )

    wish_objects_from = config.getoption('wish_objects_from')
    if wish_objects_from is not None:
        object_index.update(collect.generate_objects_from_names(wish_objects_from))

    # store options
    config._wish_index_items = list(zip(*sorted(object_index.items()))) or [(), ()]


def pytest_generate_tests(metafunc):
    if 'wish' not in metafunc.fixturenames:
        return

    config = metafunc.config
    wish_ensuresession(config)

    ids, params = config._wish_index_items
    metafunc.parametrize('wish', params, ids=ids, scope='module')
    metafunc.function = pytest.mark.timeout(config.getoption('wish_timeout'))(metafunc.function)
    if not config.getoption('wish_fail'):
        metafunc.function = pytest.mark.xfail(metafunc.function)


def pytest_terminal_summary(terminalreporter):
    if not hasattr(terminalreporter.config, '_wish_index_items'):
        return

    hit_state = 'passed' if terminalreporter.config.getoption('wish_fail') else 'xpassed'
    hits = terminalreporter.getreports(hit_state)
    terminalreporter.write_sep('=', '%d hit' % len(hits), bold=True)
    terminalreporter.write_line('')
    for report in hits:
        terminalreporter.write(report.nodeid)
        terminalreporter.write_line(' HIT', bold=True, green=True)
    terminalreporter.write_line('')
