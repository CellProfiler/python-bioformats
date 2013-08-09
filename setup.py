from setuptools import setup, find_packages

setup(
    name="python-bioformats",
    packages=['bioformats'],
    package_data={'bioformats': ['jars/*.jar']},

    tests_require='nose',
    entry_points={'nose.plugins.0.10': [
            'javabridge = javabridge.noseplugin:JavabridgePlugin',
            ]},
    test_suite='nose.collector'
)

