from setuptools import setup, find_packages

setup(
    name="python-bioformats",
    version="1.0.0pr2",
    description="Read and write life sciences file formats",
    long_description='''Python-bioformats is a Python wrapper for Bio-Formats, a standalone
    Java library for reading and writing life sciences image file
    formats. Bio-Formats is capable of parsing both pixels and
    metadata for a large number of formats, as well as writing to
    several formats. Python-bioformats uses the python-javabridge to
    start a Java virtual machine from Python and interact with
    it. Python-bioformats was developed for and is used by the cell
    image analysis software CellProfiler (cellprofiler.org).''',
    url="http://github.com/CellProfiler/python-bioformats/",
    bugtrack_url="http://github.com/CellProfiler/python-bioformats/issues",
    packages=['bioformats'],
    classifiers=['Development Status :: 5 - Production/Stable',
                 'License :: OSI Approved :: BSD License',
                 'Programming Language :: Java',
                 'Topic :: Scientific/Engineering :: Bio-Informatics',
                 'Topic :: Multimedia :: Graphics :: Graphics Conversion'
             ],
    license='BSD License',
    package_data={'bioformats': ['jars/*.jar']},
    install_requires=['javabridge>=1.0'],
    tests_require='nose',
    entry_points={'nose.plugins.0.10': [
            'javabridge = javabridge.noseplugin:JavabridgePlugin',
            ]},
    test_suite='nose.collector'
)

