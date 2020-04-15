#!/usr/bin/env python

import logging
import os
import shutil
import sys
import typing

from builder import exceptions as builder_exceptions

logger = logging.getLogger(__file__)

ENCODING: str = 'utf-8'
NOTEBOOK_DIR: str = os.path.join(os.getcwd(), 'notebooks')
RENDERED_NOTEBOOKS_DIR: str = os.path.join(os.getcwd(), 'artifact/notebooks')
if os.path.exists(RENDERED_NOTEBOOKS_DIR):
    shutil.rmtree(RENDERED_NOTEBOOKS_DIR)

os.makedirs(RENDERED_NOTEBOOKS_DIR)

def find_html_file(notebook_dir: str) -> str:
    for root, dirnames, filenames in os.walk(notebook_dir):
        for filename in filenames:
            notebook_name: str = os.path.basename(notebook_dir)
            html_filename = f'{notebook_name}.jupyter.html'
            metadata_filename: str = f'{notebook_name}.metadata.json'
            if html_filename == filename:
                return os.path.join(root, metadata_filename), os.path.join(root, filename)

        # only check the current directory
        break

    raise builder_exceptions.MissingHTMLFile(f'Notebook Dir[{notebook_dir}]')

logger.info(f'Scanning Notebooks[{NOTEBOOK_DIR}] for Rendered Notebooks')
for root, dirnames, filenames in os.walk(NOTEBOOK_DIR):
    for dirname in dirnames:
        abs_dir_path: str = os.path.join(root, dirname)
        metadata_filepath, html_filepath = find_html_file(abs_dir_path)
        html_filename: str = os.path.basename(html_filepath)
        metadata_filename: str = os.path.basename(metadata_filepath)
        notebooks_html_path: str = os.path.join(RENDERED_NOTEBOOKS_DIR, html_filename)
        notebooks_metadata_path: str = os.path.join(RENDERED_NOTEBOOKS_DIR, metadata_filename)
        logger.info(f'Moving File[{html_filename}] to Rendered Notebooks Directory[{RENDERED_NOTEBOOKS_DIR}]')
        shutil.move(html_filepath, notebooks_html_path)
        shutil.move(metadata_filepath, notebooks_metadata_path)

    # only check the current directory
    break

