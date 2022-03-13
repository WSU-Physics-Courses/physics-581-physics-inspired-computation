# Modelled after
# https://github.com/simoninireland/introduction-to-epidemics/blob/master/Makefile
SHELL = /bin/bash

RESOURCES = git@gitlab.com:wsu-courses/physics-581-physics-inspired-computation_resources.git

# Currently, even the new method uses too much memory...
USE_ANACONDA2020 ?= true

# ------- Tools -------
ifdef ANACONDA2020
  # If this is defined, we assume we are on CoCalc
  ifeq ($(USE_ANACONDA2020), true)
    # Old approach using anaconda-project in the ANACONDA2020 environment.
    # Due to the /ext/anaconda2020.02/.condarc issue, we must use mamba in this case
    # https://github.com/Anaconda-Platform/anaconda-project/issues/334#issuecomment-911918761
    CONDA_EXE = $$ANACONDA2020/bin/mamba
    ACTIVATE ?= source $$ANACONDA2020/bin/activate
  else
    # New approach - use our own miniconda
    MINICONDA = ~/.miniconda3
    CONDA_EXE = $(MINICONDA)/bin/conda
    ACTIVATE ?= source $(MINICONDA)/bin/activate
  endif

  #ANACONDA_PROJECT ?= $(ACTIVATE) root && CONDA_EXE=$(CONDA_EXE) anaconda-project
  ANACONDA_PROJECT ?= CONDA_EXE=$(CONDA_EXE) $$ANACONDA2020/bin/anaconda-project

else
  ACTIVATE ?= eval "$$(conda shell.bash hook)" && conda activate
  ANACONDA_PROJECT ?= CONDA_EXE=$(CONDA_EXE) anaconda-project
endif

ENV ?= phys-581-2021
ENV_PATH ?= $(abspath envs/$(ENV))
ACTIVATE_PROJECT ?= $(ACTIVATE) $(ENV_PATH)

# ------- Top-level targets  -------
581-Docs.tgz: Docs/*
	cd Docs && make html
	tar -s "|Docs/_build/html|581-Docs|g" -zcvf $@ Docs/_build/html

# Default prints a help message
help:
	@make usage


usage:
	@echo "$$HELP_MESSAGE"


MINICONDA_SH = https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
MINICONDA_HASH = 1ea2f885b4dbc3098662845560bc64271eb17085387a70c2ba3f29fff6f8d52f

$(MINICONDA):
	wget  $(MINICONDA_SH) -qO /tmp/_miniconda.sh
	echo "$(MINICONDA_HASH)  /tmp/_miniconda.sh" > /tmp/_miniconda.shasum
	shasum -a 256 -c /tmp/_miniconda.shasum && bash /tmp/_miniconda.sh -b -p $@
	rm /tmp/_miniconda.sh*
	$@/bin/conda update -y conda
	$@/bin/conda install -y anaconda-project
	# Dropping defaults allows this to work with < 1GB
	$@/bin/conda install --override-channels --channel conda-forge -y mamba
	$@/bin/conda clean -y --all


# Special target on CoCalc to prevent re-installing mmf_setup.
~/.local/bin/mmf_setup:
ifdef ANACONDA2020
	python3 -m pip install --user --upgrade mmf-setup
	mmf_setup cocalc
endif

init: _ext/Resources ~/.local/bin/mmf_setup anaconda-project.yaml $(MINICONDA)
	@make _init
ifdef ANACONDA2020
	if ! grep -Fq '$(ACTIVATE_PROJECT)' ~/.bash_aliases; then \
	  echo '$(ACTIVATE_PROJECT)' >> ~/.bash_aliases; \
	fi
	@make sync
endif

_init:
	$(ANACONDA_PROJECT) prepare
	$(ANACONDA_PROJECT) run init  # Custom command: see anaconda-project.yaml

.PHONY: _init

_ext/Resources:
	-git clone $(RESOURCES) $@
	@if [ ! -d "$@" ]; then \
	  echo "$$RESOURCES_ERROR_MESSAGE"; \
	fi


Docs/environment.yaml: anaconda-project.yaml Makefile
	$(ANACONDA_PROJECT) run export 1> $@


# Jupytext
sync:
	find . -name ".ipynb_checkpoints" -prune -o \
	       -name "_ext" -prune -o \
	       -name "envs" -prune -o \
	       -name "*.ipynb" -o -name "*.md" \
	       -exec jupytext --sync {} + 2> >(grep -v "is not a paired notebook" 1>&2)
# See https://stackoverflow.com/a/15936384/1088938 for details

clean:
	-find . -name "__pycache__" -exec $(RM) -r {} +
	-$(RM) -r _htmlcov .coverage .pytest_cache
	-$(ACTIVATE) root && conda clean --all -y


realclean:
	$(ANACONDA_PROJECT) run clean || true  # Custom command: see anaconda-project.yaml
	$(ANACONDA_PROJECT) clean || true
	$(RM) -r envs


test:
	$(ANACONDA_PROJECT) run test
	$(ANACONDA_PROJECT) run test-0
	$(ANACONDA_PROJECT) run test-1
	$(ANACONDA_PROJECT) run test-2
	$(ANACONDA_PROJECT) run test-4

doc-server:
	$(ANACONDA_PROJECT) run sphinx-autobuild --re-ignore '_build|_generated' Docs Docs/_build/html

#$(ANACONDA_PROJECT) run sphinx-autobuild --ignore '*/_build/*' --ignore '*/_generated/*' Docs Docs/_build/html


.PHONY: clean realclean init cocalc-init sync doc-server help test


# ----- Usage -----

define HELP_MESSAGE

This Makefile provides several tools to help initialize the project.  It is primarly designed
to help get a CoCalc project up an runnning, but should work on other platforms.

Variables:
   ANACONDA2020: (= "$(ANACONDA2020)")
                     If defined, then we assume we are on CoCalc and use this to activate
                     the conda base envrionment. Otherwise, you must make sure that the ACTIVATE
                     command works properly.
   ACTIVATE: (= "$(ACTIVATE)")
                     Command to activate a conda environment as `$$(ACTIVATE) <env name>`
                     Defaults to `conda activate`.
   ANACONDA_PROJECT: (= "$(ANACONDA_PROJECT)")
                     Command to run the `anaconda-project` command.  If you need to first
                     activate an environment (as on CoCalc), then this should do that.
                     Defaults to `anaconda-project`.
   ENV: (= "$(ENV)")
                     Name of the conda environment user by the project.
                     (Customizations have not been tested.)
                     Defaults to `phys-581-2021`.
   ENV_PATH: (= "$(ENV_PATH)")
                     Path to the conda environment user by the project.
                     (Customizations have not been tested.)
                     Defaults to `envs/$$(ENV)`.
   ACTIVATE_PROJECT: (= "$(ACTIVATE_PROJECT)")
                     Command to activate the project environment in the shell.
                     Defaults to `$$(ACTIVATE)  $$(ENV)`.

Initialization:
   make init         Initialize the environment and kernel.  On CoCalc we do specific things
                     like install mmf-setup, and activate the environment in ~/.bash_aliases.
                     This is done by `make init` if ANACONDA2020 is defined.

Testing:
   make test         Runs the general tests.

Maintenance:
   make clean        Call conda clean --all: saves disk space.
   make realclean    delete the environments and kernel as well.

Documentation:
   make doc-server   Build the html documentation server on http://localhost:8000
                     Uses Sphinx autobuild
endef
export HELP_MESSAGE


define RESOURCES_ERROR_MESSAGE

*************************************************************
WARNING: The `_ext/Resources` folder could not be cloned from

  $(RESOURCES)

Likely this is because this repository is private and requires registration in the class.
If you believe that you should have access, please contact your instructor, and provide
your GitLab username.

These resources are not crucial for the project, but are important for the course.
*************************************************************

endef
export RESOURCES_ERROR_MESSAGE
