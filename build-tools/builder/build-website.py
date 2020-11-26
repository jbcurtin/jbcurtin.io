#!/usr/bin/env python

import bs4
import collections
import logging
import git
import os
import jinja2
import json
import markdown
import shutil
import sys
import toml
import types
import typing

from builder import exceptions as builder_exceptions
from datetime import datetime
from jinja2.environment import Template, Environment

logger = logging.getLogger(__file__)

ENCODING: str = 'utf-8'

# Input
GIT_REPO_ROOT: str = os.getcwd()
NOTEBOOK_DIR: str = os.path.join(os.getcwd(), 'notebooks')
RENDERED_NOTEBOOKS_DIR: str = os.path.join(os.getcwd(), 'artifact/notebooks')
TEMPLATE_DIR: str = os.path.join(os.getcwd(), 'template')
ASSETS_DIR: str = os.path.join(os.getcwd(), 'assets')
ENVIRONMENT_PATH: str = os.path.join(f'{TEMPLATE_DIR}/environment.toml')

# Output
WEBSITE_ARTIFACT_DIR: str = os.path.join(os.getcwd(), 'artifact')
WEBSITE_ARTIFACT_STATIC_DIR: str = f'{WEBSITE_ARTIFACT_DIR}/static'

Notebook = collections.namedtuple('Notebook', [
  'jupyter_filepath', 'filepath', 'ipynb_filepath',
  'relative_path', 'metadata'])

def _add_jinja2_filters(environment: Environment) -> None:
    def _render_human_datetime(datetime: datetime) -> str:
        return datetime.strftime('%A, %d. %B %Y %I:%M%p')

    def _render_machine_datetime(datetime: datetime) -> str:
        return datetime.strftime('%Y-%m-%d')

    def _render_machine_datetime_with_time(datetime: datetime) -> str:
        return datetime.strftime('%Y-%m-%dT%H-%M-%S')

    environment.filters['human_date'] = _render_human_datetime
    environment.filters['machine_date'] = _render_machine_datetime
    environment.filters['machine_date_with_time'] = _render_machine_datetime_with_time

def load_environment() -> typing.Dict[str, typing.Any]:
    environment: typing.Dict[str, typing.Any]
    with open(ENVIRONMENT_PATH, 'r') as stream:
        environment = toml.loads(stream.read())

    environment['today'] = datetime.utcnow()
    return environment

def _enhance_notebook_metadata(notebook: Notebook) -> None:
    notebook.metadata['title-cell-html'] = _parse_markdown_title_cell_to_html(notebook)
    notebook.metadata['title-cell-atom'] = _parse_markdown_title_cell_to_atom(notebook)

    # Extract Publish Date
    try:
        git_repo: git.Repo = git.Repo(GIT_REPO_ROOT)
    except git.exc.InvalidGitRepositoryError:
        raise builder_exceptions.Error(f'Unable to create git reference[{GIT_REPO_ROOT}]')

    try:
        commits: typing.List[git.Commit] = [commit for commit in git_repo.iter_commits(paths=[notebook.ipynb_filepath])]
        first_commit: git.Commit = commits[0]
        last_commit: git.Commit = commits[-1]

    except IndexError:
        first_commit = None
        notebook.metadata['publish_date'] = None
        notebook.metadata['updated_date'] = None

    else:
        notebook.metadata['publish_date'] = first_commit.authored_datetime
        notebook.metadata['updated_date'] = last_commit.authored_datetime

    # Render jupyter HTML
    with open(notebook.jupyter_filepath, 'r') as jupyter_html:
        notebook.metadata['jupyter_html'] = _parse_jupyter_html_to_bulma_document(jupyter_html.read())


def find_notebooks() -> types.GeneratorType:
    for root, dirnames, filenames in os.walk(RENDERED_NOTEBOOKS_DIR):
        for filename in filenames:
            if filename.endswith('.jupyter.html'):
                filename_without_ext: str = filename.split('.', 1)[0]
                filename_final: str = f'{filename_without_ext}.html'
                metadata_filename: str = f'{filename_without_ext}.metadata.json'
                metadata_filepath: str = f'{root}/{metadata_filename}'
                notebook_filepath: str = f'{NOTEBOOK_DIR}/{filename_without_ext}/{filename_without_ext}.ipynb'
                with open(metadata_filepath, 'r') as stream:
                    notebook = Notebook(
                        os.path.join(root, filename),
                        os.path.join(root, filename_final),
                        notebook_filepath,
                        f'notebooks/{filename_final}',
                        json.loads(stream.read()))

                    _enhance_notebook_metadata(notebook)
                    yield notebook

        # only check the current directory
        break


def build_index_page(notebooks: typing.List[Notebook]) -> None:
    environment: Environment = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR), undefined=jinja2.StrictUndefined)
    _add_jinja2_filters(environment)

    index: Template = environment.get_template('index.html')
    template_context: typing.Dict[str, typing.Any] = {
        'environment': load_environment(),
        'static_url': 'static/',
        'notebook': notebooks[-1]
    }
    if not os.path.exists(WEBSITE_ARTIFACT_DIR):
        os.makedirs(WEBSITE_ARTIFACT_DIR)

    try:
        with open(f'{WEBSITE_ARTIFACT_DIR}/index.html', 'w') as stream:
            stream.write(index.render(**template_context))

    except jinja2.exceptions.UndefinedError as err:
        varname: str = err.args[0].rsplit("'", 2)[1]
        raise builder_exceptions.EnvironmentVarName(f'Environment missing VarName[{varname}]')

def build_about_page(notebooks: typing.List[Notebook]) -> None:
    environment = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR), undefined=jinja2.StrictUndefined)
    _add_jinja2_filters(environment)

    about: Template = environment.get_template('about.html')
    template_context = {
        'environment': load_environment(),
        'static_url': 'static/',
    }

    try:
        with open(f'{WEBSITE_ARTIFACT_DIR}/about.html', 'w') as stream:
            stream.write(about.render(**template_context))

    except jinja2.exceptions.UndefinedError as err:
        varname: str = err.args[0].rsplit("'", 2)[1]
        raise builder_exceptions.EnvironmentVarName(f'Environment missing VarName[{varname}]')

def _parse_markdown_html_to_bulma_html(html_lines: typing.List[str], notebook: Notebook) -> str:
    rendered: typing.List[str] = []
    for html_line in html_lines:
        if html_line == '':
            continue

        if html_line.startswith('<h1>'):
            title = bs4.BeautifulSoup(html_line, 'lxml').find('h1')
            title['class'] = 'title'
            anchor: str = f'<a href="{notebook.relative_path}"> {title.extract()} </a>'
            rendered.append(anchor)

        elif html_line.startswith('<h2>'):
            subtitle = bs4.BeautifulSoup(html_line, 'lxml').find('h2')
            subtitle['class'] = 'subtitle'
            rendered.append(str(subtitle.extract()))

        elif html_line.startswith('<p>'):
            rendered.append(html_line)

        elif html_line.startswith('<ul>'):
            rendered.append(html_line)

        elif html_line.startswith('<pre>'):
            rendered.append(html_line)

        elif html_line.startswith('<code>'):
            rendered.append(html_line)

        else:
            raise NotImplementedError(html_line)

    return ''.join(rendered)

def __regroup_markdown_lines(notebook: Notebook) -> str:
    # Regroup common markdown objects together
    line_groups: typing.List[str] = []
    merged_lines: typing.List[str] = []
    for line in notebook.metadata['title-cell']:
        if line.strip().startswith('*'):
            line_groups.append(line)

        elif len(line_groups) > 0:
            merged_lines.append(''.join(line_groups))
            line_groups = []

        else:
            merged_lines.append(line)

    return merged_lines


def _parse_markdown_title_cell_to_html(notebook: typing.List[str]) -> str:
    rendered_markdown_html: typing.List[str] = []
    for merged_line in __regroup_markdown_lines(notebook):
        rendered_markdown_html.append(markdown.markdown(merged_line, extensions=['attr_list']))

    return _parse_markdown_html_to_bulma_html(rendered_markdown_html, notebook)

def _parse_markdown_title_cell_to_atom(notebook: Notebook) -> str:
    rendered_markdown_atom: typing.List[str] = []
    for merged_line in __regroup_markdown_lines(notebook):
        rendered_markdown_atom.append(merged_line.strip('# *\n'))

    return '\n'.join(rendered_markdown_atom)

# typing.List[typing.Dict[str, typing.Any]]) -> None:
def build_recently_published_notebooks(notebooks: typing.List[Notebook]) -> None:
    environment: Environment = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR), undefined=jinja2.StrictUndefined)
    _add_jinja2_filters(environment)

    recently_published_notebooks: Template = environment.get_template('recently-published-notebooks.html')
    template_context: typing.Dict[str, typing.Any] = {
        'environment': load_environment(),
        'static_url': 'static/',
        'notebooks': [_parse_markdown_title_cell_to_html(notebook) for notebook in reversed(notebooks)],
    }
    if not os.path.exists(WEBSITE_ARTIFACT_DIR):
        os.makedirs(WEBSITE_ARTIFACT_DIR)

    try:
        with open(f'{WEBSITE_ARTIFACT_DIR}/recently-published-notebooks.html', 'w') as stream:
            stream.write(recently_published_notebooks.render(**template_context))

    except jinja2.exceptions.UndefinedError as err:
        varname: str = err.args[0].rsplite("'", 2)[1]
        raise builder_exceptions.EnvironmentVarName(f'Environment missing VarName[{varname}]')


def build_asset_dir(initial_directory: str, target_directory: str) -> None:
    for root, dirnames, filenames in os.walk(initial_directory):
        for dirname in dirnames:
            build_asset_dir(f'{initial_directory}/{dirname}', f'{target_directory}/{dirname}')

        for filename in filenames:
            target_filepath = os.path.join(target_directory, filename)
            source_filepath = os.path.join(initial_directory, filename)
            if any([
                filename.endswith('.png'),
                filename.endswith('.jpg'),
                filename.endswith('.jpeg'),
                filename.endswith('.svg'),
                filename.endswith('.gif')]):
                logger.info(f'Moving File[{filename}] to Asset Dir[{initial_directory}]')
                with open(target_filepath, 'wb') as target_stream:
                    with open(source_filepath, 'rb') as source_stream:
                        target_stream.write(source_stream.read())
            else:
                raise NotImplementedError(filename)
        break

def build_static_pages(initial_directory: str, target_directory:str) -> None:
    if os.path.exists(target_directory):
        shutil.rmtree(target_directory)

    os.makedirs(target_directory)
    environment: Environment = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR), undefined=jinja2.StrictUndefined)
    template_context: typing.Dict[str, typing.Any] = {
        'environment': load_environment(),
        'static_url': '/static/',
    }
    for root, dirnames, filenames in os.walk(initial_directory):
        for dirname in dirnames:
            if dirname in ['css', 'images', 'js']:
                build_static_pages(f'{initial_directory}/{dirname}', f'{target_directory}/{dirname}')

        for filename in filenames:
            target_filepath: str = os.path.join(target_directory, filename)
            source_filepath: str = os.path.join(initial_directory, filename)
            if filename.endswith('css'):
                logger.info(f'Building File[{filename}]')
                # Compress CSS
                with open(target_filepath, 'wb') as target_stream:
                    with open(source_filepath, 'rb') as source_stream:
                        css_template: Template = environment.from_string(source_stream.read().decode(ENCODING))
                        target_stream.write(css_template.render(**template_context).encode(ENCODING))

            elif filename.endswith('.js'):
                logger.info(f'Building File[{filename}]')
                # Compress JS
                with open(target_filepath, 'w') as target_stream:
                    with open(source_filepath, 'r') as source_stream:
                        target_stream.write(source_stream.read())


            elif any([
                filename.endswith('.html'),
                filename == 'environment.toml',
                filename.endswith('.swp'),
                filename == 'rss.xml',
                filename == 'atom.xml',
                filename == 'robots',
                filename == 'robots.txt',
                filename == 'sitemap.xml']):
                continue

            else:
                raise NotImplementedError(filename)
        break

def _parse_jupyter_html_to_bulma_document(html: str) -> str:
    soup = bs4.BeautifulSoup(html, 'lxml')
    styles: typing.List[str] = []
    for idx, tag in enumerate(soup.findAll()):
        if tag.name in ['style']:
            styles.extend([child for child in tag.children])

        if tag.name in ['html', 'body', 'script', 'head', 'title', 'link', 'meta']:
            continue

        GRID: typing.List[str] = ['column', 'is-11']#'is-offset-1']
        # print(tag.name, tag.attrs)
        if tag.name in ['div']:
            if tag.attrs.get('id', None) == 'notebook':
                continue

            elif tag.attrs.get('id', None) == 'notebook-container':
                continue

            elif tag.attrs.get('class', [None])[0] == 'cell':
                tag.attrs['class'] = GRID
                continue

            # Markdown Cell
            elif all([
                tag.attrs.get('class', [None])[0] == 'prompt',
                tag.parent.attrs.get('class', []) == GRID]):
                tag.attrs['class'] = ['jupyter-markdown-prompt']
                tag.extract()
                continue

            elif all([
                tag.attrs.get('class', [None])[0] == 'inner_cell',
                tag.parent.attrs.get('class', None) == GRID]):
                tag.attrs['class'] = ['jupyter-markdown-inner-cell']
                continue

            elif all([
                tag.attrs.get('class', [None])[0] == 'text_cell_render',
                tag.parent.attrs.get('class', None) == ['jupyter-markdown-inner-cell']]):
                tag.attrs['class'] = ['jupyter-markdown-text-cell']
                continue

            # Source Code Cell
            ## Input Part
            elif all([
                    tag.attrs.get('class', [None])[0] == 'input',
                    tag.parent.attrs.get('class', '') == GRID]):
                tag.attrs['class'] = ['jupyter-input']
                continue

            elif all([
                    tag.attrs.get('class', [None])[0] == 'prompt',
                    tag.parent.attrs.get('class', None) == ['jupyter-input']]):
                tag.attrs['class'] = ['jupyter-prompt']
                continue

            elif all([
                    tag.attrs.get('class', [None])[0] == 'inner_cell',
                    tag.parent.attrs.get('class', None) == ['jupyter-input']]):
                tag.attrs['class'] = ['jupyter-inner-cell']
                continue

            ## Output Part
            elif all([
                    tag.attrs.get('class', [None])[0] == 'output_wrapper',
                    tag.parent.attrs.get('class', None) == GRID]):
                tag.attrs['class'] = ['jupyter-output']
                continue

            elif all([
                    tag.attrs.get('class', [None])[0] == 'output',
                    tag.parent.attrs.get('class', None) == ['jupyter-output']]):
                tag.attrs['class'] = ['jupyter-output']
                continue

            elif all([
                    tag.attrs.get('class', [None])[0] == 'output_area',
                    tag.parent.attrs.get('class', None) == ['jupyter-output']]):
                tag.attrs['class'] = ['jupyter-output-area']
                continue

            elif all([
                    tag.attrs.get('class', [None])[0] == 'prompt',
                    tag.parent.attrs.get('class', None) == ['jupyter-output-area']]):
                tag.attrs['class'] = ['jupyter-output-prompt']
                continue

            elif all([
                    tag.attrs.get('class', [None])[0] == 'output_text',
                    tag.parent.attrs.get('class', None) == ['jupyter-output-area']]):
                tag.attrs['class'] = ['jupyter-output-text']
                continue

            else:
                # import pdb; pdb.set_trace()
                pass


        elif all([
            tag.name == 'h1',
            not tag.attrs.get('id', None) is None,
            tag.attrs.get('class', None) is None]):
            tag['class'] = 'title'
            tag.extract()

        elif all([
            tag.name == 'h2',
            not tag.attrs.get('id', None) is None,
            tag.attrs.get('class', None) is None]):
            tag['class'] = 'subtitle'

        elif all([
            tag.name == 'a',
            tag.attrs.get('id', None) is None,
            tag.attrs.get('class', [None])[0] == 'anchor-link',
            tag.attrs.get('href', '').startswith('#')]):
            continue

        elif all([
            tag.name == 'a',
            (
              tag.attrs.get('href', '').startswith('/') or 
              tag.attrs.get('href', '').startswith('http'))]):
            tag.attrs['target'] = '_blank'
            continue

        elif all([
            tag.name == 'p',
            tag.attrs.get('class', None) is None,
            tag.attrs.get('id', None) is None]):
            continue

        elif all([
            tag.name == 'code',
            tag.attrs.get('class', None) is None,
            tag.attrs.get('id', None) is None]):
            continue

        else:
            # import pdb; pdb.set_trace()
            pass

    return {
        'styles': styles,
        'document': ''.join([
            str(child) for child in soup.find('body').children if child
        ])
    }


def rebuild_rendered_notebooks(notebooks: typing.List[Notebook]) -> None:
    environment: Environment = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR), undefined=jinja2.StrictUndefined)
    _add_jinja2_filters(environment)

    notebook_template: Template = environment.get_template('notebook.html')
    for notebook in notebooks:
        template_context: typing.Dict[str, typing.Any] = {
            'environment': load_environment(),
            'static_url': '../static/',
            'notebook': notebook,
        }
        with open(notebook.filepath, 'w') as stream:
            stream.write(notebook_template.render(**template_context))

def build_sitemap(notebooks: typing.List[Notebook]) -> None:
    environment: Environment = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR), undefined=jinja2.StrictUndefined)
    _add_jinja2_filters(environment)

    sitemap_template: Template = environment.get_template('sitemap.xml')
    sitemap_filepath: str = os.path.join(WEBSITE_ARTIFACT_DIR, 'sitemap.xml')
    template_context: typing.Dict[str, typing.Any] = {
        'environment': load_environment(),
        'static_url': 'static/',
        'notebooks': notebooks,
    }
    with open(sitemap_filepath, 'w') as sitemap_stream:
        sitemap_stream.write(sitemap_template.render(**template_context))

def build_rss_feed(notebooks: typing.List[Notebook]) -> None:
    environment: Environment = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR), undefined=jinja2.StrictUndefined)
    _add_jinja2_filters(environment)

    rss_template: Template = environment.get_template('rss.xml')
    rss_filepath: str = os.path.join(WEBSITE_ARTIFACT_DIR, 'rss.xml')
    template_context: typing.Dict[str, typing.Any] = {
        'environment': load_environment(),
        'static_url': 'static/',
        'notebooks': notebooks,
    }
    with open(rss_filepath, 'w') as rss_stream:
        rss_stream.write(rss_template.render(**template_context))

def build_atom_feed(notebooks: typing.List[Notebook]) -> None:
    environment: Environment = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR), undefined=jinja2.StrictUndefined)
    _add_jinja2_filters(environment)

    atom_template: Template = environment.get_template('atom.xml')
    atom_filepath: str = os.path.join(WEBSITE_ARTIFACT_DIR, 'atom.xml')
    template_context: typing.Dict[str, typing.Any] = {
        'environment': load_environment(),
        'static_url': 'static/',
        'notebooks': notebooks
    }
    with open(atom_filepath, 'w') as atom_stream:
        atom_stream.write(atom_template.render(**template_context))

def build_robots(notebooks: typing.List[str]) -> None:
    environment: Environment = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR), undefined=jinja2.StrictUndefined)
    _add_jinja2_filters(environment)

    robots_template: Template = environment.get_template('robots.txt')
    robots_filepath: str = os.path.join(WEBSITE_ARTIFACT_DIR, 'robots')
    robots_filepath_two: str = os.path.join(WEBSITE_ARTIFACT_DIR, 'robots.txt')
    template_context: typing.Dict[str, typing.Any] = {
        'environment': load_environment(),
        'static_url': 'static/',
        'notebooks': notebooks
    }
    with open(robots_filepath, 'w') as robots_stream:
        robots_stream.write(robots_template.render(**template_context))

    shutil.copyfile(robots_filepath, robots_filepath_two)

logger.info(f'Scanning HTML files from Rendered Notebook Directory[{RENDERED_NOTEBOOKS_DIR}]')
notebooks: typing.List[typing.Dict[str, str]] = []
for notebook in find_notebooks():
    notebooks.append(notebook)

# Sort Notebooks, most recent being first
if os.environ.get('BUILDER_RUNNING', '').lower() in ['t', 'true']:
    notebooks = sorted(notebooks, key=lambda x: x.metadata['publish_date'], reverse=True)

else:
    notebooks = sorted(notebooks, key=lambda x: x.metadata['publish_date'], reverse=False)

build_recently_published_notebooks(notebooks)
rebuild_rendered_notebooks(notebooks)
build_index_page(notebooks)
build_about_page(notebooks)
build_sitemap(notebooks)
build_rss_feed(notebooks)
build_atom_feed(notebooks)
build_robots(notebooks)
build_static_pages(TEMPLATE_DIR, WEBSITE_ARTIFACT_STATIC_DIR)
build_asset_dir(ASSETS_DIR, WEBSITE_ARTIFACT_STATIC_DIR)
