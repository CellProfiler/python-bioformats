# Python-bioformats is distributed under the GNU General Public
# License, but this file is licensed under the more permissive BSD
# license.  See the accompanying file LICENSE for details.
# 
# Copyright (c) 2009-2014 Broad Institute
# All rights reserved.

import unittest
import javabridge

def basic_config():
    rootLoggerName = javabridge.get_static_field("org/slf4j/Logger",
                                                 "ROOT_LOGGER_NAME", "Ljava/lang/String;")
    rootLogger = javabridge.static_call("org/slf4j/LoggerFactory",
                                       "getLogger", "(Ljava/lang/String;)Lorg/slf4j/Logger;", rootLoggerName)
    logLevel = javabridge.get_static_field("ch/qos/logback/classic/Level",
                                                "WARN", "Lch/qos/logback/classic/Level;")
    javabridge.call(rootLogger, "setLevel", "(Lch/qos/logback/classic/Level;)V",
                    logLevel)
