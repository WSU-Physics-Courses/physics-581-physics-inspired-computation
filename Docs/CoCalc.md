# [CoCalc]

## Features

[CoCalc] provides an online platform for performing computations without the need to
install any software on your computer.  It allows you to immediately start exploring in
a variety of languages, which several unique features.  The following are particularly
relevant to this course:

Collaborative Editing
: [CoCalc] is one of the only platform I know of at the time that allows simultaneous editing
  of [Jupyter] notebooks.  This means that the instructors can directly connect to
  student's projects, seeing the exact same code, and interactively debugging it.  This
  is done with a custom implementation of the notebook server, with the downside that
  not all features of [Jupyter] notebooks are supported yet.  If you need to, you can
  launch a [Plain Jupyter Server and JupyterLab
  Server](https://doc.cocalc.com/jupyter.html#alternatives-plain-jupyter-server-and-jupyterlab-server)
  to regain all functionality (but will lose the collaborative editing ability while you
  do so).

[Extensive Software Preinstalled](https://cocalc.com/doc/software.htm)
: [CoCalc] comes with a large amount of [useful
  software](https://cocalc.com/doc/software.html), including a rather complete
  `Anaconda` environment.  This allows you to immediately start working.  Simply create
  a new [Jupyter] notebook, choose the `Anaconda2020` kernel, and start coding with the
  full SciPy software stack at your disposal. (Once you get things working, I
  **strongly** advocate migrating your code to a well tested repository like the one
  described here, but don't let this stop you from exploring.)
  
[VS Code] Editor:
: [CoCalc] now supports editing files in your browser with [VS Code].  While I
  personally use [Emacs], [VS Code] seems to be a very good tool for beginners.  I
  strongly recommend that you learn a good editor with powerful search and replace
  features, syntax highlighting and language support: it will ultimately save you lots
  of time.  *(Note: this is a fairly
  [new feature](https://github.com/sagemathinc/cocalc/issues/4479), however, and I have
  not explored it much, but it looks good.)*

I find a couple of other features important:

[Open Source](https://github.com/sagemathinc/cocalc)
: [CoCalc] itself is [open source](https://github.com/sagemathinc/cocalc) and can be
  installed from a [Docker image](https://doc.cocalc.com/docker-image.html).  This means
  that you can run [CoCalc] on your own hardware, with complete control of your data,
  even if they go out of business.  The make their profits by selling their service.  I
  completely support this type of business model which puts you in control of your data.

[Time Travel](https://doc.cocalc.com/time-travel.html)
: [CoCalc] implements an amazing backup system they call [Time
  Travel](https://cocalc.com/doc/software.htm) that allows you to roll back almost any
  file minutes, hours, days, weeks, or more.  I am blown away by how well this feature
  is implemented: it has saved me several times and along is worth the license costs.

Responsive Support
: The [CoCalc] company is small enough that they can still be responsive to feature and
  support requests.  When I have issues, the often make changes within an hour, and
  virtually never take more than a day.  This is in stark contrast to large companies
  where you submit a request to their community forums only to have it ignore for
  years.  Of course, the team being small means that they do not have the resources to
  implement everything, but can be motivated by money if you really need something
  done.  Nevertheless, they have always taken care of any core issues I have found
  promptly, and are really nice people too!

[Remote File Systems](https://doc.cocalc.com/project-settings.html#ssh-remote-files)
: You can [mount remote file systems with
  `sshfs`](https://doc.cocalc.com/project-settings.html#ssh-remote-files).  This allows
  you to use [CoCalc] as a tool to analyze off-site data (although performance will be
  slow because the data needs to be transferred over the network).

For a more completed exploration, look at the [list of features](https://cocalc.com/doc/).

## Setup

While one of the main benefits of [CoCalc] is that you can just fire it up and get to
work, for the purposes of this course, establishing a reproducible computing environment
is important.  After exploring several tools, I have landed on [`anaconda-project`]
which allows you to manage a [Conda] environment in a somewhat reasonable way.

Using this effectively on `CoCalc` is a bit challenging out of the box because the
default `anaconda2020` environment they have setup has a `/ext/anaconda2020.02/.condarc`
file with a whole slew of channels -- so many in fact that even a simple `conda search
uncertainties` almost runs out of memory.  One option is to use `mamba` which can be
done by setting `CONDA_EXE=mamba`.

Another potential option is to use a custom miniconda environment, but even this takes
too much memory.  Until `anaconda-project` has a [way of ignored the
channels](https://github.com/Anaconda-Platform/anaconda-project/issues/336), it seems
like the best option is to simply install our own version of Miniconda and use this as a
base:

```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -qO miniconda.sh
echo "1ea2f885b4dbc3098662845560bc64271eb17085387a70c2ba3f29fff6f8d52f  miniconda.sh" > miniconda.shasum
shasum -a 256 -c miniconda.shasum && bash miniconda.sh -b -p ~/.miniconda
rm miniconda.sh*
. ~/.miniconda/bin/activate
conda install anaconda-project
conda clean --all -y
du -sh ~/.miniconda   # 136M	/home/user/.miniconda
echo "export COCALC_MINICONDA=~/.miniconda" >> ~/.bashrc
```





[CoCalc Course File - Physics 581 Fall 2021]: <https://cocalc.com/projects/c31d20a3-b0af-4bf7-a951-aa93a64395f6/files/PhysicsInspiredComputation/581-2021.course>
[CoCalc]: <https://cocalc.com> "CoCalc: Collaborative Calculation and Data Science"
[Conda]: <https://docs.conda.io/en/latest/> "Conda: Package, dependency and environment management for any language—Python, R, Ruby, Lua, Scala, Java, JavaScript, C/ C++, FORTRAN, and more."
[GitHub Mirror - Physics 581 Fall 2021]: <https://github.com/WSU-Physics-Courses/physics-581-physics-inspired-computation> "GitHub mirror"
[GitHub]: <https://github.com> "GitHub"
[GitLab Public Project - Physics 581 Fall 2021]: <https://gitlab.com/wsu-courses/physics-581-physics-inspired-computation> "GitLab public course project for Fall 2021."
[GitLab Resources Project - Physics 581 Fall 2021]: <https://gitlab.com/wsu-courses/physics-581-physics-inspired-computation_resources> "GitLab private resources course project for Fall 2021."
[GitLab]: <https://gitlab.com> "GitLab"
[Git]: <https://git-scm.com> "Git"
[Heptapod]: <https://heptapod.net> "Heptapod: is a community driven effort to bring Mercurial SCM support to GitLab"
[Jupyter]: <https://jupyter.org> "Jupyter"
[Jupytext]: <https://jupytext.readthedocs.io> "Jupyter Notebooks as Markdown Documents, Julia, Python or R Scripts"
[Mercurial]: <https://www.mercurial-scm.org> "Mercurial"
[MyST]: <https://myst-parser.readthedocs.io/en/latest/> "MyST - Markedly Structured Text"
[Official Course Repository]: <https://gitlab.com/wsu-courses/physics-581-physics-inspired-computation/> "Official Physics 581 Repository hosted on GitLab"
[Read the Docs]: <https://readthedocs.org> "Read the Docs homepage"
[Resources project]: <https://gitlab.com/wsu-courses/physics-581-physics-inspired-computation_resources> "Private course resources repository."
[SSH]: <https://en.wikipedia.org/wiki/Secure_Shell> "SSH on Wikipedia"
[Shared CoCalc Project - Physics 581 Fall 2021]: <https://cocalc.com/projects/74852aba-2484-4210-9cf0-e7902e5838f4/> "581-2021 Shared CoCalc Project"
[Shared CoCalc Project]: <https://cocalc.com/projects/74852aba-2484-4210-9cf0-e7902e5838f4/> "581-2021 Shared CoCalc Project"
[WSU Courses CoCalc project]: <https://cocalc.com/projects/c31d20a3-b0af-4bf7-a951-aa93a64395f6>
[WSU Physics]: <https://physics.wsu.edu> "WSU Physics Department"
[`anaconda-project`]: <https://anaconda-project.readthedocs.io> "Anaconda Project: Tool for encapsulating, running, and reproducing data science projects."
[`pytest`]: <https://docs.pytest.org> "pytest: helps you write better programs"
[file an issue]: <https://gitlab.com/wsu-courses/physics-581-physics-inspired-computation/-/issues> "Issues on the class GitLab project."
[hg-git]: <https://hg-git.github.io> "The Hg-Git mercurial plugin"
[VS Code]: <https://code.visualstudio.com> "Visual Studio Code"
[Emacs]: <https://www.gnu.org/software/emacs/> "GNU Emacs: An extensible, customizable, free/libre text editor - and more."
