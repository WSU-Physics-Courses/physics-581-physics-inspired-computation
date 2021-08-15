SHELL := /bin/bash

all: _ext/Resources

_ext/Resources:
	git clone git@gitlab.com:wsu-courses/physics-581-physics-inspired-computation_resources.git $@

cocalc-init:
	source "$$ANACONDA2020/bin/activate" root && anaconda-project prepare && conda activate envs/default && python3 -m ipykernel install --user --name "PHYS-581-2021" --display-name "Python 3 (PHYS-581-2021)"

sync:
	find . -name ".ipynb_checkpoints" -prune -o \
	       -name "_ext" -prune -o \
	       -name "envs" -prune -o \
	       -name "*.ipynb" -exec jupytext --sync {} \;

.PHONY: clean cocalc-init sync
