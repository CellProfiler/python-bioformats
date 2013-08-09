#!/usr/bin/env python

import os
import javabridge
import bioformats
from bioformats import log4j

class_path = os.pathsep.join(bioformats.JARS + javabridge.JARS)
javabridge.start_vm(['-Djava.class.path=' + class_path], 
                    run_headless=True)
try:
    log4j.basic_config()
    image_path = os.path.join(os.path.dirname(bioformats.__file__), 'tests', 
                              'Channel1-01-A-01.tif')
    image, scale = bioformats.load_using_bioformats(image_path, rescale=False,
                                                    wants_max_intensity=True)
    print image.shape
finally:
    javabridge.kill_vm()
