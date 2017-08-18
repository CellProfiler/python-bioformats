# Python-bioformats is distributed under the GNU General Public
# License, but this file is licensed under the more permissive BSD
# license.  See the accompanying file LICENSE for details.
#
# Copyright (c) 2009-2014 Broad Institute
# All rights reserved.

from __future__ import absolute_import, print_function, unicode_literals

import os

import future.moves.urllib.request
import pytest

import bioformats


def test_load_using_bioformats():
    path = os.path.join(os.path.dirname(__file__), 'resources', 'Channel1-01-A-01.tif')
    image, scale = bioformats.load_image(path, rescale=False, wants_max_intensity=True)
    print(image.shape)


def test_file_not_found():
    # Regression test of issue #6
    path = os.path.join(os.path.dirname(__file__), 'resources', 'Channel5-01-A-01.tif')
    with pytest.raises(IOError):
        bioformats.load_image(path)


def test_open_file():
    path = os.path.join(os.path.dirname(__file__), 'resources', 'Channel1-01-A-01.tif')
    url = "file:" + future.moves.urllib.request.pathname2url(path)
    image, scale = bioformats.load_image_url(url, rescale=False, wants_max_intensity=True)
    assert image.shape[0] == 640


def test_open_http():
    url = "https://github.com/CellProfiler/python-bioformats/raw/39f2aa8360324b4129284d4f647d4f7ee7797518" \
          "/tests/resources/Channel1-01-A-01.tif"
    image, scale = bioformats.load_image_url(url, rescale=False, wants_max_intensity=True)
    assert image.shape[0] == 640


def test_unicode_url():
    #
    # Regression test of issue #17: ensure that this does not
    # raise an exception when converting URL to string
    #
    path = os.path.join(os.path.dirname(__file__), 'resources', 'Channel1-01-A-01.tif')
    url = "file:" + future.moves.urllib.request.pathname2url(path)
    image, scale = bioformats.load_image_url(url, rescale=False, wants_max_intensity=True)
    assert image.shape[0] == 640


