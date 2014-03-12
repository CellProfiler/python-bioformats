# Python-bioformats is distributed under the GNU General Public
# License, but this file is licensed under the more permissive BSD
# license.  See the accompanying file LICENSE for details.
# 
# Copyright (c) 2009-2014 Broad Institute
# All rights reserved.

import os
import unittest

import javabridge
import bioformats

import bioformats.formatreader as formatreader
import bioformats.metadatatools as metadatatools
from bioformats import load_image
from bioformats import log4j

class TestLoadUsingBioformats(unittest.TestCase):

    def setUp(self):
        javabridge.attach()
        log4j.basic_config()
        
    def tearDown(self):
        javabridge.detach()

    def test_load_using_bioformats(self):
        path = os.path.join(os.path.dirname(__file__), 'Channel1-01-A-01.tif')
        image, scale = load_image(path, rescale=False,
                                  wants_max_intensity=True)
        print image.shape

