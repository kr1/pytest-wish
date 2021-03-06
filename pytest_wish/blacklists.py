# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Alessandro Amici
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
from __future__ import unicode_literals


MODULE_BLACKLIST = {
    # crash
    'icopen',
    'ntpath',
    'tests?$',
    'tests?\.',
    'xml.etree.ElementTree',

    # hangs
    'itertools',

    # dangerous
    'subprocess',

    # annoying
    'pydoc',
    'tkinter',
    'turtle'
}

OBJECT_BLACKLIST = {
    # pytest internals
    '_pytest.runner:exit',
    '_pytest.runner:skip',
    '_pytest.skipping:xfail',

    # unconditional exit
    'faulthandler:_sigsegv',
    'posix:abort',
    'posix:_exit',
    'posix:fork',
    'posix:forkpty',
    'pty:fork',
    '_signal:default_int_handler',
    'atexit.register',

    # low level crashes
    'numpy.fft.fftpack_lite:cffti',
    'numpy.fft.fftpack_lite:rffti',
    'appnope._nope:beginActivityWithOptions',
    'ctypes:string_at',
    'ctypes:wstring_at',
    'gc:_dump_rpy_heap',
    'gc:dump_rpy_heap',
    'matplotlib._image:Image',
    'getpass:getpass',
    'getpass:unix_getpass',
    'ensurepip:_run_pip',

    # uninterruptable hang
    'compiler.ast:AugAssign',
    'itertools:cycle',
    'itertools:permutations',
    'itertools:repeat',
    'pydoc:apropos',

    # dangerous
    'os.mkdir',
    'os.command',
    'pip.utils:rmtree',
    'platform:popen',
    'posix:popen',
    'turtle.write_docstringdict',
}
