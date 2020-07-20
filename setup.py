import setuptools

setuptools.setup(
    author="Lee Kamentsky",
    author_email="leek@broadinstitute.org",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Programming Language :: Java",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion"
    ],
    description="Read and write life sciences file formats",
    extras_require={
        "test": [
            "pytest>=3.3.2,<4"
        ]
    },
    install_requires=[
        "boto3>=1.14.23",
        "future>=0.18.2",
        "python-javabridge>=4.0.0rc2"
    ],
    license="GPL License",
    long_description="""Python-bioformats is a Python wrapper for Bio-Formats, a standalone Java library for reading
    and writing life sciences image file formats. Bio-Formats is capable of parsing both pixels and metadata for a
    large number of formats, as well as writing to several formats. Python-bioformats uses the python-javabridge to
    start a Java virtual machine from Python and interact with it. Python-bioformats was developed for and is used by
    the cell image analysis software CellProfiler (cellprofiler.org).""",
    name="python-bioformats",
    package_data={
        "bioformats": [
            "jars/*.jar"
        ]
    },
    packages=[
        "bioformats"
    ],
    url="http://github.com/CellProfiler/python-bioformats/",
    setup_requires = ['setuptools_scm'],
    use_scm_version = {
        "write_to": "bioformats/_version.py",
    },
)
