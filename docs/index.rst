===================================================================
python-bioformats: read and write life sciences image file formats
===================================================================

The python-bioformats package is an interface to the `Bio-Formats
<http://www.openmicroscopy.org/site/products/bio-formats>`_ library
for reading and writing life sciences image file formats.

Because Bio-Formats is a Java library, python-bioformats uses
python-javabridge to start and interact with a Java virtual machine.

Python-bioformats and python-javabridge were developed for and are
used by the cell image analysis software CellProfiler
(cellprofiler.org).

python-bioformats is licensed under the GNU General Public License
(GPL).  Many files are licensed under the more permissive BSD license.


Installation and testing
========================

Install using pip
-----------------

    pip install python-bioformats


Running the unit tests
----------------------

Running the unit tests requires Nose::

    nosetests

On some installations, the following also works::

    python nosetests.py


Starting the JVM
================

When starting the Java virtual machine with python-javabridge's
:py:func:`javabridge.start_vm`, you must add the contents of
:py:data:`bioformats.JARS` to the class path. Example:

>>> import javabridge
>>> import bioformats
>>> javabridge.start_vm(class_path=bioformats.JARS)

.. autodata:: bioformats.JARS
   :annotation: list of strings

Initialization and termination
==============================

The javabridge package must be used to start the JVM with loci_tools.jar
which is the Bio-Formats library packaged with python-bioformats or with
your own build of Bio-Formats. As a convenience, bioformats.JARS has a list
of the required jar files.

.. code::

    import javabridge
    import bioformats
    javabridge.start_vm(class_path=bioformats.JARS)
    
    # your program goes here

    javabridge.kill_vm()
    
Reading images
==============

.. autoclass:: bioformats.ImageReader

   .. automethod:: bioformats.ImageReader.read
   .. automethod:: bioformats.ImageReader.close

Convenience functions that create an image reader for a file path or
URL and use it to read an image:

.. autofunction:: bioformats.load_image
.. autofunction:: bioformats.load_image_url


Cached image readers
====================

.. autofunction:: bioformats.get_image_reader
.. autofunction:: bioformats.release_image_reader
.. autofunction:: bioformats.clear_image_reader_cache


Metadata
========

.. autofunction:: bioformats.get_omexml_metadata
.. autoclass:: bioformats.OMEXML

   .. autoattribute:: bioformats.OMEXML.image_count
      :annotation: Settable.
   .. automethod:: bioformats.OMEXML.image                 

   .. autoclass:: bioformats::OMEXML.Image

      .. autoattribute:: bioformats::OMEXML.Image.Pixels


Writing images
==============

.. autofunction:: bioformats.write_image

.. autodata:: bioformats.PT_UINT16
.. autodata:: bioformats.PT_UINT8
.. autodata:: bioformats.PT_BIT


OMERO
=====

Python-bioformats can load images from OMERO URLs. To do this, you'll need
to put the JAR files for your OMERO server version onto your Java classpath
when you start. For OMERO server 5.0.0, these are blitz.jar, common.jar,
ice.jar, ice-glacier2.jar, ice-storm.jar and ice-grid.jar. You'll also need
to use the matching version of the Bio-formats library for the OMERO release
instead of the one included with python-bioformats.

.. autofunction:: bioformats.use_omero_credentials
.. autofunction:: bioformats.set_omero_credentials
.. autofunction:: bioformats.get_omero_credentials
.. autofunction:: bioformats.omero_logout

.. autofunction:: bioformats.set_omero_login_hook

Keys for the `credentials` dict
-------------------------------

.. autodata:: bioformats.K_OMERO_SERVER
.. autodata:: bioformats.K_OMERO_PORT
.. autodata:: bioformats.K_OMERO_USER
.. autodata:: bioformats.K_OMERO_SESSION_ID
.. autodata:: bioformats.K_OMERO_PASSWORD
.. autodata:: bioformats.K_OMERO_CONFIG_FILE




Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

