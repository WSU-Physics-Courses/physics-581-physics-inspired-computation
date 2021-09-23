Instructor Notes
================

These are notes about creating and maintaining this repository.  They may be in a state
of flux.

To Do
-----
* Fix `{{ course_package }}` replacement in `Syllabus.md`.
* Add test for anaconda-package version and issue warning.
* Clean `~/.bash_aliases` with `make reallyclean`.
* Try to activate the environment only once on CoCalc in Makefile.
* Deal with memory issues (`mamba` everywhere, or `--override-channels` on CoCalc).

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
mv anaconda-project.yml anaconda-project.yaml  # https://stackoverflow.com/a/22268973/1088938
anaconda-project add-packages python=3.9 scipy matplotlib sphinx notebook ipykernel nb_conda
anaconda-project add-lpackages conda-forge::uncertainties
anaconda-project add-packages conda-forge::sphinx-panels conda-forge::sphinx-book-theme conda-forge::myst-nb
anaconda-project add-packages pytest-cov pytest-flake8 pytest-xdist 
anaconda-project add-packages --pip sphinxcontrib-zopeext sphinxcontrib-bibtex mmf-setup
```

Then I changed all occurrences of `default` to `phys-581-2021` in
`anaconda-project.yaml` so that the environments have a consistent naming convention.


To clean:

```bash
anaconda-project clean
```

[`nbrr`]
: Maybe look at https://github.com/pyoceans/nbrr as a way of generating dependencies.
  This is used by [PyVis examples](https://examples.pyviz.org/make_project.html).

[`nbrr`]: <https://github.com/pyoceans/nbrr> "Jupyter Notebook Reproducible Repositories" 

## Repository Setup

Can use GitHub, GitLab, or Heptapod.  With automatic pushing to GitHub, one and run the
following CI's:
* LGTM.com

* One course repo.  Students clone their own fork and pull changes.  Assignments
  distributed as tests.
* How to grade?  Student's can keep projects private (but probably will not have access
  to badges.)  Run tests on Student's CoCalc servers or with CI?
  
### Things Students Need to Change
These are things that each student must change in their repo.  These should be fields in
the final skeleton project.

* `pyproject.toml`: `description`, `repository`, `documentation`, and ultimately
  `version`, `license`.
* 

## Best Practices
* Use Jupytext and version control the associated python files.  Only commit the full
  notebooks (with output) when you want to archive documentation.
  * Maybe do this on an "output" branch or something so the main repo does not get
    cluttered?


## Tests and Grading

Tests are setup using [`pytest`].  The configuration is in `pyprojects.toml` and
`.coveragerc`.  Each assignment will have an official test-suite called
`tests/assignmentX/test_official_assignmentX.py` where `X` is the assignment number.
These official tests will be marked with the special marker `assignmentX`, so that the
official tests can be run with:

```bash
pytest -k test_official_assignmentX --no-cov  # Disable coverage.
```

Students should be instructed not to put tests in `tests/assignmentX/test_official_assignmentX.py`

### Reporting

In order to generate badges, we store reporting information in the `_artifacts/` folder
including the following:

* [`_artifacts/htmlcov/index.html`](_artifacts/pytest_report.html): Report of tests.
  (Location specified in `pyproject.toml`.)
* [`_artifacts/junit.xml`](_artifacts/junit.xml): Test reports in junit-format. (Location specified in `pyproject.toml`.)
* [`_artifacts/htmlcov/index.html`](file://_artifacts/htmlcov/index.html): Test coverage
  report. (Location specified in `.coveragerc`.)
* [`_artifacts/coverage.xml`](_artifacts/coverage.xml): Coverage report in cobertura
  format that [GitLab] can use to generate reports as discussed in [GitLab test coverage
  visualization]. (Location specified in `.coveragerc`.)

Note: the "latest artifacts" are [only available if the pipeline
succeeds](https://forum.gitlab.com/t/is-there-a-way-to-ci-latest-artifact-link-work-also-for-failed-jobs/52262/3).
This means that we can't get the badges unless the pipelines pass.  To deal with this,
we make all tests pass artificially by `anaconda-project run test || true` and then use
the badges:

anaconda-project run test 

* ![Tests Badge](https://gitlab.com/wsu-courses/physics-581-physics-inspired-computation/-/jobs/artifacts/main/raw/_artifacts/test-badge.svg?job=test)
* ![Coverage Badge](https://gitlab.com/wsu-courses/physics-581-physics-inspired-computation/-/jobs/artifacts/main/raw/_artifacts/coverage-badge.svg?job=test)
* ![Assignment 0 Badge](https://gitlab.com/wsu-courses/physics-581-physics-inspired-computation/-/jobs/artifacts/main/raw/_artifacts/test-0-badge.svg?job=test-0)
* ![Assignment 1 Badge](https://gitlab.com/wsu-courses/physics-581-physics-inspired-computation/-/jobs/artifacts/main/raw/_artifacts/test-1-badge.svg?job=test-1)

## Docs

We use [MyST] for writing the documentation, which is the compiled into HTML, PDF,
etc. with [Sphinx] using the ideas of [JupyerBook] but simply using [Sphinx].  The
documents live in `Docs/` with the exception of `README.md` which lives at the top level
and provides the landing page for the
[GitLab](https://gitlab.com/wsu-courses/physics-581-physics-inspired-computation) and
[GitHub](https://github.com/WSU-Physics-Courses/physics-581-physics-inspired-computation)
repos.

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

I then edited the `conf.py`.

```bash
hg add local.bib _static/ _templates/
```

Substitutions can be used for parameters such as the `{{ class_room }} = ` {{ class_room
}}.  These can be defined in `cony.py` in the `myst_substitutions` dictionary and follow
Jinja2 conventions.  I use these to factor common information which will ultimately be
part of the templates.

### Read The Docs

The documents are hosted at [Read the
Docs](https://readthedocs.org/projects/physics-581-physics-inspired-computational-techniques/) (RtD)
where they should be build automatically whenever the main branch is pushed.  To get
this working, one needs to tell RtD which packages to install, and they [recommend using
a configuration file](https://docs.readthedocs.io/en/stable/config-file/v2.html) for
this called `.readthedocs.yaml`.

### Gotchas

* Be careful not to use [MyST] features in the `README.md` file as this forms the
  landing page on the
  [GitLab](https://gitlab.com/wsu-courses/physics-581-physics-inspired-computation) and
  [GitHub](https://github.com/WSU-Physics-Courses/physics-581-physics-inspired-computation)
  repos, neither of which support [MyST].  Check these to be sure that they look okay.
* We literally include the top-level `README.md` files as the first page of the
  documentation in `Docs/index.md`.  This as one side effect that when running `make
  doc-server` (`sphinx-autobuild`), edits to `README.md` do not trigger rebuilding of
  the `index.md` file.  While actively editing, I include `README.md` as a separate
  file, and view that.
* We are using [`anaconda-project`], but [Read the Docs] does not directly support
  provisioning from this, however, you can make the `anaconda-project.yaml` file look
  like an `environment.yaml` file if you [change `packages:` to `dependencies:` as long
  as you can ensure `anaconda-project>=0.8.4`](https://github.com/Anaconda-Platform/anaconda-project/issues/265#issuecomment-903206709).  This allows one to simply install
  this with `conda env --file anaconda-project.yaml`.  
* Since we are just doing a Conda install on RtD, we don't run `anaconda-project run
  init` and the kernel used by our notebooks does not get installed.  We can do this in
  the Sphinx `Docs/conf.py` file:
* Variables defined in `myst_substitutions` do not seem to be available for use in
  templates.  For this, the definitions must also be added to `html_context`.
* Note that `{% raw %} ... {% endraw %}`  allows you to literally include things like
  MathJaX where the braces confuse Jinja.
  
  ```python
  # Docs/conf.py
  ...
  def setup(app):
      import subprocess

      subprocess.check_call(["anaconda-project", "run", "init"])
  ```
* Don't use `bash` code-blocks when you include output, use `console` instead.  The
  reason is that `bash` code highlighting will fail with `WARNING: Could not lex
  literal_block as "bash". Highlighting skipped.` if your output has an [odd number of
  single quotes](https://github.com/sphinx-doc/sphinx/issues/4098).  Thus write:
  
  ````markdown
  ```console
  $ echo "This line's going to cause a problem"
  This line's going to cause a problem
  ```
  ````
  
  which renders as
  
  ```console
  $ echo "This line's going to cause a problem"
  This line's going to cause a problem
  ```
  
  instead of 
  
  ````
  ```bash
  $ echo "This line's going to cause a problem"
  This line's going to cause a problem
  ```
  ````
  
  which will raise the warning.  *(Interestingly, I could not even nest this block
  without triggering the warning, hence the lack of highlighting in the above block.)*
  
## CoCalc Setup

* [Purchase a license](https://cocalc.com/settings/licenses) with 2 projects to allow
  the course and [WSU Courses CoCalc project] and [Shared CoCalc Project - Physics 581
  Fall 2021] to run.  This approach requires the students to pay $14 for access four the
  term (4 months).  They can optionally use any license they already have instead.
   
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

* Add students, and follow prompt to update the payment option.

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

  This will create a Conda environment as specified in `anaconda-project.yaml` in `envs/default`.

* For students to be able to use the Linux terminal through their browser, they will
  need to provide appropriate git or mercurial configuration.  They could do this by
  defining environmental variables in their individual project settings:
  
  ```json
  {
    "LC_HG_USERNAME": "Michael McNeil Forbes <michael.forbes+python@gmail.com>",
    "LC_GIT_USERNAME": "Michael McNeil Forbes",
    "LC_GIT_USEREMAIL": "michael.forbes+python@gmail.com",
  }
  ```
  
  If they do not SSH in with a forwarded agent, then they will still need to use their
  password every time they push.  Note: SSH variable forwarding will override these.

### CoCalc Issues

* `/ext/anaconda2020.02/.condarc` includes so many channels that even a simple `conda
  search uncertainties` fails.  `mamba` stills works, so we use this for now.

## GitLab Setup

For [GitLab] access to the private repository, I created a group [Physics
581-2021](https://gitlab.com/phys-581-2021) and invited all the students.  I figure that
it will be easier to update this each year.  I then added this group to the repos.

### CI

The GitLab CI is defined in the file `.gitlab-ci.yml`.  My working strategy is:

1. Use a Docker image for Conda.
2. Update this with `anaconda-project`.
3. Use `anaconda-project run test`.

This works, but takes about [5
minutes](https://gitlab.com/wsu-courses/physics-581-physics-inspired-computation/-/pipelines/363108475).
In
principle, it might improve things to cache the virtual environment... Needs testing.

#### Badges

[GitLab] provides some support for generating badges, but it is not very flexible.
Instead, I generate badges as artifacts from the test process.  The following packages
are useful:

* **[`genbadge`]**: Generates badges from `pytest` reports.  Specific for `pytest`,
  `coverage`, and `flake8`, but very convenient for these.
* [`anybadge`]: General badge generation, but you need to feed in the appropriate
  numbers.

To get the badges, go to **Settings > CI/CD > General pipelines***.  I did the following
here:

* Set a small Timeout **20min** (important for students to do so they don't run out on
  private projects).
* Copy the badges.  Note: it is not easy to [change the "pipline"
  name](https://stackoverflow.com/questions/55836220/how-to-change-pipeline-badge-name)
  in the badges.

To get [coverage working](https://docs.gitlab.com/ee/user/project/merge_requests/test_coverage_visualization.html), I needed to:

1. Generate `_htmlcov/coverage.xml` by adding an `[xml]` section to `.coveragerc`.
2. Add the `--cov-report=xml` option in `pyproject.toml` in the
   `[tool.pytest.ini_options]` section.
3. Make the report an `artifact` in `.gitlab-ci.yml`.

With this enabled, I can get the following badges:

[![pipeline status](https://gitlab.com/wsu-courses/physics-581-physics-inspired-computation/badges/main/pipeline.svg)](https://gitlab.com/wsu-courses/physics-581-physics-inspired-computation/-/commits/main)

[![coverage report](https://gitlab.com/wsu-courses/physics-581-physics-inspired-computation/badges/main/coverage.svg)](https://gitlab.com/wsu-courses/physics-581-physics-inspired-computation/-/commits/main)

Note: by default it does not seem possible to get different badges for different jobs.
Instead, it seems that one must generate the badges as part of the tests.  I am playing
with the [`anybadge`] project.

* [Customize pipeline configuration (GitLab
  Docs)](https://docs.gitlab.com/ee/ci/pipelines/settings.html)
* [Gitlab - How to add badge based on jobs
  pipeline](https://stackoverflow.com/questions/52228070/gitlab-how-to-add-badge-based-on-jobs-pipeline)
* [GitLab covraged badge with
  pytest](https://www.stddev.tech/gitlab-coverage-badge-with-pytest/): Shows how to
  generate a coverage badge without any artifacts.  We use artifacts anyway so that
  [GitLab] will show in the diffs as discussed in [GitLab test coverage
  visualization].

## GitHub Mirror

[GitHub] has a different set of tools, so it is useful to mirror the repo there so we
can take advantage of these:

* [GitLab Main Repo](https://gitlab.com/wsu-courses/physics-581-physics-inspired-computation)
* [GitHub Mirror](https://github.com/WSU-Physics-Courses/physics-581-physics-inspired-computation)

To do this:

1. Create an empty [GitHub
   project](https://github.com/forbes-group/physics-581-physics-inspired-computation).
   Disable
   [Features](https://github.com/WSU-Physics-Courses/physics-581-physics-inspired-computation/settings)
   like `Wikis`, `Issues`, `Projects`, etc. which are not desired for a mirror.
2. Get a personal token from [GitHub] as [described
   here](https://hg.iscimath.org/help/user/project/repository/repository_mirroring#setting-up-a-push-mirror-from-gitlab-to-github).
   Create a token here [**Settings > Developer settings > Personal access
tokens**](https://github.com/settings/tokens) with `repo` access, `admin:repo_hook`
   access, and `delete_repo` access.  Copy the key. 
3. Go to your [**Settings > Repository > Mirroring
   respositories**](https://gitlab.com/wsu-courses/physics-581-physics-inspired-computation/-/settings/repository)
   in you GitLab repo and use the URL to your GitHub repo using the following format:
   `https://<your_github_username>@github.com/<your_github_group>/<your_github_project>.git`.
   I.e.:
   
   ```
   https://mforbes@github.com/WSU-Physics-Courses/physics-581-physics-inspired-computation.git
   ```
   
   Include your name here (the user associated with the key you just generated) and
   use the key as the password.  Choose **Mirror direction** to be **Push**.
   Optionally, you can choose to mirror only protected branches: this would be a good
   choice if you were mirroring a private development repo and only wanted to public
   branches to be available on [GitHub].

Now whenever you push changes to GitLab, they will be mirrored on GitHub, allowing you
to use GitHub features like their CI, Notebook viewer etc.

# General Course Preparation

Here are the general steps needed to prepare for the course: see above for further
details.

1. Purchase $N+1$ CoCalc Licenses for $N$ courses for the duration of the course.
2. Create the following as needed (some may be reused from previous terms):

   CoCalc Course:
   : This is the course page where you add students.  It will give each student a
     private project, and create a shared course project.  E.g.:
     * [CoCalc Course File - Physics 581 Fall 2021]
     * [Shared CoCalc Project - Physics 581 Fall 2021]
   
   GitLab Course Project (Public)
   : This is the public repository for the course, with notes, assignments, syllabus,
     etc.  It will likely be reused, or cloned from a previous course.  E.g.:

     * [GitLab Public Project - Physics 581 Fall 2021]

   GitLab Course Resource Project (Private)
   : This is a private repository with things that should only be shared with the class,
     such as textbooks, data, etc.  *(Currently this is doing double duty as it is also
     used for data that could in principle be shared publicaly.  We may need to add a
     third repo later.)* E.g.:

     * [GitLab Resources Project - Physics 581 Fall 2021]
     

   GitLab Group for the course
   : To give students access to the course, I add them to a [GitLab] group, then I give
     the group access to the various projects above.  This makes it easy to switch
     classes, and to add students.  E.g.:

     * [Physics 581-2021 GitLab Group](https://gitlab.com/phys-581-2021)
     
   GitHub Mirror (Public)
   : This is a public mirror of the GitLab course project on [GitHub], allowing us to
     use their CI tools.  E.g.:
   
     * [GitHub Mirror - Physics 581 Fall 2021]
     
   

[MyST]: <https://myst-parser.readthedocs.io/en/latest/> "MyST - Markedly Structured Text"

[WSU Courses CoCalc project]: <https://cocalc.com/projects/c31d20a3-b0af-4bf7-a951-aa93a64395f6>

[GitHub]: <https://github.com> "GitHub"
[`pytest`]: <https://docs.pytest.org> "pytest: helps you write better programs"
[Read the Docs]: <https://readthedocs.org> "Read the Docs homepage"
[`anaconda-project`]: <https://anaconda-project.readthedocs.io> "Anaconda Project: Tool for encapsulating, running, and reproducing data science projects."

<!-- Fall 2021 links -->
[CoCalc Course File - Physics 581 Fall 2021]: <https://cocalc.com/projects/c31d20a3-b0af-4bf7-a951-aa93a64395f6/files/PhysicsInspiredComputation/581-2021.course>

[Shared CoCalc Project - Physics 581 Fall 2021]: <https://cocalc.com/projects/74852aba-2484-4210-9cf0-e7902e5838f4/> "581-2021 Shared CoCalc Project"

[GitLab Public Project - Physics 581 Fall 2021]: <https://gitlab.com/wsu-courses/physics-581-physics-inspired-computation> "GitLab public course project for Fall 2021."

[GitLab Resources Project - Physics 581 Fall 2021]: <https://gitlab.com/wsu-courses/physics-581-physics-inspired-computation_resources> "GitLab private resources course project for Fall 2021."

[GitHub Mirror - Physics 581 Fall 2021]: <https://github.com/WSU-Physics-Courses/physics-581-physics-inspired-computation> "GitHub mirror"

[`anybadge`]: <https://github.com/jongracecox/anybadge> "Python project for generating badges for your projects"
[`genbadge`]: <https://smarie.github.io/python-genbadge/> "Generate badges for tools that do not provide one."
[GitLab test coverage visualization]: <https://docs.gitlab.com/ee/user/project/merge_requests/test_coverage_visualization.html>
