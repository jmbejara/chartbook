"""Run or update the project. This file uses the `doit` Python package. It works
like a Makefile, but is Python-based

"""

#######################################
## Configuration and Helpers for PyDoit
#######################################
## Make sure the src folder is in the path
import sys

sys.path.insert(1, "./src/")

from os import environ, getcwd, path
from pathlib import Path

import config
import pipeline_publish
from colorama import Fore, Style, init

## Custom reporter: Print PyDoit Text in Green
# This is helpful because some tasks write to sterr and pollute the output in
# the console. I don't want to mute this output, because this can sometimes
# cause issues when, for example, LaTeX hangs on an error and requires
# presses on the keyboard before continuing. However, I want to be able
# to easily see the task lines printed by PyDoit. I want them to stand out
# from among all the other lines printed to the console.
from doit.reporter import ConsoleReporter

try:
    in_slurm = environ["SLURM_JOB_ID"] is not None
except:
    in_slurm = False


class GreenReporter(ConsoleReporter):
    def write(self, stuff, **kwargs):
        doit_mark = stuff.split(" ")[0].ljust(2)
        task = " ".join(stuff.split(" ")[1:]).strip() + "\n"
        output = (
            Fore.GREEN
            + doit_mark
            + f" {path.basename(getcwd())}: "
            + task
            + Style.RESET_ALL
        )
        self.outstream.write(output)


if not in_slurm:
    DOIT_CONFIG = {
        "reporter": GreenReporter,
        # other config here...
        # "cleanforget": True, # Doit will forget about tasks that have been cleaned.
        'backend': 'sqlite3',
        'dep_file': './.doit-db.sqlite'
    }
else:
    DOIT_CONFIG = {
        'backend': 'sqlite3',
        'dep_file': './.doit-db.sqlite'
    }
init(autoreset=True)


BASE_DIR = Path(config.BASE_DIR)
DATA_DIR = Path(config.DATA_DIR)
MANUAL_DATA_DIR = Path(config.MANUAL_DATA_DIR)
OUTPUT_DIR = Path(config.OUTPUT_DIR)
OS_TYPE = config.OS_TYPE
PUBLISH_DIR = Path(config.PUBLISH_DIR)
USER = config.USER

## Helpers for handling Jupyter Notebook tasks
# fmt: off
## Helper functions for automatic execution of Jupyter notebooks
environ["PYDEVD_DISABLE_FILE_VALIDATION"] = "1"
def jupyter_execute_notebook(notebook):
    return f"jupyter nbconvert --execute --to notebook --ClearMetadataPreprocessor.enabled=True --log-level WARN --inplace ./src/{notebook}.ipynb"
def jupyter_to_html(notebook, output_dir=OUTPUT_DIR):
    return f"jupyter nbconvert --to html --log-level WARN --output-dir={output_dir} ./src/{notebook}.ipynb"
def jupyter_to_md(notebook, output_dir=OUTPUT_DIR):
    """Requires jupytext"""
    return f"jupytext --to markdown --log-level WARN --output-dir={output_dir} ./src/{notebook}.ipynb"
def jupyter_to_python(notebook, build_dir):
    """Convert a notebook to a python script"""
    return f"jupyter nbconvert --log-level WARN --to python ./src/{notebook}.ipynb --output _{notebook}.py --output-dir {build_dir}"
def jupyter_clear_output(notebook):
    return f"jupyter nbconvert --log-level WARN --ClearOutputPreprocessor.enabled=True --ClearMetadataPreprocessor.enabled=True --inplace ./src/{notebook}.ipynb"
# fmt: on


def copy_notebook_to_folder(notebook_stem, origin_folder, destination_folder):
    origin_path = Path(origin_folder) / f"{notebook_stem}.ipynb"
    destination_folder = Path(destination_folder)
    destination_folder.mkdir(parents=True, exist_ok=True)
    destination_path = destination_folder / f"{notebook_stem}.ipynb"
    if OS_TYPE == "nix":
        command = f"cp {origin_path} {destination_path}"
    else:
        command = f"copy  {origin_path} {destination_path}"
    return command


##################################
## Begin rest of PyDoit tasks here
##################################


pipeline_doc_file_deps = pipeline_publish.get_file_deps(base_dir=BASE_DIR)
generated_md_targets = pipeline_publish.get_targets(base_dir=BASE_DIR)
# pipeline_doc_file_deps = []
# generated_md_targets = []


def task_pipeline_publish():
    """Create Pipeline Docs for Use in Sphinx"""

    file_dep = [
        "./docs_src/_templates/chart_entry_bottom.md",
        "./docs_src/_templates/chart_entry_top.md",
        "./docs_src/_templates/dataframe_specs.md",
        "./docs_src/_templates/pipeline_specs.md",
        "./docs_src/charts.md",
        "./docs_src/conf.py",
        "./docs_src/dataframes.md",
        "./docs_src/pipelines.md",
        "./pipeline.json",
        "./README.md",
        "./src/pipeline_publish.py",
        *pipeline_doc_file_deps,
    ]

    targets = [
        # "./_docs/index.md", 
        *generated_md_targets,
    ]

    return {
        "actions": [
            "ipython ./src/pipeline_publish.py",
            "rsync -lr --exclude=charts --exclude=dataframes --exclude=notebooks --exclude=index.md --exclude=pipelines.md --exclude=dataframes.md ./docs_src/ ./_docs/",
            ],
        "targets": targets,
        "file_dep": file_dep,
        "clean": True,
    }


sphinx_targets = [
    "./_docs/_build/html/index.html",
    "./_docs/_build/html/myst_markdown_demos.html",
]


def task_compile_sphinx_docs():
    """Compile Sphinx Docs"""

    file_dep = [
        "./docs_src/conf.py",
        "./docs_src/contributing.md",
        "./docs_src/index.md",
        "./docs_src/myst_markdown_demos.md",
        # Pipeline docs
        "./docs_src/_templates/chart_entry_bottom.md",
        "./docs_src/_templates/chart_entry_top.md",
        "./docs_src/_templates/dataframe_specs.md",
        "./docs_src/_templates/pipeline_specs.md",
        "./docs_src/charts.md",
        "./docs_src/dataframes.md",
        "./docs_src/pipelines.md",
        "./pipeline.json",
        "./README.md",
        "./src/pipeline_publish.py",
    ]
    return {
        "actions": [
            "sphinx-build -M html ./_docs/ ./_docs/_build",
        ],  # Use docs as build destination
        # "actions": ["sphinx-build -M html ./docs/ ./docs/_build"], # Previous standard organization
        "targets": sphinx_targets,
        "file_dep": file_dep,
        "task_dep": [
            "pipeline_publish",
        ],
        "clean": True,
    }
