#!/usr/bin/env python

import nose
from javabridge.noseplugin import JavabridgePlugin

if __name__ == '__main__':
    nose.main(plugins=[JavabridgePlugin()])

