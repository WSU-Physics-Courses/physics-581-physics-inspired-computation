(sec:prerequisites)=
Prerequisites
=============

There are no formal prerequisites to this class, but you should know the following.
Some of this will be covered at the start of the course, but you may need to seek the
help of classmates or other resources if you are not comfortable with some of this
material.  Some resources are provided here, but suggestions are always welcome: please
[file an issue] with suggestions of resources you find helpful and I will include them.

*(probably need to soften)* 
* **Real and Complex Analysis**: Topology (notions of continuity), Calculus, [Banach
  spaces](https://en.wikipedia.org/wiki/Banach_space) (e.g. conditions for the existence
  of extrema), Fourier Analysis, Contour Integration, Conformal Maps.
* **Linear Algebra:** Properties of Linear Operators (Self-Adjoint, Hermitian, Unitary,
  etc.), Matrix Factorization including the Singular Value Decomposition, Bases and
  Orthogonalization via
  [Gram-Schmidt](https://en.wikipedia.org/wiki/Gram%E2%80%93Schmidt_process).
* **Differential Equations:** Formulation of differential equations, existence of
  solutions and boundary value requirements, [Sturm-Liouville
  Theory](https://en.wikipedia.org/wiki/Sturm%E2%80%93Liouville_theory).
* **Domain Specific Preparation**: The ability to communicate about and formulate
  complex problems in the student's field of study that would benefit from the
  techniques covered in this course.  Students will expected to actively engage with the
  techniques taught in this course, apply them to relevant problems in their domain of
  expertise, and to communicate about the efficacy to the class.


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
