#!/usr/bin/env python3
#
#  Copyright (c) 2015 - 2022, Intel Corporation
#  SPDX-License-Identifier: BSD-3-Clause
#

'''
Run Arithmetic Intensity benchmark with the monitor agent.
'''

import argparse

from experiment.monitor import monitor
from experiment import machine
from apps.arithmetic_intensity import arithmetic_intensity

if __name__ == '__main__':

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    monitor.setup_run_args(parser)
    arithmetic_intensity.setup_run_args(parser)
    args, extra_args = parser.parse_known_args()
    mach = machine.init_output_dir(args.output_dir)
    app_conf = arithmetic_intensity.create_appconf(mach, args)
    monitor.launch(app_conf=app_conf, args=args,
                   experiment_cli_args=extra_args)
