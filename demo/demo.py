#!/usr/bin/env python

from __future__ import absolute_import, print_function, unicode_literals

import os
import javabridge
import bioformats
from bioformats import log4j
import sys

javabridge.start_vm(class_path=bioformats.JARS,
                    run_headless=True)
try:
    log4j.basic_config()
    if len(sys.argv) < 2:
        image_path = os.path.join(
            os.path.dirname(bioformats.__file__),
            '..',
            'tests',
            'resources',
            'Channel1-01-A-01.tif'
        )
    else:
        image_path = sys.argv[1]
    image, scale = bioformats.load_image(image_path, rescale=False,
                                         wants_max_intensity=True)
    try:
        import pylab

        pylab.imshow(image)
        pylab.gca().set_title(image_path)
        pylab.show()
    except:
        print(image.shape)
finally:
    javabridge.kill_vm()
