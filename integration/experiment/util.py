#
#  Copyright (c) 2015 - 2022, Intel Corporation
#  SPDX-License-Identifier: BSD-3-Clause
#

# Helper functions useful for both tests and experiments

import sys
import os
import socket
import subprocess
import io
import yaml
import shlex

import geopmpy.launcher


def detect_launcher():
    """
    Heuristic to determine the resource manager used on the system.
    Returns name of resource manager or launcher, otherwise a
    LookupError is raised.
    """
    # Try the environment
    result = os.environ.get('GEOPM_LAUNCHER', None)
    if not result:
        # Check for known host names
        slurm_hosts = ['mr-fusion', 'mcfly']
        alps_hosts = ['theta']
        hostname = socket.gethostname()
        if any(hostname.startswith(word) for word in slurm_hosts):
            result = 'srun'
        elif any(hostname.startswith(word) for word in alps_hosts):
            result = 'aprun'
    if not result:
        try:
            exec_str = 'srun --version'
            subprocess.check_call(exec_str, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, shell=True)
            result = 'srun'
        except subprocess.CalledProcessError:
            pass
    if not result:
        try:
            exec_str = 'aprun --version'
            subprocess.check_call(exec_str, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, shell=True)
            result = 'aprun'
        except subprocess.CalledProcessError:
            pass
    if not result:
        raise LookupError('Unable to determine resource manager')
    return result


def allocation_node_test(test_exec, stdout, stderr):
    argv = shlex.split(test_exec)
    launcher = detect_launcher()
    argv.insert(1, launcher)
    if launcher == 'aprun':
        argv.insert(2, '-q')  # Use quiet flag with aprun to suppress end of job info string
    argv.insert(2, '--geopm-ctl-disable')
    launcher = geopmpy.launcher.Factory().create(argv, num_rank=1, num_node=1,
                                                 job_name="geopm_allocation_test", quiet=True)
    launcher.run(stdout, stderr)


def geopmwrite(write_str):
    test_exec = "dummy -- geopmwrite " + write_str
    stdout = io.StringIO()
    stderr = io.StringIO()
    try:
        allocation_node_test(test_exec, stdout, stderr)
    except subprocess.CalledProcessError as err:
        sys.stderr.write(stderr.getvalue())
        raise err
    output = stdout.getvalue().splitlines()
    last_line = None
    if len(output) > 0:
        last_line = output[-1]
    return last_line


def geopmread(read_str):
    test_exec = "dummy -- geopmread " + read_str
    stdout = io.StringIO()
    stderr = io.StringIO()
    try:
        allocation_node_test(test_exec, stdout, stderr)
    except subprocess.CalledProcessError as err:
        sys.stderr.write(stderr.getvalue())
        raise err
    output = stdout.getvalue()
    last_line = output.splitlines()[-1]

    if last_line.startswith('0x'):
        result = int(last_line)
    else:
        try:
            result = float(last_line)
        except ValueError:
            result = list(yaml.safe_load(output).values())[0]
    return result


def geopmread_domain():
    test_exec = "dummy -- geopmread -d"
    stdout = io.StringIO()
    stderr = io.StringIO()
    try:
        allocation_node_test(test_exec, stdout, stderr)
    except subprocess.CalledProcessError as err:
        sys.stderr.write(stderr.getvalue())
        raise err
    output = stdout.getvalue()
    result = {}
    for line in output.strip().split('\n'):
        domain, count = tuple(line.split())
        result[domain] = int(count)
    return result


def get_node_memory_info():
    test_exec = 'dummy -- cat /proc/meminfo'
    stdout = io.StringIO()
    stderr = io.StringIO()
    try:
        allocation_node_test(test_exec, stdout, stderr)
    except subprocess.CalledProcessError as err:
        sys.stderr.write(stderr.getvalue())
        raise err
    output = stdout.getvalue()
    result = {}
    for line in output.strip().split('\n'):
        if 'MemTotal' in line:
            key, total, units = tuple(line.split())
            if units != 'kB':
                raise RuntimeError("Unknown how to convert units: {}".format(units))
            # Convert to bytes.  Note: in spite of 'kB' label, meminfo
            # displays kibibytes
            result['MemTotal'] = float(total) * 1024
            break
    return result
