# Python-bioformats is distributed under the GNU General Public
# License, but this file is licensed under the more permissive BSD
# license.  See the accompanying file LICENSE for details.
# 
# Copyright (c) 2009-2014 Broad Institute
# All rights reserved.

import unittest
import javabridge

def basic_config():
    javabridge.static_call("org/apache/log4j/BasicConfigurator",
                           "configure", "()V")
    log4j_logger = javabridge.static_call("org/apache/log4j/Logger",
                                          "getRootLogger",
                                          "()Lorg/apache/log4j/Logger;")
    warn_level = javabridge.get_static_field("org/apache/log4j/Level","WARN",
                                             "Lorg/apache/log4j/Level;")
    javabridge.call(log4j_logger, "setLevel", "(Lorg/apache/log4j/Level;)V", 
                    warn_level)
