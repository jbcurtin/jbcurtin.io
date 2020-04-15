#!/usr/bin/env python

import argparse
import json
import os
import typing

def capture_options() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, required=True)
    parser.add_argument('-o', '--output', type=str, required=True)
    return parser.parse_args()

def extract_metadata(options: argparse.Namespace) -> None:
    metadata: typing.Dict[str, typing.Any] = {}
    notebook_filename: str = os.path.basename(options.input)
    with open(options.input) as stream:
        notebook: typing.Dict[str, typing.Any] = json.loads(stream.read())

    for idx, cell in enumerate(notebook['cells']):
        if idx == 0:
            if not cell['cell_type'] in ['markdown']:
                raise builder_exceptions.InvalidNotebook(f"The first cell in every notebook must be a 'markdown' cell. Please fix notebook[{notebook_filename}]")

            metadata['title'] = cell['source'][0].strip('# \n')
            metadata['title-cell'] = cell['source']
            continue

    with open(options.output, 'w') as stream:
        stream.write(json.dumps(metadata, indent=2))

if __name__ in ['__main__']:
    options = capture_options()
    extract_metadata(options)

