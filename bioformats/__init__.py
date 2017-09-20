# Python-bioformats is distributed under the GNU General Public
# License, but this file is licensed under the more permissive BSD
# license.  See the accompanying file LICENSE for details.
#
# Copyright (c) 2009-2014 Broad Institute
# All rights reserved.

'''Bioformats package - wrapper for loci.bioformats java code

'''

from __future__ import absolute_import, unicode_literals

try:
    from _version import __version__
except ImportError:
    # We're running in a tree that doesn't have a _version.py, so we don't know what our version is.
    __version__ = "0.0.0"

import os.path
import javabridge
from . import formatreader as _formatreader
from . import formatwriter as _formatwriter

_jars_dir = os.path.join(os.path.dirname(__file__), 'jars')

JAR_VERSION = '5.7.1'

JARS = javabridge.JARS + [os.path.realpath(os.path.join(_jars_dir, name + '.jar'))
                          for name in ['loci_tools']]
"""List of directories, jar files, and zip files that should be added
to the Java virtual machine's class path."""

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

OMETiffWriter = _formatwriter.make_ome_tiff_writer_class()
ChannelSeparator = _formatreader.make_reader_wrapper_class(
    "loci/formats/ChannelSeparator")


from .metadatatools import createOMEXMLMetadata as create_ome_xml_metadata
from .metadatatools import wrap_imetadata_object
from . import metadatatools as _metadatatools
PixelType = _metadatatools.make_pixel_type_class()
get_metadata_options = _metadatatools.get_metadata_options

# Reading images

ImageReader = _formatreader.ImageReader
load_image = _formatreader.load_using_bioformats
load_image_url = _formatreader.load_using_bioformats_url

# Cached image readers

get_image_reader = _formatreader.get_image_reader
release_image_reader = _formatreader.release_image_reader
clear_image_reader_cache = _formatreader.clear_image_reader_cache

# Metadata

from .omexml import OMEXML
get_omexml_metadata = _formatreader.get_omexml_metadata

# Writing images

write_image = _formatwriter.write_image

from .omexml import PT_UINT16, PT_UINT8, PT_BIT

# Omero

from .formatreader import use_omero_credentials, set_omero_credentials, get_omero_credentials
from .formatreader import set_omero_login_hook, omero_logout, has_omero_packages
from .formatreader import K_OMERO_SERVER, K_OMERO_PORT, K_OMERO_USER, K_OMERO_SESSION_ID,\
         K_OMERO_PASSWORD, K_OMERO_CONFIG_FILE

from . import omexml


if __name__ == "__main__":
    # Handy-dandy PyShell for exploring BioFormats / Rhino / ImageJ
    import wx.py.PyCrust

    wx.py.PyCrust.main()
    J.kill_vm()
