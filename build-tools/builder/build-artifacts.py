#!/usr/bin/env python

import logging
import os
import subprocess
import sys
import time
import typing

from builder import exceptions as builder_exceptions

logger = logging.getLogger(__file__)

ENCODING: str = 'utf-8'
NOTEBOOK_DIR: str = os.path.join(os.getcwd(), 'notebooks')

def find_build_script(notebook_dir: str) -> None:
    for root, dirnames, filenames in os.walk(notebook_dir):
        for filename in filenames:
            if filename == 'build.sh':
                return os.path.join(root, filename)

        # only check the current directory
        break

    raise builder_exceptions.MissingBuildScript(f'Notebook Dir[{notebook_dir}]')

def run_command(cmd: typing.Union[str, typing.List[str]]) -> None:
    if isinstance(cmd, str):
        cmd = [cmd]

    proc = subprocess.Popen(cmd, shell=True)
    while proc.poll() is None:
        time.sleep(.1)

    if proc.poll() > 0:
        raise Exception(proc.stderr.read().decode(ENCODING))

logger.info(f'Scanning Notebooks[{NOTEBOOK_DIR}] for build scripts')
for root, dirnames, filenames in os.walk(NOTEBOOK_DIR):
    for dirname in dirnames:
        abs_dir_path: str = os.path.join(root, dirname)
        build_script_path = find_build_script(abs_dir_path)
        logger.info(f'Running build for Notebook[{dirname}]')
        run_command(f'bash {build_script_path}')
        os.remove(build_script_path)

    # only check the current directory
    break

