#!/usr/bin/env python

from __future__ import absolute_import, unicode_literals

import nose
from javabridge.noseplugin import JavabridgePlugin

if __name__ == '__main__':
    nose.main(plugins=[JavabridgePlugin()])

