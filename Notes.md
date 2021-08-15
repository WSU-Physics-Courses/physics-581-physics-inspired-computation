Instructor Notes
================

These are notes about creating and maintaining this repository.  They may be in a state
of flux.

## Maintainer Notes
Try to keep this upper-level project as clean as possible, matching the layout expected
for the students.  This will be turned into a skeleton at some point.


## Tools

### Cookie Cutter
* https://github.com/cookiecutter/cookiecutter
* https://cookiecutter-hypermodern-python.readthedocs.io/

### Anaconda Project

```bash
anaconda-project init
anaconda-project add-packages python=3.9 scipy matplotlib sphinx
anaconda-project add-lpackages conda-forge::uncertainties
anaconda-project add-packages conda-forge::sphinx-panels conda-forge::sphinx-book-theme conda-forge::myst-nb
anaconda-project add-packages --pip sphinxcontrib-zopeext sphinxcontrib-bibtex mmf-setup
```

To clean:

```bash
anaconda-project clean
```

## Repository Setup

Can use GitHub, GitLab, or Heptapod.  With automatic pushing to GitHub, one and run the
following CI's:
* LGTM.com

* One course repo.  Students clone their own fork and pull changes.  Assignments
  distributed as tests.
* How to grade?  Student's can keep projects private (but probably will not have access
  to badges.)  Run tests on Student's CoCalc servers or with CI?
  

## Best Practices

* Use Jupytext and version control the associated python files.  Only commit the full
  notebooks (with output) when you want to archive documentation.
  * Maybe do this on an "output" branch or something so the main repo does not get
    cluttered?


## Docs

To build the documents interactively:

```bash
make doc-server
```

This will run [`sphinx-autobuild`](https://github.com/executablebooks/sphinx-autobuild)
which will launch a webserver on http://127.0.0.1:8000 and rebuild the docs whenever you
save a change.

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
```

## CoCalc Setup

* [Purchase a license](https://cocalc.com/settings/licenses) with 2 projects to allow
  the course and [WSU Courses CoCalc project] and [Shared CoCalc Project] to run.  This
  approach requires the students to pay $14 for access four the term (4 months).  They
  can optionally use any license they already have instead.
   
  Optionally, one might opt to purchase a license for $n+2$ projects where $n$ is the
  number of students, if there is central funding available.  See [Course Upgrading
  Students](https://doc.cocalc.com/teaching-upgrade-course.html#course-upgrading-students)
  for more details.
  
* Next, [create a course](https://doc.cocalc.com/teaching-create-course.html).  I do
  this in my [WSU Courses CoCalc project] called
  [581-2021](https://cocalc.com/projects/c31d20a3-b0af-4bf7-a951-aa93a64395f6/files/PhysicsInspiredComputation/581-2021.course).
  
  Open this course and create the [Shared CoCalc Project].  Activate the license for
  this project so that it can run.  I then add the SSH key to may `.ssh/config` files so
  I can quickly login.

* Clone the repos into the shared project and initialize the project.  Optional, but
  highly recommend -- use my [`mmf-setup`] project to provide some useful features

  ```bash
  ssh smc581shared       # My alias in .ssh/config
  python3 -m pip install mmf_setup
  mmf_setup cocalc
  ```
  
  This provides some instructions on how to use the CoCalc configuration.  The most
  important is to forward your user agent and set your `hg` and `git` usernames:
  
  ```bash
  ~$ mmf_setup cocalc
  ...
  If you use version control, then to get the most of the configuration,
  please make sure that you set the following variables on your personal
  computer, and forward them when you ssh to the project:

      # ~/.bashrc or similar
      LC_HG_USERNAME=Your Full Name <your.email.address+hg@gmail.com>
      LC_GIT_USEREMAIL=your.email.address+git@gmail.com
      LC_GIT_USERNAME=Your Full Name

  To forward these, your SSH config file (~/.ssh/config) might look like:

      # ~/.ssh/config
      Host cc-project1
        User ff1cb986f...
    
      Host cc*
        HostName ssh.cocalc.com
        ForwardAgent yes
        SendEnv LC_HG_USERNAME
        SendEnv LC_GIT_USERNAME
        SendEnv LC_GIT_USEREMAIL
        SetEnv LC_EDITOR=vi
  ```
  
  Logout and log back in so we have the forwarded credentials, and now clone the repos.
  
  ```bash
  git clone git@gitlab.com:wsu-courses/physics-581-physics-inspired-computation.git
  cd physics-581-physics-inspired-computation
  make
  ```
  
  The last step runs `git clone
  git@gitlab.com:wsu-courses/physics-581-physics-inspired-computation_resources.git
  _ext/Resources` which puts the resources folder in `_ext/Resources`.

* Create an environment:

  ```bash
  ssh smc581shared
  cd physics-581-physics-inspired-computation
  anaconda2020
  anaconda-project prepare
  conda activate envs/default
  python -m ipykernel install --user --name "PHYS-581-2021" --display-name "Python 3 (PHYS-581-2021)"
  ```

  This will create a Conda environment as specified in `anaconda-project.yml` in `envs/default`.

[WSU Courses CoCalc project]: <https://cocalc.com/projects/c31d20a3-b0af-4bf7-a951-aa93a64395f6>
[Shared CoCalc Project]: (https://cocalc.com/projects/74852aba-2484-4210-9cf0-e7902e5838f4/) "581-2021 Shared CoCalc Project"
