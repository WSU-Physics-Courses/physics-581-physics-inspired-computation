Overview
========



Maintainer Notes
================
Try to keep this upper-level project as clean as possible, matching the layout expected
for the students.  This will be turned into a skeleton at some point.


Tools
=====

## Cookie Cutter
* https://github.com/cookiecutter/cookiecutter
* https://cookiecutter-hypermodern-python.readthedocs.io/

## Anaconda Project

```bash
anaconda-project init
anaconda-project add-packages python=3.9 scipy matplotlib sphinx
anaconda-project add-lpackages conda-forge::uncertainties
anaconda-project add-packages conda-forge::sphinx-panels conda-forge::sphinx-book-theme conda-forge::myst-nb
anaconda-project add-packages --pip sphinxcontrib-zopeext sphinxcontrib-bibtex 
```

To clean:

```bash
anaconda-project clean
```

Repository Setup
================

Can use GitHub, GitLab, or Heptapod.  With automatic pushing to GitHub, one and run the
following CI's:
* LGTM.com
* 

* One course repo.  Students clone their own fork and pull changes.  Assignments
  distributed as tests.
* How to grade?  Student's can keep projects private (but probably will not have access
  to badges.)  Run tests on Student's CoCalc servers or with CI?
  

Best Practices
==============
* Use Jupytext and version control the associated python files.  Only commit the full
  notebooks (with output) when you want to archive documentation.
  * Maybe do this on an "output" branch or something so the main repo does not get
    cluttered?


Docs
====
Here is the play-by-play for setting up the documentation.

```bash
cd Docs
sphinx-quickstart
wget https://brand.wsu.edu/wp-content/themes/brand/images/pages/logos/wsu-signature-vertical.svg -O _static/wsu-logo.svg 
cp -r ../envs/default/lib/python3.9/site-packages/sphinx_book_theme/_templates/* _templates
```

I then edited the `conf.py`

```bash
hg add local.bib _static/ _templates/
