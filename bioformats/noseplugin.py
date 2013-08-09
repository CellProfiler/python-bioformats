# CellProfiler is distributed under the GNU General Public License.
# See the accompanying file LICENSE for details.
# 
# Copyright (c) 2003-2009 Massachusetts Institute of Technology
# Copyright (c) 2009-2013 Broad Institute
# 
# Please see the AUTHORS file for credits.
# 
# Website: http://www.cellprofiler.org

import logging
from nose.plugins import Plugin

import javabridge


log = logging.getLogger(__name__)


class Log4JPlugin(Plugin):
    '''
    Plugin that initializes Log4J in order to avoid Bioformats error
    messages.

    '''
    enabled = False
    name = "log4j"
    score = 90 # Less than the score of javabridge.nosetests.JavaBridgePlugin

    def begin(self):
        javabridge.static_call("org/apache/log4j/BasicConfigurator",
                               "configure", "()V")
        log4j_logger = javabridge.static_call("org/apache/log4j/Logger",
                                              "getRootLogger",
                                              "()Lorg/apache/log4j/Logger;")
        warn_level = javabridge.get_static_field("org/apache/log4j/Level","WARN",
                                                 "Lorg/apache/log4j/Level;")
        javabridge.call(log4j_logger, "setLevel", "(Lorg/apache/log4j/Level;)V", 
                        warn_level)
