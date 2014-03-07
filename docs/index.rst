===================================================================
python-bioformats: read and write life sciences image file formats
===================================================================

The python-bioformats package is an interface to the `Bioformats
<http://loci.wisc.edu/software/bio-formats>`_ library for reading and
writing life sciences image file formats.

Because Bioformats is a Java library, python-bioformats uses
python-javabridge to start and interact with a Java virtual machine.

Python-bioformats and python-javabridge were developed for and are
used by the cell image analysis software CellProfiler
(cellprofiler.org).


Installation and testing
========================

Install using pip
-----------------

    pip install python-bioformats


Running the unit tests
----------------------

Running the unit tests requires Nose.

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

