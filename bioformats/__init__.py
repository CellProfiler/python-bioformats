'''Bioformats package - wrapper for loci.bioformats java code

CellProfiler is distributed under the GNU General Public License,
but this file is licensed under the more permissive BSD license.
See the accompanying file LICENSE for details.

Copyright (c) 2003-2009 Massachusetts Institute of Technology
Copyright (c) 2009-2013 Broad Institute
All rights reserved.

Please see the AUTHORS file for credits.

Website: http://www.cellprofiler.org
'''
__version__ = "$Revision$"

import os.path
import javabridge
import formatreader as _formatreader
import formatwriter as _formatwriter

_jars_dir = os.path.join(os.path.dirname(__file__), 'jars')
JARS = javabridge.JARS + [os.path.realpath(os.path.join(_jars_dir, name + '.jar'))
                          for name in ['loci_tools']]

# See http://www.loci.wisc.edu/software/bio-formats
READABLE_FORMATS = ('al3d', 'am', 'amiramesh', 'apl', 'arf', 'avi', 'bmp', 
                    'c01', 'cfg', 'cxd', 'dat', 'dcm', 'dicom', 'dm3', 'dv', 
                    'eps', 'epsi', 'fits', 'flex', 'fli', 'gel', 'gif', 'grey', 
                    'hdr', 'html', 'hx', 'ics', 'ids', 'img', 'ims', 'ipl', 
                    'ipm', 'ipw', 'jp2', 'jpeg', 'jpg', 'l2d', 'labels', 'lei', 
                    'lif', 'liff', 'lim', 'lsm', 'mdb', 'mnc', 'mng', 'mov', 
                    'mrc', 'mrw', 'mtb', 'naf', 'nd', 'nd2', 'nef', 'nhdr', 
                    'nrrd', 'obsep', 'oib', 'oif', 'ome', 'ome.tiff', 'pcx', 
                    'pgm', 'pic', 'pict', 'png', 'ps', 'psd', 'r3d', 'raw', 
                    'scn', 'sdt', 'seq', 'sld', 'stk', 'svs', 'tif', 'tiff', 
                    'tnb', 'txt', 'vws', 'xdce', 'xml', 'xv', 'xys', 'zvi')
WRITABLE_FORMATS = ('avi', 'eps', 'epsi', 'ics', 'ids', 'jp2', 'jpeg', 'jpg', 
                    'mov', 'ome', 'ome.tiff', 'png', 'ps', 'tif', 'tiff')

ImageReader = _formatreader.make_image_reader_class()
FormatTools = _formatreader.make_format_tools_class()
OMETiffWriter = _formatwriter.make_ome_tiff_writer_class()
ChannelSeparator = _formatreader.make_reader_wrapper_class(
    "loci/formats/ChannelSeparator")

from .metadatatools import createOMEXMLMetadata as create_ome_xml_metadata
from .metadatatools import wrap_imetadata_object
import metadatatools as _metadatatools
PixelType = _metadatatools.make_pixel_type_class()

load_image = _formatreader.load_using_bioformats

def init_logger():
    javabridge.static_call("org/apache/log4j/BasicConfigurator",
                           "configure", "()V")
    log4j_logger = javabridge.static_call("org/apache/log4j/Logger",
                                          "getRootLogger",
                                          "()Lorg/apache/log4j/Logger;")
    warn_level = javabridge.get_static_field("org/apache/log4j/Level", "WARN",
                                             "Lorg/apache/log4j/Level;")
    javabridge.call(log4j_logger, "setLevel", "(Lorg/apache/log4j/Level;)V", 
                    warn_level)


if __name__ == "__main__":
    # Handy-dandy PyShell for exploring BioFormats / Rhino / ImageJ
    import wx.py.PyCrust
    
    wx.py.PyCrust.main()
    J.kill_vm()
