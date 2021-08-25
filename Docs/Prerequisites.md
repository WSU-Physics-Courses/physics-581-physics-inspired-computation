(sec:prerequisites)=
Prerequisites and Resources
===========================

There are no formal prerequisites for the course, but I will expect you to be
comfortable with the material discussed here, which contains links to additional
resources should you need to refresh your knowledge.  Please work with your classmates
to try to share knowledge as needed.  Generally, I will expect familiarity with the
following:

Domain Specific Preparation: 
: The most important prerequisite is the ability to communicate about and formulate
  complex problems in your field of study that would benefit from the techniques covered
  in this course.  Students will expected to actively engage with the techniques taught
  in this course, apply them to relevant problems in their domain of expertise, and to
  communicate about the efficacy to the class.

Linear Algebra
: Properties of Linear Operators (Self-Adjoint, Hermitian, Unitary,
  etc.), Matrix Factorization including the Singular Value Decomposition, Bases and
  Orthogonalization via
  [Gram-Schmidt](https://en.wikipedia.org/wiki/Gram%E2%80%93Schmidt_process).

Real and Complex Analysis
: Topology (notions of continuity), Calculus, [Banach
  spaces](https://en.wikipedia.org/wiki/Banach_space) (e.g. conditions for the existence
  of extrema), Fourier Analysis, Contour Integration, Conformal Maps.

Differential Equations
: Formulation of differential equations, existence of solutions and boundary value
  requirements, [Sturm-Liouville
  Theory](https://en.wikipedia.org/wiki/Sturm%E2%80%93Liouville_theory). 

Programming Skills
: There are some specific skills you will need for this course, including basic
  programming skills, distributed version control, how to connect remotely to computers
  etc. with [SSH].  We will use the [CoCalc] platform so you do not need to install any
  of the software on your computer.

(sec:version-control)=
## Version Control

You should know how to use a distributed version control system such as
[Git] or [Mercurial].  This project assumes you can use [Git], but I actually prefer
[Mercurial] which I find has a much more intuitive interface.  [Git] is much more
popular due to [GitHub] and [GitLab] (but keep an eye on [Heptapod] -- a fork of
[GitLab] for [Mercurial]), and you are likely to find more resources about [Git]
online.  Also, [Heptapod] is not yet ready for prime time, so [GitLab] or [GitHub] are
to be preferred.

:::{note}
If you install the [hg-git] plugin, then you can use [Mercurial] to work with [Git]
repos.  This is what I generally do, but it adds some potential complications, so I
do not recommend it unless you are comfortable with [Mercurial]:

```bash
hg clone https://gitlab.com/wsu-courses/physics-581-physics-inspired-computation.git
```

To enable [Mercurial] with a useful set of tools, you can do the following:

```bash
python3 -m pip install --upgrade --user pip mercurial hg-evolve hg-git jupytext black
```
   
This allows you to use the [Heptapod
workflow](https://octobus.net/blog/2019-09-04-heptapod-workflow.html)
:::


If you are not familiare with a distributed version control system like [Mercurial] or
[Git], the [Software Carpentry] program has two relevant courses you should work through
completely:

* [Software Carpentry: The Unix Shell](http://swcarpentry.github.io/shell-novice/).  Please work-though the course (about 4.5h) if you are not familiar with the
  Unix command line.
* [Software Carpentry: Version Control with
  Git](http://swcarpentry.github.io/git-novice/). Please work-though the course (about
  3h) if you are not familiar with [Git].

(sec:python)=
## Python, [SciPy], [NumPy], etc.

While not absolutely required, a good working knowledge of [Python] is needed. You will
also need to develop an understanding of the [SciPy] ecosystem, especially [NumPy],
[Matplotlib], and the [SciPy library] itself.  The following are a good place to start
learning about these:

* [Official Python Tutorial](https://docs.python.org/3/tutorial/index.html): A good
  starting point is to read this tutorial.  It goes into quite a few details, but will
  give you a good idea of what is possible with python and the standard library.
* [Software Carpentry: Programming with
  Python](https://swcarpentry.github.io/python-novice-inflammation/): The [Software
  Carpentry] course provides a pretty good gentle introduction (~7.5h) although it is
  quite data focused.
* {cite:p}`Gezerlis:2020`, ["Numerical Methods in Physics with Python" (2020)](
  https://ntserver1.wsulibs.wsu.edu:2532/core/books/numerical-methods-in-physics-with-python/563DF013576DCC535668A100B8F7D2F9):
  The course textbook has a fairly gentle introduction to basic python and then quickly
  gets into some of the more important points about array processing with [NumPy] which
  will be central to this course.
* {cite:p}`VanderPlas:2016`, [J. VanderPlas: "Python Data Science Handbook" (2016)](
  https://ntserver1.wsulibs.wsu.edu:2171/lib/wsu/detail.action?docID=4746657&pq-origsite=primo):
  Jake's book assumes you know Python, then dives into some of the more interesting
  features for data analysis, including [NumPy], [Pandas], etc.  Definitely read Chapter
  2 about [NumPy] and Chapter 4 about visualizing with [Matplotlib]

## CoCalc

You should be familiar with [CoCalc]; specifically:

* Creating an account.
* Creating projects.
* Using [Jupyter Notebooks](https://jupyter.org).
* Adding [SSH] keys to your project so you can use [SSH] to connect.

### References
* [CoCalc: Getting Started](https://doc.cocalc.com/getting-started.html)

## SSH

You should know how to use [SSH] to connect to remote servers (in particular [CoCalc])
with password-less login using `ssh-keygen` to generate a key, `ssh-agent` to add this
key, and the forwarding this key so you can use this to authenticate to [GitLab] etc.

* [Adding SSH keys to your CoCalc account](https://doc.cocalc.com/account/ssh.html)
* [Adding SSH keys to your GitLab account](https://docs.gitlab.com/ee/ssh/)


[SciPy]: <https://www.scipy.org/> "SciPy (pronounced “Sigh Pie”) is a Python-based ecosystem of open-source software for mathematics, science, and engineering."
[NumPy]: <https://numpy.org/> "The fundamental package for scientific computing with Python"
[Matplotlib]: <https://matplotlib.org/> "Matplotlib: Visualization with Python"
[SciPy library]: <https://www.scipy.org/scipylib/> "The SciPy library is one of the core packages that make up the SciPy stack."

[CoCalc]: <https://cocalc.com> "CoCalc: Collaborative Calculation and Data Science"
[Conda]: <https://docs.conda.io/en/latest/> "Conda: Package, dependency and environment management for any language—Python, R, Ruby, Lua, Scala, Java, JavaScript, C/ C++, FORTRAN, and more."
[GitHub]: <https://github.com> "GitHub"
[GitLab]: <https://gitlab.com> "GitLab"
[Git]: <https://git-scm.com> "Git"
[Heptapod]: <https://heptapod.net> "Heptapod: is a community driven effort to bring Mercurial SCM support to GitLab"
[Jupyter]: <https://jupyter.org> "Jupyter"
[Jupytext]: <https://jupytext.readthedocs.io> "Jupyter Notebooks as Markdown Documents, Julia, Python or R Scripts"
[Mercurial]: <https://www.mercurial-scm.org> "Mercurial"
[Official Course Repository]: <https://gitlab.com/wsu-courses/physics-581-physics-inspired-computation/> "Official Physics 581 Repository hosted on GitLab"
[Resources project]: <https://gitlab.com/wsu-courses/physics-581-physics-inspired-computation_resources> "Private course resources repository."
[SSH]: <https://en.wikipedia.org/wiki/Secure_Shell> "SSH on Wikipedia"
[Shared CoCalc Project]: <https://cocalc.com/projects/74852aba-2484-4210-9cf0-e7902e5838f4/> "581-2021 Shared CoCalc Project"
[WSU Courses CoCalc project]: <https://cocalc.com/projects/c31d20a3-b0af-4bf7-a951-aa93a64395f6>
[WSU Physics]: <https://physics.wsu.edu> "WSU Physics Department"
[file an issue]: <https://gitlab.com/wsu-courses/physics-581-physics-inspired-computation/-/issues> "Issues on the class GitLab project."
[hg-git]: <https://hg-git.github.io> "The Hg-Git mercurial plugin"
[Software Carpentry]: <https://software-carpentry.org/> "Software Carpentry: Teaching basic lab skills for research computing"

<!--
```{include} Links.md
```
-->
