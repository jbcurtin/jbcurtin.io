#!/usr/bin/env python

import logging
import os
import types
import shutil

from builder import exceptions as builder_exceptions

logger = logging.getLogger(__file__)

ENCODING: str = 'utf-8'
NOTEBOOK_DIR: str = os.path.join(os.getcwd(), 'notebooks')

def validate_notebook_directory_structure(notebook_dir: str) -> None:
    requirements_found: bool = False
    ipynb_found: bool = False
    for root, dirnames, filenames in os.walk(notebook_dir):
        for filename in filenames:
            if filename == 'requirements.txt':
                requirements_found = True

            if filename.endswith('.ipynb'):
                ipynb_found = True
                dirname: str = os.path.basename(notebook_dir)
                notebook_name: str = f'{dirname}.ipynb'
                if not notebook_name == filename:
                    raise builder_exceptions.NotebookFileIssue(f"Notebook Name[{filename}] doesn't match dirname[{dirname}]")

        # only check the current directory
        break

    if requirements_found is False:
        raise builder_exceptions.MissingRequirementsFile(dirname)

    if ipynb_found is False:
        raise builder_exceptions.MissingNotebookFile(dirname)

def generate_build_script(notebook_dir: str) -> types.GeneratorType:
    notebook_name: str = os.path.basename(notebook_dir)
    notebook_html_name: str = f'{notebook_name}.jupyter.html'
    notebook_ipynb_name: str = f'{notebook_name}.ipynb'
    notebook_metadata_name: str = f'{notebook_name}.metadata.json'
    build_path: str = os.path.join(notebook_dir, 'build.sh')
    builder_path: str = os.path.join(os.getcwd(), 'build-tools')
    build_script: str = f"""#!/usr/bin/env bash
set -e

cd {notebook_dir}
# virtualenv -p $(which python3) env
# source env/bin/activate
pip install jupyter

if [ -f "pre_requirements.txt" ]; then
    pip install -r pre_requirements.txt
fi
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

echo 'Converting Notebook to HTML'
python {builder_path}/builder/extract-metadata.py --input {notebook_ipynb_name} --output {notebook_metadata_name}
jupyter nbconvert --stdout --to html {notebook_ipynb_name} > {notebook_html_name}

# Clean up
rm -rf env
cd -
"""
    logger.info(f'Creating Build Script for Notebook[{notebook_name}]')
    with open(build_path, 'w') as stream:
        stream.write(build_script)

logger.info(f'Creating Artifacts for Notebook Dir[{NOTEBOOK_DIR}]')
for root, dirnames, filenames in os.walk(NOTEBOOK_DIR):
    for dirname in dirnames:
        abs_dir_path: str = os.path.join(root, dirname)
        validate_notebook_directory_structure(abs_dir_path)
        generate_build_script(abs_dir_path)

    # only check the current directory
    break

