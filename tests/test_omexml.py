# Python-bioformats is distributed under the GNU General Public
# License, but this file is licensed under the more permissive BSD
# license.  See the accompanying file LICENSE for details.
#
# Copyright (c) 2009-2014 Broad Institute
# All rights reserved.

"""test_omexml.py read and write OME xml

"""

from __future__ import absolute_import, unicode_literals

import datetime
import os

import pytest

import bioformats.omexml


@pytest.fixture
def groupfiles_xml():
    path = os.path.join(os.path.split(__file__)[0], "resources", "groupfiles.xml")
    fd = open(path)
    return fd.read()


@pytest.fixture
def tiff_xml():
    path = os.path.join(os.path.split(__file__)[0], "resources", "tiff.xml")
    fd = open(path)
    return fd.read()


def test_00_00_init():
    o = bioformats.omexml.OMEXML()
    assert o.root_node.tag == bioformats.omexml.qn(o.get_ns("ome"), "OME")
    assert o.image_count == 1


def test_01_01_read(groupfiles_xml, tiff_xml):
    for xml in (groupfiles_xml, tiff_xml):
        o = bioformats.omexml.OMEXML(xml)


def test_02_01_iter_children(tiff_xml):
    o = bioformats.omexml.OMEXML(tiff_xml)
    for node, expected_tag in zip(
            o.root_node,
            (bioformats.omexml.qn(o.get_ns("ome"), "Image"),
             bioformats.omexml.qn(o.get_ns("sa"), "StructuredAnnotations"))):
        assert node.tag == expected_tag


def test_02_02_get_text(tiff_xml):
    o = bioformats.omexml.OMEXML(tiff_xml)
    ad = o.root_node.find(
        "/".join([bioformats.omexml.qn(o.get_ns('ome'), x) for x in ("Image", "AcquisitionDate")]))
    assert bioformats.omexml.get_text(ad) == "2008-02-05T17:24:46"


def test_02_04_set_text(tiff_xml):
    o = bioformats.omexml.OMEXML(tiff_xml)
    ad = o.root_node.find("/".join(
        [bioformats.omexml.qn(o.get_ns('ome'), x) for x in ("Image", "AcquisitionDate")]))
    im = o.root_node.find(bioformats.omexml.qn(o.get_ns("ome"), "Image"))
    bioformats.omexml.set_text(im, "Foo")
    assert bioformats.omexml.get_text(im) == "Foo"
    bioformats.omexml.set_text(ad, "Bar")
    assert bioformats.omexml.get_text(ad) == "Bar"


def test_03_01_get_image_count(groupfiles_xml, tiff_xml):
    for xml, count in ((groupfiles_xml, 576), (tiff_xml, 1)):
        o = bioformats.omexml.OMEXML(xml)
        assert o.image_count == count


def test_03_02_set_image_count(tiff_xml):
    o = bioformats.omexml.OMEXML(tiff_xml)
    o.image_count = 2
    assert len(o.root_node.findall(bioformats.omexml.qn(o.get_ns("ome"), "Image"))) == 2


def test_03_03_image(groupfiles_xml):
    o = bioformats.omexml.OMEXML(groupfiles_xml)
    assert o.image_count == 576
    for i in range(576):
        im = o.image(i)
        assert im.node.get("ID") == "Image:%d" % i


def test_03_04_structured_annotations(tiff_xml):
    o = bioformats.omexml.OMEXML(tiff_xml)
    assert o.structured_annotations.node.tag == bioformats.omexml.qn(o.get_ns("sa"), "StructuredAnnotations")


def test_04_01_image_get_id(tiff_xml):
    o = bioformats.omexml.OMEXML(tiff_xml)
    assert o.image(0).ID == "Image:0"


def test_04_02_image_set_id(tiff_xml):
    o = bioformats.omexml.OMEXML(tiff_xml)
    o.image(0).ID = "Foo"
    assert o.image(0).node.get("ID") == "Foo"


def test_04_03_image_get_name(tiff_xml):
    o = bioformats.omexml.OMEXML(tiff_xml)
    assert o.image(0).Name == "Channel1-01-A-01.tif"


def test_04_04_image_set_name(tiff_xml):
    o = bioformats.omexml.OMEXML(tiff_xml)
    o.image(0).Name = "Foo"
    assert o.image(0).node.get("Name") == "Foo"


def test_04_05_image_get_acquisition_date(tiff_xml):
    o = bioformats.omexml.OMEXML(tiff_xml)
    assert o.image(0).AcquisitionDate == "2008-02-05T17:24:46"


def test_04_06_image_set_acquisition_date(tiff_xml):
    o = bioformats.omexml.OMEXML(tiff_xml)
    o.image(0).AcquisitionDate = "2011-12-21T11:04:14.903000"
    assert o.image(0).AcquisitionDate == "2011-12-21T11:04:14.903000"


def test_04_07_image_1_acquisition_date():
    # regression test of #38
    o = bioformats.omexml.OMEXML()
    o.set_image_count(2)
    date_1 = "2011-12-21T11:04:14.903000"
    date_2 = "2015-10-13T09:57:00.000000"
    o.image(0).AcquisitionDate = date_1
    o.image(1).AcquisitionDate = date_2
    assert o.image(0).AcquisitionDate == date_1
    assert o.image(1).AcquisitionDate == date_2


def test_05_01_pixels_get_id(tiff_xml):
    o = bioformats.omexml.OMEXML(tiff_xml)
    assert o.image(0).Pixels.ID == "Pixels:0"


def test_05_02_pixels_set_id(tiff_xml):
    o = bioformats.omexml.OMEXML(tiff_xml)
    o.image(0).Pixels.ID = "Foo"
    assert o.image(0).Pixels.ID == "Foo"


def test_05_03_pixels_get_dimension_order(tiff_xml):
    o = bioformats.omexml.OMEXML(tiff_xml)
    assert o.image(0).Pixels.DimensionOrder == bioformats.omexml.DO_XYCZT


def test_05_04_pixels_set_dimension_order(tiff_xml):
    o = bioformats.omexml.OMEXML(tiff_xml)
    o.image(0).Pixels.DimensionOrder = bioformats.omexml.DO_XYZCT
    assert o.image(0).Pixels.DimensionOrder == bioformats.omexml.DO_XYZCT


def test_05_05_pixels_get_pixel_type(tiff_xml):
    o = bioformats.omexml.OMEXML(tiff_xml)
    assert o.image(0).Pixels.PixelType == bioformats.omexml.PT_UINT8


def test_05_06_pixels_set_pixel_type(tiff_xml):
    o = bioformats.omexml.OMEXML(tiff_xml)
    o.image(0).Pixels.PixelType = bioformats.omexml.PT_FLOAT
    assert o.image(0).Pixels.PixelType == bioformats.omexml.PT_FLOAT


def test_05_07_pixels_get_size_x(tiff_xml):
    o = bioformats.omexml.OMEXML(tiff_xml)
    assert o.image(0).Pixels.SizeX == 640


def test_05_08_pixels_set_size_x(tiff_xml):
    o = bioformats.omexml.OMEXML(tiff_xml)
    o.image(0).Pixels.SizeX = 480
    assert o.image(0).Pixels.SizeX == 480


def test_05_09_pixels_get_size_y(tiff_xml):
    o = bioformats.omexml.OMEXML(tiff_xml)
    assert o.image(0).Pixels.SizeY == 512


def test_05_10_pixels_set_size_y(tiff_xml):
    o = bioformats.omexml.OMEXML(tiff_xml)
    o.image(0).Pixels.SizeY = 480
    assert o.image(0).Pixels.SizeY == 480


def test_05_11_pixels_get_size_z(tiff_xml):
    o = bioformats.omexml.OMEXML(tiff_xml)
    assert o.image(0).Pixels.SizeZ == 1


def test_05_12_pixels_set_size_z(tiff_xml):
    o = bioformats.omexml.OMEXML(tiff_xml)
    o.image(0).Pixels.SizeZ = 2
    assert o.image(0).Pixels.SizeZ == 2


def test_05_13_pixels_get_size_c(tiff_xml):
    o = bioformats.omexml.OMEXML(tiff_xml)
    assert o.image(0).Pixels.SizeC == 2


def test_05_14_pixels_set_size_c(tiff_xml):
    o = bioformats.omexml.OMEXML(tiff_xml)
    o.image(0).Pixels.SizeC = 3
    assert o.image(0).Pixels.SizeC == 3


def test_05_15_pixels_get_size_t(tiff_xml):
    o = bioformats.omexml.OMEXML(tiff_xml)
    assert o.image(0).Pixels.SizeT == 3


def test_05_16_pixels_set_size_t(tiff_xml):
    o = bioformats.omexml.OMEXML(tiff_xml)
    o.image(0).Pixels.SizeT = 1
    assert o.image(0).Pixels.SizeT == 1


def test_05_17_pixels_get_channel_count(tiff_xml):
    o = bioformats.omexml.OMEXML(tiff_xml)
    assert o.image(0).Pixels.channel_count == 1


def test_05_18_pixels_set_channel_count(tiff_xml):
    o = bioformats.omexml.OMEXML(tiff_xml)
    o.image(0).Pixels.channel_count = 2
    assert len(o.image(0).Pixels.node.findall(bioformats.omexml.qn(o.get_ns("ome"), "Channel"))) == 2


def test_06_01_channel_get_id(tiff_xml):
    o = bioformats.omexml.OMEXML(tiff_xml)
    assert o.image(0).Pixels.Channel(0).ID == "Channel:0:0"


def test_06_02_channel_set_id(tiff_xml):
    o = bioformats.omexml.OMEXML(tiff_xml)
    o.image(0).Pixels.Channel(0).ID = "Red"
    assert o.image(0).Pixels.Channel(0).ID == "Red"


def test_06_03_channel_get_name(tiff_xml):
    o = bioformats.omexml.OMEXML(tiff_xml)
    assert o.image(0).Pixels.Channel(0).Name == "Actin"


def test_06_04_channel_set_Name(tiff_xml):
    o = bioformats.omexml.OMEXML(tiff_xml)
    o.image(0).Pixels.Channel(0).Name = "PI"
    assert o.image(0).Pixels.Channel(0).Name == "PI"


def test_06_04_channel_get_samples_per_pixel(tiff_xml):
    o = bioformats.omexml.OMEXML(tiff_xml)
    assert o.image(0).Pixels.Channel(0).SamplesPerPixel == 1


def test_06_04_channel_set_samples_per_pixel(tiff_xml):
    o = bioformats.omexml.OMEXML(tiff_xml)
    o.image(0).Pixels.Channel(0).SamplesPerPixel = 3
    assert o.image(0).Pixels.Channel(0).SamplesPerPixel == 3


def test_07_01_sa_get_item(tiff_xml):
    o = bioformats.omexml.OMEXML(tiff_xml)
    a = o.structured_annotations["Annotation:4"]
    assert a.tag, bioformats.omexml.qn(o.get_ns("sa") == "XMLAnnotation")
    values = a.findall(bioformats.omexml.qn(o.get_ns("sa"), "Value"))
    assert len(values) == 1
    oms = values[0].findall(bioformats.omexml.qn(bioformats.omexml.NS_ORIGINAL_METADATA, "OriginalMetadata"))
    assert len(oms) == 1
    keys = oms[0].findall(bioformats.omexml.qn(bioformats.omexml.NS_ORIGINAL_METADATA, "Key"))
    assert len(keys) == 1
    assert bioformats.omexml.get_text(keys[0]) == "XResolution"
    values = oms[0].findall(bioformats.omexml.qn(bioformats.omexml.NS_ORIGINAL_METADATA, "Value"))
    assert len(values) == 1
    assert bioformats.omexml.get_text(values[0]) == "72"


def test_07_02_01_sa_keys(tiff_xml):
    keys = bioformats.omexml.OMEXML(tiff_xml).structured_annotations.keys()
    for i in range(21):
        assert "Annotation:%d" % i in keys


def test_07_02_02_sa_has_key(tiff_xml):
    o = bioformats.omexml.OMEXML(tiff_xml)
    for i in range(20):
        assert "Annotation:%d" % i in o.structured_annotations
    assert "Foo" not in o.structured_annotations


def test_07_03_om_getitem(tiff_xml):
    o = bioformats.omexml.OMEXML(tiff_xml)
    assert o.structured_annotations.OriginalMetadata["MetaMorph"] == "no"


def test_07_04_01_om_keys(tiff_xml):
    o = bioformats.omexml.OMEXML(tiff_xml)
    keys = o.structured_annotations.OriginalMetadata.keys()
    assert len(keys) == 21
    for k in ("DateTime", "Software", "YResolution"):
        assert k in keys


def test_07_04_02_om_has_key(tiff_xml):
    o = bioformats.omexml.OMEXML(tiff_xml)
    om = o.structured_annotations.OriginalMetadata
    for k in ("DateTime", "Software", "YResolution"):
        assert k in om
    assert "Foo" not in om


def test_07_05_om_setitem():
    o = bioformats.omexml.OMEXML()
    o.structured_annotations.OriginalMetadata["Foo"] = "Bar"
    sa = o.structured_annotations.node
    a = sa.findall(bioformats.omexml.qn(o.get_ns("sa"), "XMLAnnotation"))
    assert len(a) == 1
    vs = a[0].findall(bioformats.omexml.qn(o.get_ns("sa"), "Value"))
    assert len(vs) == 1
    om = vs[0].findall(bioformats.omexml.qn(bioformats.omexml.NS_ORIGINAL_METADATA, "OriginalMetadata"))
    assert len(om) == 1
    k = om[0].findall(bioformats.omexml.qn(bioformats.omexml.NS_ORIGINAL_METADATA, "Key"))
    assert len(k) == 1
    assert bioformats.omexml.get_text(k[0]) == "Foo"
    v = om[0].findall(bioformats.omexml.qn(bioformats.omexml.NS_ORIGINAL_METADATA, "Value"))
    assert len(v) == 1
    assert bioformats.omexml.get_text(v[0]) == "Bar"


def test_08_01_get_plate(groupfiles_xml):
    o = bioformats.omexml.OMEXML(groupfiles_xml)
    plate = o.plates[0]
    assert plate.ID == "Plate:0"


def test_08_02_get_plate_count(groupfiles_xml):
    o = bioformats.omexml.OMEXML(groupfiles_xml)
    assert len(o.plates) == 1


def test_08_02_new_plate(groupfiles_xml):
    o = bioformats.omexml.OMEXML(groupfiles_xml)
    o.plates.newPlate("MyPlate", "Plate:1")
    assert o.plates[1].ID == "Plate:1"
    assert o.plates[1].Name == "MyPlate"


def test_08_03_plate_iter(groupfiles_xml):
    o = bioformats.omexml.OMEXML(groupfiles_xml)
    nplates = 5
    for i in range(1, nplates):
        o.plates.newPlate("MyPlate%d" % i, "Plate:%d" % i)
    for i, plate in enumerate(o.plates):
        assert plate.ID == "Plate:%d" % i


def test_08_04_plate_slice(groupfiles_xml):
    o = bioformats.omexml.OMEXML(groupfiles_xml)
    for i in range(1, 5):
        o.plates.newPlate("MyPlate%d" % i, "Plate:%d" % i)
    plates = o.plates[2:-1]
    assert len(plates) == 2
    assert all([plate.ID == "Plate:%d" % (i + 2) for i, plate in enumerate(plates)])

    plates = o.plates[-4:4]
    assert len(plates) == 3
    assert all([plate.ID == "Plate:%d" % (i + 1) for i, plate in enumerate(plates)])


def test_09_01_plate_get_name(groupfiles_xml):
    o = bioformats.omexml.OMEXML(groupfiles_xml)
    assert o.plates[0].Name == "TimePoint_1"


def test_09_02_plate_set_status():
    o = bioformats.omexml.OMEXML()
    plate = o.plates.newPlate("Foo", "Bar")
    plate.Status = "Gronked"
    assert plate.node.get("Status") == "Gronked"


def test_09_03_plate_get_status():
    o = bioformats.omexml.OMEXML()
    plate = o.plates.newPlate("Foo", "Bar")
    plate.node.set("Status", "Gronked")
    assert plate.Status == "Gronked"


def test_09_04_plate_get_external_identifier():
    o = bioformats.omexml.OMEXML()
    plate = o.plates.newPlate("Foo", "Bar")
    plate.node.set("ExternalIdentifier", "xyz")
    assert plate.ExternalIdentifier == "xyz"


def test_09_05_plate_set_external_identifier():
    o = bioformats.omexml.OMEXML()
    plate = o.plates.newPlate("Foo", "Bar")
    plate.ExternalIdentifier = "xyz"
    assert plate.node.get("ExternalIdentifier") == "xyz"


def test_09_06_plate_get_column_naming_convention():
    o = bioformats.omexml.OMEXML()
    plate = o.plates.newPlate("Foo", "Bar")
    plate.node.set("ColumnNamingConvention", bioformats.omexml.NC_LETTER)
    assert plate.ColumnNamingConvention == bioformats.omexml.NC_LETTER


def test_09_07_plate_set_column_naming_convention():
    o = bioformats.omexml.OMEXML()
    plate = o.plates.newPlate("Foo", "Bar")
    plate.ColumnNamingConvention = bioformats.omexml.NC_NUMBER
    assert plate.ColumnNamingConvention == bioformats.omexml.NC_NUMBER


def test_09_08_plate_get_row_naming_convention():
    o = bioformats.omexml.OMEXML()
    plate = o.plates.newPlate("Foo", "Bar")
    plate.node.set("RowNamingConvention", bioformats.omexml.NC_LETTER)
    assert plate.RowNamingConvention == bioformats.omexml.NC_LETTER


def test_09_09_plate_set_row_naming_convention():
    o = bioformats.omexml.OMEXML()
    plate = o.plates.newPlate("Foo", "Bar")
    plate.RowNamingConvention = bioformats.omexml.NC_NUMBER
    assert plate.RowNamingConvention == bioformats.omexml.NC_NUMBER


def test_09_10_plate_get_well_origin_x():
    o = bioformats.omexml.OMEXML()
    plate = o.plates.newPlate("Foo", "Bar")
    plate.node.set("WellOriginX", "4.8")
    assert plate.WellOriginX == 4.8


def test_09_11_plate_set_well_origin_x():
    o = bioformats.omexml.OMEXML()
    plate = o.plates.newPlate("Foo", "Bar")
    plate.WellOriginX = 3.5
    assert plate.node.get("WellOriginX") == "3.5"


def test_09_12_plate_get_well_origin_y():
    o = bioformats.omexml.OMEXML()
    plate = o.plates.newPlate("Foo", "Bar")
    plate.node.set("WellOriginY", "5.8")
    assert plate.WellOriginY == 5.8


def test_09_13_plate_set_well_origin_y():
    o = bioformats.omexml.OMEXML()
    plate = o.plates.newPlate("Foo", "Bar")
    plate.WellOriginY = 3.5
    assert plate.node.get("WellOriginY") == "3.5"


def test_09_14_plate_get_rows():
    o = bioformats.omexml.OMEXML()
    plate = o.plates.newPlate("Foo", "Bar")
    plate.node.set("Rows", "8")
    assert plate.Rows == 8


def test_09_15_plate_set_rows():
    o = bioformats.omexml.OMEXML()
    plate = o.plates.newPlate("Foo", "Bar")
    plate.Rows = 16
    assert plate.node.get("Rows") == "16"


def test_09_16_plate_get_columns():
    o = bioformats.omexml.OMEXML()
    plate = o.plates.newPlate("Foo", "Bar")
    plate.node.set("Columns", "12")
    assert plate.Columns == 12


def test_09_15_plate_set_columns():
    o = bioformats.omexml.OMEXML()
    plate = o.plates.newPlate("Foo", "Bar")
    plate.Columns = 24
    assert plate.node.get("Columns") == "24"


def test_10_01_wells_len(groupfiles_xml):
    o = bioformats.omexml.OMEXML(groupfiles_xml)
    assert len(o.plates[0].Well) == 96


def test_10_02_wells_by_row_and_column(groupfiles_xml):
    o = bioformats.omexml.OMEXML(groupfiles_xml)
    w = o.plates[0].Well[1, 3]
    assert w.ID == "Well:0:15"


def test_10_03_wells_by_index(groupfiles_xml):
    o = bioformats.omexml.OMEXML(groupfiles_xml)
    w = o.plates[0].Well[2]
    assert w.ID == "Well:0:2"


def test_10_04_wells_by_name(groupfiles_xml):
    o = bioformats.omexml.OMEXML(groupfiles_xml)
    w = o.plates[0].Well["C05"]
    assert w.Row == 2
    assert w.Column == 4


def test_10_05_wells_by_id(groupfiles_xml):
    o = bioformats.omexml.OMEXML(groupfiles_xml)
    w = o.plates[0].Well["Well:0:3"]
    assert w.Row == 0
    assert w.Column == 3


def test_10_06_wells_by_slice(groupfiles_xml):
    o = bioformats.omexml.OMEXML(groupfiles_xml)
    for i, w in enumerate(o.plates[0].Well[1::12]):
        assert w.Column == 1
        assert w.Row == i


def test_10_07_iter_wells(groupfiles_xml):
    o = bioformats.omexml.OMEXML(groupfiles_xml)
    for i, name in enumerate(o.plates[0].Well):
        row = int(i / 12)
        column = i % 12
        assert name == "ABCDEFGH"[row] + "%02d" % (column + 1)
    assert name == "H12"


def test_10_08_new_well():
    o = bioformats.omexml.OMEXML()
    plate = o.plates.newPlate("Foo", "Bar")
    plate.Well.new(4, 5, "xyz")
    w = plate.Well[0]
    assert w.node.get("Row") == "4"
    assert w.node.get("Column") == "5"
    assert w.node.get("ID") == "xyz"


def test_11_01_get_Column(groupfiles_xml):
    o = bioformats.omexml.OMEXML(groupfiles_xml)
    assert o.plates[0].Well["B05"].Column == 4


def test_11_02_get_Row(groupfiles_xml):
    o = bioformats.omexml.OMEXML(groupfiles_xml)
    assert o.plates[0].Well["B05"].Row == 1


def test_11_03_get_external_description():
    o = bioformats.omexml.OMEXML()
    plate = o.plates.newPlate("foo", "bar")
    w = plate.Well.new(4, 5, "xyz")
    w.node.set("ExternalDescription", "ijk")
    assert w.ExternalDescription == "ijk"


def test_11_04_set_external_description():
    o = bioformats.omexml.OMEXML()
    plate = o.plates.newPlate("foo", "bar")
    w = plate.Well.new(4, 5, "xyz")
    w.ExternalDescription = "LMO"
    assert w.node.get("ExternalDescription") == "LMO"


def test_11_05_get_external_identifier():
    o = bioformats.omexml.OMEXML()
    plate = o.plates.newPlate("foo", "bar")
    w = plate.Well.new(4, 5, "xyz")
    w.node.set("ExternalIdentifier", "ijk")
    assert w.ExternalIdentifier == "ijk"


def test_11_06_set_external_identifier():
    o = bioformats.omexml.OMEXML()
    plate = o.plates.newPlate("foo", "bar")
    w = plate.Well.new(4, 5, "xyz")
    w.ExternalIdentifier = "LMO"
    assert w.node.get("ExternalIdentifier") == "LMO"


def test_12_01_get_sample_len(groupfiles_xml):
    o = bioformats.omexml.OMEXML(groupfiles_xml)
    assert len(o.plates[0].Well[0].Sample) == 6


def test_12_02_get_sample_item(groupfiles_xml):
    o = bioformats.omexml.OMEXML(groupfiles_xml)
    s = o.plates[0].Well[0].Sample[2]
    assert s.node.get("ID") == "WellSample:0:0:2"


def test_12_03_get_sample_item_slice(groupfiles_xml):
    o = bioformats.omexml.OMEXML(groupfiles_xml)
    for i, s in enumerate(o.plates[0].Well[0].Sample[1::2]):
        assert s.node.get("ID") == "WellSample:0:0:%d" % (i * 2 + 1)


def test_12_04_iter_sample_item(groupfiles_xml):
    o = bioformats.omexml.OMEXML(groupfiles_xml)
    for i, s in enumerate(o.plates[0].Well[0].Sample):
        assert s.node.get("ID") == "WellSample:0:0:%d" % i


def test_12_05_new_sample_item():
    o = bioformats.omexml.OMEXML()
    plate = o.plates.newPlate("foo", "bar")
    w = plate.Well.new(4, 5, "xyz")
    w.Sample.new("ooo")
    w.Sample.new("ppp")
    sample_nodes = w.node.findall(bioformats.omexml.qn(o.get_ns("spw"), "WellSample"))
    assert len(sample_nodes) == 2
    assert sample_nodes[0].get("ID") == "ooo"
    assert sample_nodes[1].get("ID") == "ppp"
    assert sample_nodes[0].get("Index") == "0"
    assert sample_nodes[1].get("Index") == "1"


def test_13_01_get_sample_id(groupfiles_xml):
    o = bioformats.omexml.OMEXML(groupfiles_xml)
    assert o.plates[0].Well['A02'].Sample[3].ID == "WellSample:0:1:3"


def test_13_02_set_sample_id(groupfiles_xml):
    o = bioformats.omexml.OMEXML(groupfiles_xml)
    ws = o.plates[0].Well['A02'].Sample[3]
    ws.ID = "Foo"
    assert ws.node.get("ID") == "Foo"


def test_13_03_get_position_x(groupfiles_xml):
    o = bioformats.omexml.OMEXML(groupfiles_xml)
    assert o.plates[0].Well['A01'].Sample[4].PositionX == 402.5


def test_13_04_set_position_x(groupfiles_xml):
    o = bioformats.omexml.OMEXML(groupfiles_xml)
    ws = o.plates[0].Well['A02'].Sample[3]
    ws.PositionX = 201.75
    assert ws.node.get("PositionX") == "201.75"


def test_13_05_get_position_y(groupfiles_xml):
    o = bioformats.omexml.OMEXML(groupfiles_xml)
    assert o.plates[0].Well['A01'].Sample[4].PositionY == 204.25


def test_13_06_set_position_y(groupfiles_xml):
    o = bioformats.omexml.OMEXML(groupfiles_xml)
    ws = o.plates[0].Well['A02'].Sample[3]
    ws.PositionY = 14.5
    assert ws.node.get("PositionY") == "14.5"


def test_13_07_get_timepoint(groupfiles_xml):
    o = bioformats.omexml.OMEXML(groupfiles_xml)
    assert o.plates[0].Well['A01'].Sample[1].Timepoint == '2011-12-27T08:24:29.960000'


def test_13_08_set_timepoint(groupfiles_xml):
    o = bioformats.omexml.OMEXML(groupfiles_xml)
    ws = o.plates[0].Well['A02'].Sample[3]
    now = datetime.datetime.now()
    now_string = now.isoformat()
    ws.Timepoint = now
    assert ws.node.get("Timepoint") == now_string
    ws = o.plates[0].Well['A03'].Sample[4]
    ws.Timepoint = now_string
    assert ws.node.get("Timepoint") == now_string


def test_13_09_get_index(groupfiles_xml):
    o = bioformats.omexml.OMEXML(groupfiles_xml)
    ws = o.plates[0].Well['A02'].Sample[3]
    assert ws.Index == 9


def test_13_10_set_index(groupfiles_xml):
    o = bioformats.omexml.OMEXML(groupfiles_xml)
    ws = o.plates[0].Well['A02'].Sample[3]
    ws.Index = 301
    assert ws.Index == 301


def test_13_11_get_image_ref(groupfiles_xml):
    o = bioformats.omexml.OMEXML(groupfiles_xml)
    ws = o.plates[0].Well['A02'].Sample[3]
    assert ws.ImageRef == "Image:9"
    ref = ws.node.find(bioformats.omexml.qn(o.get_ns("spw"), "ImageRef"))
    ws.node.remove(ref)
    assert ws.ImageRef is None


def test_13_12_set_image_ref(groupfiles_xml):
    o = bioformats.omexml.OMEXML(groupfiles_xml)
    ws = o.plates[0].Well['A02'].Sample[3]
    ws.ImageRef = "Foo"
    assert ws.node.find(bioformats.omexml.qn(o.get_ns("spw"), "ImageRef")).get("ID") == "Foo"


def test_14_01_get_plane_count(tiff_xml):
    o = bioformats.omexml.OMEXML(tiff_xml)
    assert o.image(0).Pixels.plane_count == 1


def test_14_02_set_plane_count():
    o = bioformats.omexml.OMEXML()
    pixels = o.image(0).Pixels
    assert isinstance(pixels, bioformats.omexml.OMEXML.Pixels)
    pixels.plane_count = 2
    assert len(pixels.node.findall(bioformats.omexml.qn(o.get_ns('ome'), "Plane"))) == 2


def test_14_03_get_the_c(tiff_xml):
    o = bioformats.omexml.OMEXML(tiff_xml)
    pixels = o.image(0).Pixels
    assert isinstance(pixels, bioformats.omexml.OMEXML.Pixels)
    plane = pixels.Plane(0)
    assert isinstance(plane, bioformats.omexml.OMEXML.Plane)
    plane.node.set("TheC", "15")
    assert plane.TheC == 15


def test_14_04_get_the_z(tiff_xml):
    o = bioformats.omexml.OMEXML(tiff_xml)
    pixels = o.image(0).Pixels
    assert isinstance(pixels, bioformats.omexml.OMEXML.Pixels)
    plane = pixels.Plane(0)
    assert isinstance(plane, bioformats.omexml.OMEXML.Plane)
    plane.node.set("TheZ", "10")
    assert plane.TheZ == 10


def test_14_05_get_the_t(tiff_xml):
    o = bioformats.omexml.OMEXML(tiff_xml)
    pixels = o.image(0).Pixels
    assert isinstance(pixels, bioformats.omexml.OMEXML.Pixels)
    plane = pixels.Plane(0)
    assert isinstance(plane, bioformats.omexml.OMEXML.Plane)
    plane.node.set("TheT", "9")
    assert plane.TheT == 9


def test_14_06_set_the_c(tiff_xml):
    o = bioformats.omexml.OMEXML(tiff_xml)
    pixels = o.image(0).Pixels
    assert isinstance(pixels, bioformats.omexml.OMEXML.Pixels)
    plane = pixels.Plane(0)
    plane.TheC = 5
    assert int(plane.node.get("TheC")) == 5


def test_14_07_set_the_z(tiff_xml):
    o = bioformats.omexml.OMEXML(tiff_xml)
    pixels = o.image(0).Pixels
    assert isinstance(pixels, bioformats.omexml.OMEXML.Pixels)
    plane = pixels.Plane(0)
    plane.TheZ = 6
    assert int(plane.node.get("TheZ")) == 6


def test_14_08_set_the_t(tiff_xml):
    o = bioformats.omexml.OMEXML(tiff_xml)
    pixels = o.image(0).Pixels
    assert isinstance(pixels, bioformats.omexml.OMEXML.Pixels)
    plane = pixels.Plane(0)
    plane.TheC = 7
    assert int(plane.node.get("TheC")) == 7


def test_14_09_get_delta_t(tiff_xml):
    o = bioformats.omexml.OMEXML(tiff_xml)
    pixels = o.image(0).Pixels
    assert isinstance(pixels, bioformats.omexml.OMEXML.Pixels)
    plane = pixels.Plane(0)
    assert plane.DeltaT == 1.25


def test_14_10_get_exposure_time(tiff_xml):
    o = bioformats.omexml.OMEXML(tiff_xml)
    pixels = o.image(0).Pixels
    assert isinstance(pixels, bioformats.omexml.OMEXML.Pixels)
    plane = pixels.Plane(0)
    assert plane.get_ExposureTime() == 0.25


def test_14_11_get_position_x(tiff_xml):
    o = bioformats.omexml.OMEXML(tiff_xml)
    pixels = o.image(0).Pixels
    assert isinstance(pixels, bioformats.omexml.OMEXML.Pixels)
    plane = pixels.Plane(0)
    assert plane.PositionX == 3.5


def test_14_12_get_position_y(tiff_xml):
    o = bioformats.omexml.OMEXML(tiff_xml)
    pixels = o.image(0).Pixels
    assert isinstance(pixels, bioformats.omexml.OMEXML.Pixels)
    plane = pixels.Plane(0)
    assert plane.PositionY == 4.75


def test_14_13_get_position_z(tiff_xml):
    o = bioformats.omexml.OMEXML(tiff_xml)
    pixels = o.image(0).Pixels
    assert isinstance(pixels, bioformats.omexml.OMEXML.Pixels)
    plane = pixels.Plane(0)
    assert plane.PositionZ == 2.25


def test_14_14_set_delta_t(tiff_xml):
    o = bioformats.omexml.OMEXML(tiff_xml)
    pixels = o.image(0).Pixels
    assert isinstance(pixels, bioformats.omexml.OMEXML.Pixels)
    plane = pixels.Plane(0)
    plane.DeltaT = 1.25
    assert float(plane.node.get("DeltaT")) == 1.25


def test_14_15_set_position_x(tiff_xml):
    o = bioformats.omexml.OMEXML(tiff_xml)
    pixels = o.image(0).Pixels
    assert isinstance(pixels, bioformats.omexml.OMEXML.Pixels)
    plane = pixels.Plane(0)
    plane.PositionX = 5.5
    assert float(plane.node.get("PositionX")) == 5.5


def test_14_16_set_position_y(tiff_xml):
    o = bioformats.omexml.OMEXML(tiff_xml)
    pixels = o.image(0).Pixels
    assert isinstance(pixels, bioformats.omexml.OMEXML.Pixels)
    plane = pixels.Plane(0)
    plane.PositionY = 6.5
    assert float(plane.node.get("PositionY")) == 6.5


def test_14_17_set_position_z(tiff_xml):
    o = bioformats.omexml.OMEXML(tiff_xml)
    pixels = o.image(0).Pixels
    assert isinstance(pixels, bioformats.omexml.OMEXML.Pixels)
    plane = pixels.Plane(0)
    plane.PositionZ = 7.5
    assert float(plane.node.get("PositionZ")) == 7.5
