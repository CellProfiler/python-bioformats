import os.path
import re
import subprocess
from setuptools import setup, find_packages

def get_version():
    """Get version from git or file system.

    If this is a git repository, try to get the version number by
    running ``git describe``, then store it in
    bioformats/_version.py. Otherwise, try to load the version number
    from that file. If both methods fail, quietly return None.

    """
    git_version = None
    if os.path.exists(os.path.join(os.path.dirname(__file__), '.git')):
        import subprocess
        try:
            git_version = subprocess.check_output(['git', 'describe']).strip()
        except:
            pass

    version_file = os.path.join(os.path.dirname(__file__), 'bioformats', 
                                '_version.py')
    if os.path.exists(version_file):
        with open(version_file) as f:
            cached_version_line = f.read().strip()
        try:
            # From http://stackoverflow.com/a/3619714/17498
            cached_version = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", 
                                       cached_version_line, re.M).group(1)
        except:
            raise RuntimeError("Unable to find version in %s" % version_file)
    else:
        cached_version = None

    if git_version and git_version != cached_version:
        with open(version_file, 'w') as f:
            print >>f, '__version__ = "%s"' % git_version

    return git_version or cached_version

setup(
    name="python-bioformats",
    version=get_version(),
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
    packages=['bioformats'],
    classifiers=['Development Status :: 5 - Production/Stable',
                 'License :: OSI Approved :: GPL License',
                 'Programming Language :: Java',
                 'Topic :: Scientific/Engineering :: Bio-Informatics',
                 'Topic :: Multimedia :: Graphics :: Graphics Conversion'
             ],
    license='GPL License',
    package_data={'bioformats': ['jars/*.jar']},
    install_requires=['javabridge>=1.0']
)

