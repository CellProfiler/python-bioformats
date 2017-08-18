# Python-bioformats is distributed under the GNU General Public
# License, but this file is licensed under the more permissive BSD
# license.  See the accompanying file LICENSE for details.
#
# Copyright (c) 2009-2014 Broad Institute
# All rights reserved.

from __future__ import absolute_import, unicode_literals

import numpy

import bioformats.formatreader
import bioformats.formatwriter


def test_write_monochrome_8_bit_tif(tmpdir):
    r = numpy.random.RandomState()
    r.seed(101)
    img = r.randint(0, 256, (11, 33)).astype(numpy.uint8)
    path = str(tmpdir.join("monochrome_8_bit.tif"))
    bioformats.formatwriter.write_image(path, img, "uint8")
    result = bioformats.formatreader.load_using_bioformats(path, rescale=False)
    numpy.testing.assert_array_equal(img, result)


def test_write_monochrome_16_bit_tif(tmpdir):
    r = numpy.random.RandomState()
    r.seed(102)
    img = r.randint(0, 4096, size=(21, 24))
    path = str(tmpdir.join("monochrome_16_bit.tif"))
    bioformats.formatwriter.write_image(path, img, "uint16")
    result = bioformats.formatreader.load_using_bioformats(path, rescale=False)
    numpy.testing.assert_array_equal(img, result)


def test_write_color_tif(tmpdir):
    r = numpy.random.RandomState()
    r.seed(103)
    img = r.randint(0, 256, (9, 11, 3))
    path = str(tmpdir.join("color.tif"))
    bioformats.formatwriter.write_image(path, img, "uint8")
    result = bioformats.formatreader.load_using_bioformats(path, rescale=False)
    numpy.testing.assert_array_equal(img, result)


def test_write_movie(tmpdir):
    r = numpy.random.RandomState()
    r.seed(103)
    img = r.randint(0, 256, (7, 23, 11))
    path = str(tmpdir.join("movie.tif"))
    for i in range(img.shape[0]):
        bioformats.formatwriter.write_image(
            path, img[i], "uint8", t=i, size_t=img.shape[0]
        )
    for i in range(img.shape[0]):
        result = bioformats.formatreader.load_using_bioformats(path, t=i, rescale=False)
        numpy.testing.assert_array_equal(img[i], result)
