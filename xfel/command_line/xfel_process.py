#!/usr/bin/env python
#
# LIBTBX_SET_DISPATCHER_NAME cctbx.xfel.process

from __future__ import division

help_message = '''

See dials.stills_process.

'''

from libtbx.phil import parse
control_phil_str = '''
  input {
    trial = None
      .type = int
      .help = Optional. Trial number for this run.
    rungroup = None
      .type = int
      .help = Optional. Useful for organizing runs with similar parameters into logical \
              groupings.
   }
'''

delete_shoeboxes_override_str = '''
  integration {
    debug {
      delete_shoeboxes = True
        .type = bool
        .help = "Delete shoeboxes immediately before saving files. This option"
                "in combination with debug.output=True enables intermediate"
                "processing steps to make use of shoeboxes."
    }
  }
'''

radial_average_phil_str = '''
  radial_average {
    enable = False
      .type = bool
      .help = If True, perform a radial average on each image
    two_theta_low = None
      .type = float
      .help = If not None and database logging is enabled, for each image \
              compute the radial average at this two theta position and log \
              it in the database
    two_theta_high = None
      .type = float
      .help = If not None and database logging is enabled, for each image \
              compute the radial average at this two theta position and log \
              it in the database
    include scope dxtbx.command_line.radial_average.master_phil
  }
'''

import dials.command_line.stills_process
from xfel.ui.db.frame_logging import DialsProcessorWithLogging
dials.command_line.stills_process.Processor = DialsProcessorWithLogging

from dials.command_line.stills_process import dials_phil_str, program_defaults_phil_str, Script as DialsScript, control_phil_str as dials_control_phil_str
from xfel.ui import db_phil_str

phil_scope = parse(dials_control_phil_str + control_phil_str + dials_phil_str + db_phil_str + radial_average_phil_str, process_includes=True).fetch(parse(program_defaults_phil_str))
phil_scope = phil_scope.fetch(parse(delete_shoeboxes_override_str))

class Script(DialsScript):
  '''A class for running the script.'''
  def __init__(self):
    '''Initialise the script.'''
    from dials.util.options import OptionParser
    import libtbx.load_env

    # The script usage
    usage = "usage: %s [options] [param.phil] filenames" % libtbx.env.dispatcher_name

    self.tag = None
    self.reference_detector = None

    # Create the parser
    self.parser = OptionParser(
      usage=usage,
      phil=phil_scope,
      epilog=help_message
      )

if __name__ == '__main__':
  from dials.util import halraiser
  try:
    script = Script()
    script.run()
  except Exception as e:
    halraiser(e)
