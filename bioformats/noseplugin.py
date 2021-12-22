# Python-bioformats is distributed under the GNU General Public
# License, but this file is licensed under the more permissive BSD
# license.  See the accompanying file LICENSE for details.
#
# Copyright (c) 2009-2014 Broad Institute
# All rights reserved.

from __future__ import absolute_import, unicode_literals

import logging
from nose.plugins import Plugin

import javabridge


log = logging.getLogger(__name__)


class LogbackPlugin(Plugin):
    '''
    Plugin that initializes Logback in order to avoid Bioformats error
    messages.

    '''
    enabled = False
    name = "logback"
    score = 90 # Less than the score of javabridge.nosetests.JavaBridgePlugin

    def begin(self):
        javabridge.static_call("org/apache/logback/BasicConfigurator",
                               "configure", "()V")
        logback_logger = javabridge.static_call("org/apache/logback/Logger",
                                              "getRootLogger",
                                              "()Lorg/apache/logback/Logger;")
        warn_level = javabridge.get_static_field("org/apache/logback/Level","WARN",
                                                 "Lorg/apache/logback/Level;")
        javabridge.call(logback_logger, "setLevel", "(Lorg/apache/logback/Level;)V",
                        warn_level)
