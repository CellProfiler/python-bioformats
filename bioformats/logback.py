# Python-bioformats is distributed under the GNU General Public
# License, but this file is licensed under the more permissive BSD
# license.  See the accompanying file LICENSE for details.
#
# Copyright (c) 2009-2014 Broad Institute
# All rights reserved.

import javabridge

def basic_config():
    '''Configure logging for "WARN" level'''
    logback = javabridge.JClassWrapper("loci.common.LogbackTools")
    logback.enableLogging()
    logback.setRootLevel("WARN")
