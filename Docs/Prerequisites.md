(sec:prerequisites)=
Prerequisites
=============

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
   
This allows you to use the [Heptapod workflow](https://octobus.net/blog/2019-09-04-heptapod-workflow.html)

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


[SSH]: <https://en.wikipedia.org/wiki/Secure_Shell> "SSH on Wikipedia"
[GitLab]: <https://gitlab.com> "GitLab"
[CoCalc]: <https://cocalc.com> "CoCalc: Collaborative Calculation and Data Science"
[file an issue]: <https://gitlab.com/wsu-courses/physics-581-physics-inspired-computation/-/issues> "Issues on the class GitLab project."
