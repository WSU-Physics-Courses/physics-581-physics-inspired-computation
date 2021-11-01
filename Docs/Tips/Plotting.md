---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.13.0
kernelspec:
  display_name: Python 3 (phys-581-2021)
  language: python
  name: phys-581-2021
---

# Plotting

Here we describe some subtleties about plotting with python.

## [Matplotlib]

[Matplotlib] is the most widely used plotting library available with python and should probably be
your first choice, especially if you need to make high quality two-dimensional plots.
You can do almost anything you want, and can tweak the output to satisfy any needs for
publication (e.g. choosing fonts, vector verses raster graphics, including LaTeX math).
In addition, you will probably find examples about how to do these things in 95% of the
cases with a simple internet search.

The downside is that [Matplotlib] can be slow, and can take a lot of code to implement
these tweaks.  (I budget a solid day of work to get plots ready for publication.)  It
also has very rudimentary support for 3D plotting: if you need to interact with 3D data,
look to other tools like [PyVista] or [MayaVi].

Here we present some tips for using [Matplotlib].

### Jupyter Notebooks

There are a [few
ways](https://medium.com/@Med1um1/using-matplotlib-in-jupyter-notebooks-comparing-methods-and-some-tips-python-c38e85b40ba1)
to get plots working in a [Jupyter Notebook](https://matplotlib.org/stable/users/interactive.html?highlight=jupyter%20notebook#jupyter-notebooks-lab).  I generally recommend using the `%pylab
inline --no-import-all` magic, (but also checkout the `%pylab notebook` magic if you use
notebooks which provides some interactivity.)

I also recommend you create a figure and axes with
[`plt.subplots()`](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.subplots.html)
which allows you to create an array of plots.  With the axes, you can then easily add
labels, etc.

```{margin}
Always include axes labels in your plots!  You will thank yourself later.

Note the use of `aspect=1`.  This is not of much use here, but very important if you
need an accurate comparison of $x$ and $y$ sizes, such as with an image.  The $y=x$ line
here should look like it has unit slope in the right plot.
```

```{code-cell}
%matplotlib inline
import numpy as np, matplotlib.pyplot as plt

x = np.linspace(-1, 1)

fig, axs = plt.subplots(1, 2, figsize=(5, 3))
for ax in axs:
    for p in [1, 2, 3]:
        ax.plot(x, x**p, label=f'$x^{p}$')
    ax.legend()
    ax.set(xlabel='$x$', ylabel='$x^p$')
axs[1].set(aspect=1)  # Needed to properly display angles etc.
plt.tight_layout()  # Adjust axes so they don't collide.
plt.show()  # Not strictly needed, but see below.
```

### LaTeX

You will notice that I am using "LaTeX" to format labels in the previous plot.  I am not
actually using LaTeX, but Matplotlib's
[mathtext](https://matplotlib.org/stable/tutorials/text/mathtext.html).  This is much
faster, but not as flexible as actually using LaTeX.

For publications, you may need to actually use LaTeX.  You can do this by creating a
plot context.  One subtlety is that you must call `plt.show()` **in the context**.  This
is good practice in general (see 
issues [13431](https://github.com/matplotlib/matplotlib/issues/13431) and
[17931](https://github.com/matplotlib/matplotlib/issues/17931) for example).

Here is an example of defining a custom preamble and style:

```{code-cell}
%matplotlib inline
import numpy as np, matplotlib.pyplot as plt

latex_preamble = r"""
\newcommand{\bra}[1]{\vert #1 \rangle}
\newcommand{\ket}[1]{\langle #1 \vert}
\newcommand{\braket}[1]{\langle #1 \rangle}
""".replace("\n", "")  # Strip out newlines


# Here we calculate the exact figure width for a single
# column figure in an APS Physical Review journal.  This
# will ensure that fonts will be the correct size.
columnwidth_pt = 246.0  # From LaTeX \showthe\columnwidth
inches_per_pt = 1.0 / 72.27
width = inches_per_pt * columnwidth_pt
golden_mean = (np.sqrt(5) - 1) / 2

plot_style = {
    "text.latex.preamble": latex_preamble,
    "text.usetex": True,
    "figure.figsize": (width, golden_mean*width),
}

x = np.linspace(-5, 5, 100)
psi0 = np.exp(-x**2/2)/np.pi**(1/4)
psi1 = np.sqrt(2) * x * psi0
with plt.style.context(plot_style, after_reset=True):
    fig, ax = plt.subplots()
    ax.plot(x, psi0, ls='--', label=r"$\braket{x|0}$")
    ax.plot(x, psi1, ls=':', label=r"$\braket{x|1}$")
    ax.legend(loc='best') 
    ax.set(xlabel='$x/r_0$', ylabel=r'$\psi_{n}(x)$')
    plt.show()  # MUST be inside the context.
```

Some important points:

1. LaTeX math must appear between dollar signs `$` in your labels.
2. If you have backslashes in your strings, you need to either escape them, or use [*raw
    strings*](https://docs.python.org/3/reference/lexical_analysis.html?highlight=%22raw%20string%22#string-and-bytes-literals).
    Thus: `"$\\newcommand{\\I}{\\mathrm{i}}$"` or `r"$\newcommand{\I}{\mathrm{i}}$"`.
3. When using contexts, you must call `plt.show()` inside the context. See issues
    [13431](https://github.com/matplotlib/matplotlib/issues/13431) and
    [17931](https://github.com/matplotlib/matplotlib/issues/17931) for example).
4. The `rcParam["text.latex.preamble"]` parameter is [not officially
    supported](https://matplotlib.org/stable/tutorials/text/usetex.html#troubleshooting),
    but extremely powerful.  When things go wrong, you will probably need to look in the
    generated `*.tex` file (located in `~/.matplotlib/tex.cache/*.tex` on my Mac) to see
    why LaTeX is having issues.
    
    ````{admonition} LaTeX Failure Example
    :class: dropdown
    
    For example, if you do not call `plt.show()` in the
    context, the LaTeX will likely fail with an error message like this:
   
    ```
    ---------------------------------------------------------------------------
    CalledProcessError                        Traceback (most recent call last)
    ...
    CalledProcessError: Command '['latex', '-interaction=nonstopmode', '--halt-on-error', '/Users/mforbes/.matplotlib/tex.cache/a24b175253e506052ac2ac5a51792273.tex']' returned non-zero exit status 1.
    ...
    RuntimeError: latex was not able to process the following string:
    b'$\\\\braket{x|0}$'

    Here is the full report generated by latex:
    ...
    ! Undefined control sequence.
    <recently read> \braket 

    l.19 {\sffamily $\braket
                            {x|0}$}
    ...
    ```

    Inspecting the file
    `/Users/mforbes/.matplotlib/tex.cache/a24b175253e506052ac2ac5a51792273.tex` shows
    no sign of the preamble where we defined `\braket`.  This is because the figure is
    actually created after the context is closed, and the `rcParams` have been reset.
    Thus, when LaTeX is actually called, the preamble no longer has our customizations.
    
    ````
    
5. The `rcParam["text.latex.preamble"]` must be a string on a **single line**.  This
    behaviour changed in [3.3.0](https://matplotlib.org//stable/api/prev_api_changes/api_changes_3.3.0.html?highlight=latex%20preamble#setting-rcparams-text-latex-preamble-default-or-rcparams-pdf-preamble-to-non-strings).
   

## Further Reading

* [Software Carpentry: Plotting in Python](https://swcarpentry.github.io/python-novice-gapminder/09-plotting/index.html):
  A short (15min) draft [Software Carpentry] topic about plotting with [Matplotlib].


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
[Matplotlib]: <https://matplotlib.org/> "Matplotlib: Visualization with Python"
[Mayavi]: <https://docs.enthought.com/mayavi/mayavi/> "Mayavi: 3D scientific data visualization and plotting in Python"
[PyVista]: <https://docs.pyvista.org/> "3D plotting and mesh analysis through a streamlined interface for the Visualization Toolkit (VTK)"
