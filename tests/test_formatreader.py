# Python-bioformats is distributed under the GNU General Public
# License, but this file is licensed under the more permissive BSD
# license.  See the accompanying file LICENSE for details.
#
# Copyright (c) 2009-2014 Broad Institute
# All rights reserved.

'''test_formatreader.py - test the Bioformats format reader wrapper

'''

from __future__ import absolute_import, unicode_literals

import os
import re
import unittest

import future.moves.urllib.request
import javabridge
import numpy

import bioformats
import bioformats.formatreader


def test_make_format_tools_class():
    FormatTools = bioformats.formatreader.make_format_tools_class()
    assert FormatTools.CAN_GROUP == 1
    assert FormatTools.CANNOT_GROUP == 2
    assert FormatTools.DOUBLE == 7
    assert FormatTools.FLOAT == 6
    assert FormatTools.INT16 == 2
    assert FormatTools.INT8 == 0
    assert FormatTools.MUST_GROUP == 0
    assert FormatTools.UINT16 == 3
    assert FormatTools.UINT32 == 5
    assert FormatTools.UINT8 == 1


def test_make_image_reader():
    path = os.path.join(os.path.dirname(__file__), 'resources', 'Channel1-01-A-01.tif')
    ImageReader = bioformats.formatreader.make_image_reader_class()
    FormatTools = bioformats.formatreader.make_format_tools_class()
    reader = ImageReader()
    reader.setId(path)
    assert reader.getDimensionOrder() == "XYCZT"
    metadata = javabridge.jdictionary_to_string_dictionary(reader.getMetadata())
    assert int(metadata["ImageWidth"]) == reader.getSizeX()
    assert int(metadata["ImageLength"]) == reader.getSizeY()
    assert reader.getImageCount() == 1
    assert reader.getSizeC() == 1
    assert reader.getSizeT() == 1
    assert reader.getSizeZ() == 1
    assert reader.getPixelType() == FormatTools.UINT8
    assert reader.getRGBChannelCount() == 1


def test_read_tif():
    path = os.path.join(os.path.dirname(__file__), 'resources', 'Channel1-01-A-01.tif')
    ImageReader = bioformats.formatreader.make_image_reader_class()
    FormatTools = bioformats.formatreader.make_format_tools_class()
    reader = ImageReader()
    reader.setId(path)
    data = reader.openBytes(0)
    data.shape = (reader.getSizeY(), reader.getSizeX())
    #
    # Data as read by cellprofiler.modules.loadimages.load_using_PIL
    #
    expected_0_10_0_10 = numpy.array(
        [[ 0,  7,  7,  6,  5,  8,  4,  2,  1,  2],
         [ 0,  8,  8,  7,  6, 10,  4,  2,  2,  2],
         [ 0,  9,  9,  7,  8,  8,  2,  1,  3,  2],
         [ 0, 10,  9,  8, 10,  6,  2,  2,  3,  2],
         [ 0, 10, 10, 10,  9,  4,  2,  2,  2,  2],
         [ 0,  9,  9, 10,  8,  3,  2,  4,  2,  2],
         [ 0,  9,  9, 10,  8,  2,  2,  4,  3,  2],
         [ 0,  9,  8,  9,  7,  4,  2,  2,  2,  2],
         [ 0, 10, 11,  9,  9,  4,  2,  2,  2,  2],
         [ 0, 12, 13, 12,  9,  4,  2,  2,  2,  2]], dtype=numpy.uint8)
    expected_n10_n10 = numpy.array(
        [[2, 1, 1, 1, 2, 2, 1, 2, 1, 2],
         [1, 2, 2, 2, 2, 1, 1, 1, 2, 1],
         [1, 1, 1, 2, 1, 2, 2, 2, 2, 1],
         [2, 2, 2, 2, 3, 2, 2, 2, 2, 1],
         [1, 2, 2, 1, 1, 1, 1, 1, 2, 2],
         [2, 1, 2, 2, 2, 1, 1, 2, 2, 2],
         [2, 2, 3, 2, 2, 1, 2, 2, 2, 1],
         [3, 3, 1, 2, 2, 2, 2, 3, 2, 2],
         [3, 2, 2, 2, 2, 2, 2, 2, 3, 3],
         [5, 2, 3, 3, 2, 2, 2, 3, 2, 2]], dtype=numpy.uint8)
    assert numpy.all(expected_0_10_0_10 == data[:10, :10])
    assert numpy.all(expected_n10_n10 == data[-10:, -10:])


def test_load_using_bioformats():
    path = os.path.join(os.path.dirname(__file__), 'resources', 'Channel1-01-A-01.tif')
    data = bioformats.formatreader.load_using_bioformats(path, rescale=False)
    expected_0_10_0_10 = numpy.array(
        [[ 0,  7,  7,  6,  5,  8,  4,  2,  1,  2],
         [ 0,  8,  8,  7,  6, 10,  4,  2,  2,  2],
         [ 0,  9,  9,  7,  8,  8,  2,  1,  3,  2],
         [ 0, 10,  9,  8, 10,  6,  2,  2,  3,  2],
         [ 0, 10, 10, 10,  9,  4,  2,  2,  2,  2],
         [ 0,  9,  9, 10,  8,  3,  2,  4,  2,  2],
         [ 0,  9,  9, 10,  8,  2,  2,  4,  3,  2],
         [ 0,  9,  8,  9,  7,  4,  2,  2,  2,  2],
         [ 0, 10, 11,  9,  9,  4,  2,  2,  2,  2],
         [ 0, 12, 13, 12,  9,  4,  2,  2,  2,  2]], dtype=numpy.uint8)
    expected_n10_n10 = numpy.array(
        [[2, 1, 1, 1, 2, 2, 1, 2, 1, 2],
         [1, 2, 2, 2, 2, 1, 1, 1, 2, 1],
         [1, 1, 1, 2, 1, 2, 2, 2, 2, 1],
         [2, 2, 2, 2, 3, 2, 2, 2, 2, 1],
         [1, 2, 2, 1, 1, 1, 1, 1, 2, 2],
         [2, 1, 2, 2, 2, 1, 1, 2, 2, 2],
         [2, 2, 3, 2, 2, 1, 2, 2, 2, 1],
         [3, 3, 1, 2, 2, 2, 2, 3, 2, 2],
         [3, 2, 2, 2, 2, 2, 2, 2, 3, 3],
         [5, 2, 3, 3, 2, 2, 2, 3, 2, 2]], dtype=numpy.uint8)
    assert numpy.all(expected_0_10_0_10 == data[:10, :10])
    assert numpy.all(expected_n10_n10 == data[-10:, -10:])


def test_read_subimage_tif():
    path = os.path.join(os.path.dirname(__file__), 'resources', 'Channel1-01-A-01.tif')
    with bioformats.ImageReader(path) as f:
        data_0_10_0_10 = f.read(XYWH=(0, 0, 10, 10), rescale=False)

    #
    # Data as read by cellprofiler.modules.loadimages.load_using_PIL
    #
    expected_0_10_0_10 = numpy.array(
        [[ 0,  7,  7,  6,  5,  8,  4,  2,  1,  2],
         [ 0,  8,  8,  7,  6, 10,  4,  2,  2,  2],
         [ 0,  9,  9,  7,  8,  8,  2,  1,  3,  2],
         [ 0, 10,  9,  8, 10,  6,  2,  2,  3,  2],
         [ 0, 10, 10, 10,  9,  4,  2,  2,  2,  2],
         [ 0,  9,  9, 10,  8,  3,  2,  4,  2,  2],
         [ 0,  9,  9, 10,  8,  2,  2,  4,  3,  2],
         [ 0,  9,  8,  9,  7,  4,  2,  2,  2,  2],
         [ 0, 10, 11,  9,  9,  4,  2,  2,  2,  2],
         [ 0, 12, 13, 12,  9,  4,  2,  2,  2,  2]], dtype=numpy.uint8)
    expected_n10_n10 = numpy.array(
        [[2, 1, 1, 1, 2, 2, 1, 2, 1, 2],
         [1, 2, 2, 2, 2, 1, 1, 1, 2, 1],
         [1, 1, 1, 2, 1, 2, 2, 2, 2, 1],
         [2, 2, 2, 2, 3, 2, 2, 2, 2, 1],
         [1, 2, 2, 1, 1, 1, 1, 1, 2, 2],
         [2, 1, 2, 2, 2, 1, 1, 2, 2, 2],
         [2, 2, 3, 2, 2, 1, 2, 2, 2, 1],
         [3, 3, 1, 2, 2, 2, 2, 3, 2, 2],
         [3, 2, 2, 2, 2, 2, 2, 2, 3, 3],
         [5, 2, 3, 3, 2, 2, 2, 3, 2, 2]], dtype=numpy.uint8)
    assert numpy.all(expected_0_10_0_10 == data_0_10_0_10)
    # assert np.all(expected_n10_n10 == data[-10:,-10:])


def test_load_using_bioformats_url():
    url = "https://github.com/CellProfiler/python-bioformats/raw/1.0.5/bioformats/tests/Channel1-01-A-01.tif"
    try:
        fd = future.moves.urllib.request.urlopen(url)
        if fd.code < 200 or fd.code >= 300:
            raise OSError("Http error %d" % fd.code)
    except OSError as e:
        def bad_url(e=e):
            raise e
        unittest.expectedFailure(bad_url)()

    data = bioformats.formatreader.load_using_bioformats_url(url, rescale=False)
    assert data.shape == (640, 640)


def test_read_omexml_metadata():
    path = os.path.join(os.path.dirname(__file__), 'resources', 'Channel1-01-A-01.tif')
    xml = bioformats.formatreader.get_omexml_metadata(path)
    pattern = r'<\s*Image\s+ID\s*=\s*"Image:0"\s+Name\s*=\s*"Channel1-01-A-01.tif"\s*>'
    assert re.search(pattern, xml)
