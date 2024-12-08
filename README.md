RAC Chart Base
==============

## TODO

Jeremy

  - Read the last available data date (by finding the last non-missing value in each parquet file) and print in dataframe specs
  - Read the last data update date (by finding the date modified of the parquet file) and print in the data frame specs
  - Code to inject data in Excel sheets (from Windows)
  - how to set up auto-runner when I don't have permission to all datasets? Federated running? Caleb Wesley?

Ashlyn

  - ME: review powerpoint slides from ashlyn for template instructions
  - When done, convert template instructions to Markdown
  - have RAs review trino uploads. Some columns get uploaded without a column name because column is in pandas Index
  - Have all RA's review data dictionary page. Format markdown nicely with equations and everything so that it makes sense

Nick
  - review new template docs with Nick. Edit to match the chart/dataset separation. Have Nick draft this.
  - have RAs review trino uploads. Some columns get uploaded without a column name because column is in pandas Index
  - Have all RA's review data dictionary page. Format markdown nicely with equations and everything so that it makes sense

Derrek

  - Fix Excel formatting on all charts
  - To assign: Adjust formatting of all plotly charts to match OFR style guide

## About this project

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

## Quick Start

### Step 0: Clone Repository

*Self-Signed Certificate Errors with OFR BitBucket Instance*:
To clone this repository or others from the OFR Bitbucket, you might have trouble with self-signed certificates. You can disable this for the cloning action as follows:
```
git -c http.sslVerify=false clone https://repository.ofr.treas.gov/scm/~jbejarano/project_template.git
```
If you have trouble pushing your changes, you can add this flag to the push as well. For example, use
```
git -c http.sslVerify=false push origin main
```

### Step 1: Set Up SSH Connections

You will also need to set up an SSH key and a keytab file. You can set up the SSH key like this. After connecting via SSH to `grid.ofr.treas.gov`, just paste the following lines into the OFR Grid terminal:
```
rm -irf ~/.ssh/authorized_keys
## accept all the defaults, leave the password blank
yes | ssh-keygen -t ecdsa -b 521 -N "" -f ~/.ssh/id_ecdsa 
cat ~/.ssh/id_ecdsa.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
## Now, ssh into trino.emr.ofr.treas.gov. It should not ask you for a password
ssh -o "StrictHostKeyChecking=accept-new" -t trino.emr.ofr.treas.gov 'printf "\n\nTrino connection setup completed successfully\n\n"'

```
Now, you should also do this in the Windows Command Prompt, so you can ssh into the grid without a password. Just copy the following lines into Windows Command Prompt:
```
del %USERPROFILE%\.ssh\id_rsa*
ssh-keygen -t rsa -b 2048 -f "%USERPROFILE%\.ssh\id_rsa" -N ""
type %USERPROFILE%\.ssh\id_rsa.pub >> U:\.ssh\authorized_keys
:: Sleep for 5 seconds to allow time to sync files
ping 127.0.0.1 -n 6 > nul
:: type "%USERPROFILE%\.ssh\id_rsa.pub" | ssh grid.ofr.treas.gov "cat >> ~/.ssh/authorized_keys"
ssh -o "StrictHostKeyChecking=accept-new" -t grid.ofr.treas.gov echo -e "\\n\\nGrid connection setup completed successfully\\n\\n"
```

You can create the keytab file using the 
[directions here](https://confluence.ofr.treas.gov/display/APPDEV/How+to+create+a+Kerberos+Keytab+file). Use the default settings given in the instructions.
It is preferred, but not required that you save the keytab file in your user directory and name it using your username. Thus, if your username is `jdoe`, it would be saved here:
```
/data/unixhome/jdoe/jdoe.keytab
```

### Step 2: Connect to OFR Grid via SSH

Next, connect to the OFR grid using the following instructions.
Although most of this code is platform independent, a limited few aspects of this repo will only work on the OFR grid 
(e.g., because it's running SQL pulls from our Trino database).
A limited few of them will only work there. This code is designed to be run from the command line after connecting via SSH. 
For interactive work, my preferred workflow follows these steps described 
[here.](https://confluence.ofr.treas.gov/pages/viewpage.action?spaceKey=OFRSYS&title=RAC%27s+Guide+to+Using+OFR%27s+HPC+Systems#RAC'sGuidetoUsingOFR'sHPCSystems-UseJupyterNotebookinLocalVDIwithJupyterserverrunningonworkernode)

For convenience, I repeat the main steps of this interactive work here:
```
ssh grid
tmux ## use this to prevent disconnection
cd /data/
module use -a /opt/aws_ofropt/Modulefiles
module load anaconda3/3.11.4 TeXLive/2023 R/4.4.0 pandoc/3.1.6 gcc/14.1.0 stata/17
pip install -r requirements.txt ## only needs to be done once. You may optionally use venv below
salloc --exclusive srun -X --pty bash -c 'jupyter notebook --no-browser --ip=$SLURMD_NODENAME' 
```
In a separate, local instance of Command Prompt, run this (subbing in the name
of the checked out node from above)
```
ssh grid.ofr.treas.gov -L 8888:defq-dy-generalq-2:8888 -N 
```

### Step 3: Configure environment variables in `.env` 

This template uses a `.env` file to contain user-specific configurations and secrets (such as API keys). The purpose is to separate configuration from code. This project uses the `decouple` [Python package](https://pypi.org/project/python-decouple/).

Create a new file called `.env` and save it in the root project directory. 
This files should NOT be committed to Git, since it can contain private
information. Use the included file `env.example` to
give you a sense of what the `.env` file should look like.
Include your user-specific and other configurations in this file.
Some examples would be to include your OFR username and the path
to your keytab file:

```
KEYTAB=config("KEYTAB", default="") ## Path to keytab file, 
## e.g. "/data/unixhome/jdoe/jdoe.keytab"
```


### Step 4: Install required software on grid

**LaTeX**
The reports of this code use LaTeX. 
You must have TexLive (or another LaTeX distribution) installed on your computer and available in your path.
I strongly recommend TeXLive, since it contains a snapshot of all available packages and you don't have to deal
with LaTeX package management (which is troublesome because of OFR restrictions). TeXLive can be obtained via 
a UAR. It can alternatively be loaded on the grid with the `module` command. More on that below.

**Conda or another environment manager**
To run this code, I recommend only using `conda` for the bare minimum. This is because `conda` is too slow
and `mamba` in not currently available on the OFR grid. Thus, for managing environments and Python versions, I use `conda`. 
For all other package management, I recommend `pip`.

**Working on the Grid**
On the grid, the easiest way to get started is to simply load Anaconda and TexLive modules.
You can do this with 
```
module use -a /opt/aws_ofropt/Modulefiles
module load anaconda3 TeXLive R pandoc gcc stata
```
You need to do this with every new session. The alternative is to install these yourself.
Now, you have an optional step of creating a virtual environment (for package isolation):
```
python -m venv ~/.venvs/pipeline
source ~/.venvs/pipeline/bin/activate ## Note: use deactivate to undo
```
Note, in Windows the command is `venv\Scripts\activate` and `deactivate`.

Having done this, then install the dependencies with pip (only needs to be done once)
```
pip install -r requirements.txt
```
Finally, you can then run 
```
doit
```
And that's it!

**Alternative Using Conda (which can be tricky on the grid)**

Having installed LaTeX and conda, open a terminal and navigate to the root directory of the project and create a 
conda environment using the following command:
```
conda create -n blank python=3.12
conda activate blank
```
and then install the dependencies with pip
```
pip install -r requirements.txt
```
Finally, you can then run 
```
doit
```
And that's it!

If you have problems with the SQL pulls to Trino or with `trino_driver.py`, try running `kinit` directly on the Trino grid first.

### Step 5: Optional Usage of R

If you would also like to run the R code included in this project, you can either install
R and the required packages manually. The included `environment.yml` file
contains the R packages needed, but these are unavailable through the OFR's conda channel.



## Other commands

### Copying Project Template Code without .git subdirectory
```
rsync -lrv --delete --exclude={.venv,_output,_data,_docs,.git} /data/unixhome/jbejarano/GitRepositories/chart_base/ /data/OPS_Share/chart_base/pipelines/

rsync -lr /data/unixhome/jbejarano/GitRepositories/chart_base/published_pipelines/ /data/OPS_Share/chart_base/to_be_published/

rsync -lr --delete --exclude={.venv,_output,_data,_docs,.git}  /data/unixhome/jbejarano/GitRepositories/chart_base/ /data/OPS_Share/_chart_base/
```
Altogether, this is
```
rsync -lrv --delete --exclude={.venv,_output,_data,_docs,.git} /data/unixhome/jbejarano/GitRepositories/chart_base/ /data/OPS_Share/chart_base/pipelines/ && rsync -lr /data/unixhome/jbejarano/GitRepositories/chart_base/published_pipelines/ /data/OPS_Share/chart_base/to_be_published/ && rsync -lr --delete --exclude={.venv,_output,_data,_docs,.git}  /data/unixhome/jbejarano/GitRepositories/chart_base/ /data/OPS_Share/_chart_base/
```

Links to 
```
file://pfileaws.ofr.treas.gov/Dept_Shares/Researchers/jbejarano/chart_base/chart_base/_docs/_build/html/index.html
file://pfileaws.ofr.treas.gov/Share/chart_base/chart_base/_docs/_build/html/index.html
```
The following link works in the File Explorer:

```
\\pfileaws.ofr.treas.gov\Share\chart_base
```

Note, from directory above, delete all `_docs` directories with this command:
```
for dir in ./*/; do (cd "$dir" && echo "Deleting _docs in $dir" && rm -irf ./_docs); done
```
Run doit forget in all subdirectories
```
for dir in ./*/; do (cd "$dir" && echo "Running in $dir" && doit forget pipeline_publish); done
```
For debugging (running all pipelines simultaneously to test changes), use this:
```
doit -n 9 -f ./dodo_debug_all.py
```

### Unit Tests and Doc Tests

You can run the unit test, including doctests, with the following command:
```
pytest --doctest-modules
```
You can build the documentation with:
```
rm ./src/.pytest_cache/README.md 
jupyter-book build -W ./
```
Use `del` instead of rm on Windows

### Setting Environment Variables

You can 
[export your environment variables](https://stackoverflow.com/questions/43267413/how-to-set-environment-variables-from-env-file) 
from your `.env` files like so, if you wish. This can be done easily in a Linux or Mac terminal with the following command:
```
set -a ## automatically export all variables
source .env
set +a
```
In Windows, this can be done with the included `set_env.bat` file,
```
set_env.bat
```

## General Directory Structure

 - The `assets` folder is used for things like hand-drawn figures or other
   pictures that were not generated from code. These things cannot be easily
   recreated if they are deleted.

 - The `output` folder, on the other hand, contains tables and figures that are
   generated from code. The entire folder should be able to be deleted, because
   the code can be run again, which would again generate all of the contents.

 - The `manual_data` is for data that cannot be easily recreated. This data
   should be version controlled. Anything in the `data` folder or in
   the `output` folder should be able to be recreated by running the code
   and can safely be deleted.

 - I'm using the `doit` Python module as a task runner. It works like `make` and
   the associated `Makefile`s. To rerun the code, install `doit`
   (https://pydoit.org/) and execute the command `doit` from the `src`
   directory. Note that doit is very flexible and can be used to run code
   commands from the command prompt, thus making it suitable for projects that
   use scripts written in multiple different programming languages.

 - I'm using the `.env` file as a container for absolute paths that are private
   to each collaborator in the project. You can also use it for private
   credentials, if needed. It should not be tracked in Git.

## Data and Output Storage

I'll often use a separate folder for storing data. Any data in the data folder
can be deleted and recreated by rerunning the PyDoit command (the pulls are in
the dodo.py file). Any data that cannot be automatically recreated should be
stored in the "manual_data" folder. Because of the risk of manually-created data
getting changed or lost, I prefer to keep it under version control if I can.
Thus, data in the "data" folder is excluded from Git (see the .gitignore file),
while the "manual_data" folder is tracked by Git.

Output is stored in the "output" directory. This includes tables, charts, and
rendered notebooks. When the output is small enough, I'll keep this under
version control. I like this because I can keep track of how tables change as my
analysis progresses, for example.

Of course, the data directory and output directory can be kept elsewhere on the
machine. To make this easy, I always include the ability to customize these
locations by defining the path to these directories in environment variables,
which I intend to be defined in the `.env` file, though they can also simply be
defined on the command line or elsewhere. The `config.py` is reponsible for
loading these environment variables and doing some like preprocessing on them.
The `config.py` file is the entry point for all other scripts to these
definitions. That is, all code that references these variables and others are
loading by importing `config`.

## Naming Conventions

 - **`pull_` vs `load_`**: Files or functions that pull data from an external
 data source are prepended with "pull_", as in "pull_fred.py". Functions that
 load data that has been cached in the "data" folder are prepended with "load_".
 For example, inside of the `pull_CRSP_Compustat.py` file there is both a
 `pull_compustat` function and a `load_compustat` function. The first pulls from
 the web, whereas the other loads cached data from the "data" directory.


## Dependencies and Virtual Environments

### Working with `pip` requirements

`conda` allows for a lot of flexibility, but can often be slow. `pip`, however, is fast for what it does.  You can install the requirements for this project using the `requirements.txt` file specified here. Do this with the following command:
```
pip install -r requirements.txt
```

The requirements file can be created like this:
```
pip list --format=freeze
```

### Working with `conda` environments

The dependencies used in this environment (along with many other environments commonly used in data science) are stored in the conda environment called `blank` which is saved in the file called `environment.yml`. To create the environment from the file (as a prerequisite to loading the environment), use the following command:

```
conda env create -f environment.yml
```

Now, to load the environment, use

```
conda activate blank
```

Note that an environment file can be created with the following command:

```
conda env export > environment.yml
```

However, it's often preferable to create an environment file manually, as was done with the file in this project.

Also, these dependencies are also saved in `requirements.txt` for those that would rather use pip. Also, GitHub actions work better with pip, so it's nice to also have the dependencies listed here. This file is created with the following command:

```
pip freeze > requirements.txt
```

**Other helpful `conda` commands**

- Create conda environment from file: `conda env create -f environment.yml`
- Activate environment for this project: `conda activate blank`
- Remove conda environment: `conda remove --name blank --all`
- Create blank conda environment: `conda create --name myenv --no-default-packages`
- Create blank conda environment with different version of Python: `conda create --name myenv --no-default-packages python` Note that the addition of "python" will install the most up-to-date version of Python. Without this, it may use the system version of Python, which will likely have some packages installed already.

### `mamba` and `conda` performance issues

Since `conda` has so many performance issues, it's recommended to use `mamba` instead. I recommend installing the `miniforge` distribution. See here: https://github.com/conda-forge/miniforge
