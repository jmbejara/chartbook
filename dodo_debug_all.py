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


def task_doit_pipeline_template():
    """Run pipeline"""

    return {
        "actions": ["doit -f ../blank_project/dodo.py"],
        "targets": [],
        "verbosity": 2,  # Print everything immediately. This is important in
        # case WRDS asks for credentials.
    }


def task_doit_COIN():
    """Run pipeline"""

    return {
        "actions": ["doit -f ../COIN/dodo.py"],
        "targets": [],
        "verbosity": 2,  # Print everything immediately. This is important in
        # case WRDS asks for credentials.
    }


def task_doit_chart_book():
    """Render ChartBook pages"""

    return {
        "actions": ["doit -f dodo.py"],
        "targets": [],
        "verbosity": 2,  # Print everything immediately. This is important in
        # case WRDS asks for credentials.
        "task_dep": [
            "doit_pipeline_template",
            "doit_COIN",
        ]
    }

