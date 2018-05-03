from __future__ import absolute_import, division, print_function

import glob
import os

from libtbx import easy_run

from dxtbx.serialize import dump
from dxtbx.imageset import ImageSetFactory

def test_to_xds(dials_regression, tmpdir):
  tmpdir.chdir()

  template = os.path.join(dials_regression, 'centroid_test_data', "centroid_*.cbf")
  file_names = glob.glob(template)

  expected_output = """\
DETECTOR=PILATUS MINIMUM_VALID_PIXEL_VALUE=0 OVERLOAD=495976
SENSOR_THICKNESS= 0.320
DIRECTION_OF_DETECTOR_X-AXIS= 1.00000 0.00000 0.00000
DIRECTION_OF_DETECTOR_Y-AXIS= 0.00000 1.00000 0.00000
NX=2463 NY=2527 QX=0.1720 QY=0.1720
DETECTOR_DISTANCE= 190.180
ORGX= 1235.84 ORGY= 1279.58
ROTATION_AXIS= 1.00000 0.00000 0.00000
STARTING_ANGLE= 0.000
OSCILLATION_RANGE= 0.200
X-RAY_WAVELENGTH= 0.97950
INCIDENT_BEAM_DIRECTION= -0.000 -0.000 1.021
FRACTION_OF_POLARIZATION= 0.999
POLARIZATION_PLANE_NORMAL= 0.000 1.000 0.000
NAME_TEMPLATE_OF_DATA_FRAMES= %s
TRUSTED_REGION= 0.0 1.41
UNTRUSTED_RECTANGLE= 487 495 0 2528
UNTRUSTED_RECTANGLE= 981 989 0 2528
UNTRUSTED_RECTANGLE= 1475 1483 0 2528
UNTRUSTED_RECTANGLE= 1969 1977 0 2528
UNTRUSTED_RECTANGLE= 0 2464 195 213
UNTRUSTED_RECTANGLE= 0 2464 407 425
UNTRUSTED_RECTANGLE= 0 2464 619 637
UNTRUSTED_RECTANGLE= 0 2464 831 849
UNTRUSTED_RECTANGLE= 0 2464 1043 1061
UNTRUSTED_RECTANGLE= 0 2464 1255 1273
UNTRUSTED_RECTANGLE= 0 2464 1467 1485
UNTRUSTED_RECTANGLE= 0 2464 1679 1697
UNTRUSTED_RECTANGLE= 0 2464 1891 1909
UNTRUSTED_RECTANGLE= 0 2464 2103 2121
UNTRUSTED_RECTANGLE= 0 2464 2315 2333
DATA_RANGE= 1 9
JOB=XYCORR INIT COLSPOT IDXREF DEFPIX INTEGRATE CORRECT\
""" %(template.replace("*", "????"))

  cmd = " ".join(["dxtbx.to_xds"] + file_names)
  result = easy_run.fully_buffered(cmd)
  # allow extra lines to have been added (these may be comments)
  for record in expected_output.split('\n'):
    assert record.strip() in "\n".join(result.stdout_lines), record

  # now test reading from a json file
  sweep = ImageSetFactory.new(file_names)[0]
  with open("sweep.json", mode="wb") as fh:
    dump.imageset(sweep, fh)
  cmd = " ".join(["dxtbx.to_xds", "sweep.json"])
  print(cmd)
  result = easy_run.fully_buffered(cmd)

  # allow extra lines to have been added (these may be comments)
  for record in expected_output.split('\n'):
    assert record.strip() in "\n".join(result.stdout_lines), record
