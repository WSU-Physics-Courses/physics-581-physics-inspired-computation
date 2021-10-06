Physics 581: Physics Inspired Computational Techniques
======================================================

[![Documentation Status](https://readthedocs.org/projects/wsu-phys-581-fall-2021/badge/?version=latest)](https://wsu-phys-581-fall-2021.readthedocs.io/en/latest/?badge=latest)
[![pipeline status](https://gitlab.com/wsu-courses/physics-581-physics-inspired-computation/badges/main/pipeline.svg)](https://gitlab.com/wsu-courses/physics-581-physics-inspired-computation/-/commits/main)
[![coverage report](https://gitlab.com/wsu-courses/physics-581-physics-inspired-computation/badges/main/coverage.svg)](https://gitlab.com/wsu-courses/physics-581-physics-inspired-computation/-/commits/main)

This is the main project for the [WSU Physics] course **Physics 518: Physics Inspired
Computational Techniques** first offered in [Fall
2021](https://schedules.wsu.edu/List/Pullman/20213/Phys/581/02).

Physics has a successful track record of providing effective solutions to complex
problems outside its specific domain. This course will focus on using efficient
numerical techniques inspired by physics to solve challenging problems in a wide variety
of applications.  Techniques will be chosen from physics applications, but also applied
to problems outside of the physics domain including economics, biology, sociology, etc.
Students will be introduced to powerful numerical toolkits based on the
[SciPy](https://www.scipy.org/) and [NumFocus](https://numfocus.org) ecosystem. Using
the [CoCalc](https://cocalc.com/) platform will enable rapid development and prototyping
with an explicit path to stable, tested, and performant codes capable of supporting
research, or industry applications.

TL;DR
-----

To use this repository: *(See [Getting Started](#getting-started) for more details.)*

1. *(Optional)* 
   * Create accounts on [CoCalc] and [GitLab], a project on [CoCalc], and a
   repo on [GitLab].  Send your [GitLab] account name to your instructor.
   * Create [Create SSH
   keys](https://doc.cocalc.com/project-settings.html#ssh-keys), and add them [to your
   CoCalc account](https://doc.cocalc.com/account/ssh.html) and [to your GitLab
   account](https://docs.gitlab.com/ee/ssh/).
   * SSH into your [CoCalc] project for the remaining steps.
2. Clone this repo and initialize it:

   ```bash
   git clone https://gitlab.com/wsu-courses/physics-581-physics-inspired-computation.git
   cd physics-581-physics-inspired-computation
   make init
   ```
   
   This will create a [Conda] environment you can activate `conda activate envs/default`,
   and a Jupyter kernel called `phys-581-2021` that you can select from notebooks.
   
3. *(Optional)* 
   * Add your [GitLab] repo as a remote, and push.
   * Create a [GitHub] mirror with automatic push from your [GitLab] repo so you can
     take advantage of their CI.


Overview
--------

One of the things I would like to do is to present each technique from at least two
perspectives:

From scratch
: I feel it is extremely valuable to understand what is at the core
  of an algorithm, and to be able to quickly implement a simplistic "brute force"
  version.  These have the following advantage:
  * Predictable convergence properties.  While often not as accurate or fast as more
    specialized or adaptive routines, simple brute-force versions of an algorithm can
    often be understood completely in terms of convergence properties and/or stability
    with respect to round-off errors etc.  I highly recommend always checking your results
    with a simple brute-force approach to make sure you are not making any mistakes:
  * Occasionally one will need to implement an algorithm from scratch on a specialize
    platform.  For example, to efficiently port code to a GPUs, one must try to remove
    conditionals (`if` statements).  This makes high-precision adaptive routines very
    hard to program, and one  can often gets better performance from a more
    straight-forward brute-force approach. 
  * Related: sometimes high precision is not needed.  In these cases, a simple
    low-accuracy but highly optimized brute-force approach might be fastest.  *(This is
    common in video graphics for example where results need only be accurate to the
    pixel level.)*
  * Having a basic understanding what is happening under "under the hood" of library
    routines can help when those routines fail. 

As fast as possible
: When you need accurate results for research, however, it is also very useful to be
  familiar with library techniques so you can quickly get high-precision results. 
  * If the appropriate technique is implement in a well-tested library, then one can
    often use it in a few lines of code and implement it in a few minutes of time --
    most of which is spent understanding the arguments.  This allows you to get results
    quickly. 
  * These techniques tend to be adaptive, spending more time where the problem is hard
    to achieve desired tolerance objectives.  If you need performance, you can reduce
    the tolerance. 
   * Unfortunately, adaptive routines can skip over the hard stuff, giving incorrect
     results that may seem reasonable at first.  There is no substitute for
     understanding your problem. 
  * It can be hard to understand exactly what black-box library routines are doing, and
    hence hard to understand their convergence properties.  It is essential to check your
    results with different techniques, or, at a minimum, with different resolutions. 
      > **Definition 16 (IDIOT)** *Anyone who publishes a calculation without checking it
      > against an identical computation with smaller $N$ OR without evaluating the 
      > residual of the pseudospectral approximation via finite differences is an IDIOT.*
      *(J. P. Boyd: Chebyshev and Fourier Spectral Methods {cite:p}`Boyd:1989`)* 

## Software Carpentry

Another objective of the course is to provide students with good software carpentry
skills.  This includes using version control, documenting code, testing, code-coverage,
and continuous integration (CI).  In particular, students are expected to fork this
repository and maintain their own [GitLab] repository with fully tested code.
Assignments will be distributed in the form of tests which the students must provide
functions which pass these tests.

* Students will be expected to maintain their code under version control.
* Code must be tested with unit tests providing at least 85% code coverage.
* Code must meet certain quality metrics, including documenting behaviour,
  inputs/outputs, specifying interfaces etc.

As part of the course, I will provide a detailed explanation of how to use tools like
[pytest](https://docs.pytest.org), [Coverage.py](https://coverage.readthedocs.io),
[Flake8](https://flake8.pycqa.org) and new tools like [LGTM](https://lgtm.com/) that
provide security analyses of code for Python-based projects to satisfying all of these
objectives.  With continuous integration techniques, these tests can be run whenever
code is committed, helping maintain functioning, well-tested code.

This repository provides a skeleton satisfying these requirements, and demonstrating how
to write proper tests, use [GitLab]s continuous integration, and to generate
documentation for Python.  *(Students wishing to use other languages will need to learn
how to use similar tools on their own.)*

Justification
: * Thinking about how to test code can significantly help in understanding the
    techniques and the problems. A significant portion of the course will address this
    issue.  For example: How can one find non-trivial problems with analytic solutions
    for testing?  What if such problems cannot be found? How should the algorithms
    converge?  Is appropriate convergence being achieved? *(Answering this later
    question quantitatively can provide for very useful test cases.)*
  * These skills will definitely be of benefit to anyone looking later for a career in
    industry, but will also help in maintaining code in a research setting.
  * The repository of code developed for this course can serve as a future portfolio.
  * Working tests serve as a demonstration of how to use the code, thereby functioning
    in some sense as documentation examples that are checked.

## Project Structure

This project is structured 

## Getting Started

These are complete instructions for students to get started working with this project
for use in the course and include managing a [GitLab] repository, with automated testing
etc.

1. *(Optional)* Create an account and project on [CoCalc].  If you are taking the
   course, then you should use the project you are invited to join as part of the
   course.  The instructions will generally assume you are working in the [CoCalc]
   project, but things will probably work out-of-the-box on Linux machines or Mac OS
   X. (No guarantees with Windows or other platforms.)  If you encounter any problems,
   please [file an issue].
   
   If you plan to use [CoCalc], then either complete the remaining steps using an [Online
   Linux Terminal](https://cocalc.com/doc/terminal.html) in your project, or by
   [connecting to CoCalc with
   SSH](https://doc.cocalc.com/project-settings.html#ssh-keys).
   
   If you are running this on another platform, you must make sure that you have a
   [Conda] environment setup with `anaconda-project >= 0.8.4`.  You can do this easily
   by installing [Miniconda], then either updating the `base` environment:
   
   ```console
   (base) $ conda install anaconda-project
   (base) $ anaconda-project ...
   ```

   or creating a new environment with `anaconda-project`:
   
   ```console
   (base) $ conda create -n myenv anaconda-project
   (base) $ conda activate myenv
   (myenv) $ anaconda-project ...
   ```

   <details><summary>Example session with Mac OS X</summary>
   
   ```console
   # Download Miniconda installer
   MacOSX $ curl -O https://repo.anaconda.com/miniconda/Miniconda3-py39_4.10.3-MacOSX-x86_64.sh
      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                    Dload  Upload   Total   Spent    Left  Speed
   100 42.3M  100 42.3M    0     0  22.8M      0  0:00:01  0:00:01 --:--:-- 22.8M
 
   # Check that it was not corrupted with the SHA 256 value listed on the website
   MacOSX $ shasum -a 256 Miniconda3-py39_4.10.3-MacOSX-x86_64.sh
   786de9721f43e2c7d2803144c635f5f6e4823483536dc141ccd82dbb927cd508  Miniconda3-py39_4.10.3-MacOSX-x86_64.sh

   # Install Miniconda in the current directory
   MacOSX $ bash Miniconda3-py39_4.10.3-MacOSX-x86_64.sh -b -p ./miniconda3
   PREFIX=/Users/mforbes/.../miniconda3
   Unpacking payload ...
   Collecting package metadata (current_repodata.json): done                                                                                
   Solving environment: done

   ## Package Plan ##

     environment location: /Users/mforbes/.../miniconda3

     added / updated specs:
       - brotlipy==0.7.0=py39h9ed2024_1003
       - ca-certificates==2021.7.5=hecd8cb5_1
       - certifi==2021.5.30=py39hecd8cb5_0
       - cffi==1.14.6=py39h2125817_0
       - chardet==4.0.0=py39hecd8cb5_1003
       - conda-package-handling==1.7.3=py39h9ed2024_1
       - conda==4.10.3=py39hecd8cb5_0
       - cryptography==3.4.7=py39h2fd3fbb_0
       - idna==2.10=pyhd3eb1b0_0
       - libcxx==10.0.0=1
       - libffi==3.3=hb1e8313_2
       - ncurses==6.2=h0a44026_1
       - openssl==1.1.1k=h9ed2024_0
       - pip==21.1.3=py39hecd8cb5_0
       - pycosat==0.6.3=py39h9ed2024_0
       - pycparser==2.20=py_2
       - pyopenssl==20.0.1=pyhd3eb1b0_1
       - pysocks==1.7.1=py39hecd8cb5_0
       - python.app==3=py39h9ed2024_0
       - python==3.9.5=h88f2d9e_3
       - readline==8.1=h9ed2024_0
       - requests==2.25.1=pyhd3eb1b0_0
       - ruamel_yaml==0.15.100=py39h9ed2024_0
       - setuptools==52.0.0=py39hecd8cb5_0
       - six==1.16.0=pyhd3eb1b0_0
       - sqlite==3.36.0=hce871da_0
       - tk==8.6.10=hb0a8c7a_0
       - tqdm==4.61.2=pyhd3eb1b0_1
       - tzdata==2021a=h52ac0ba_0
       - urllib3==1.26.6=pyhd3eb1b0_1
       - wheel==0.36.2=pyhd3eb1b0_0
       - xz==5.2.5=h1de35cc_0
       - yaml==0.2.5=haf1e3a3_0
       - zlib==1.2.11=h1de35cc_3


   The following NEW packages will be INSTALLED:

     brotlipy           pkgs/main/osx-64::brotlipy-0.7.0-py39h9ed2024_1003
     ca-certificates    pkgs/main/osx-64::ca-certificates-2021.7.5-hecd8cb5_1
     certifi            pkgs/main/osx-64::certifi-2021.5.30-py39hecd8cb5_0
     cffi               pkgs/main/osx-64::cffi-1.14.6-py39h2125817_0
     chardet            pkgs/main/osx-64::chardet-4.0.0-py39hecd8cb5_1003
     conda              pkgs/main/osx-64::conda-4.10.3-py39hecd8cb5_0
     conda-package-han~ pkgs/main/osx-64::conda-package-handling-1.7.3-py39h9ed2024_1
     cryptography       pkgs/main/osx-64::cryptography-3.4.7-py39h2fd3fbb_0
     idna               pkgs/main/noarch::idna-2.10-pyhd3eb1b0_0
     libcxx             pkgs/main/osx-64::libcxx-10.0.0-1
     libffi             pkgs/main/osx-64::libffi-3.3-hb1e8313_2
     ncurses            pkgs/main/osx-64::ncurses-6.2-h0a44026_1
     openssl            pkgs/main/osx-64::openssl-1.1.1k-h9ed2024_0
     pip                pkgs/main/osx-64::pip-21.1.3-py39hecd8cb5_0
     pycosat            pkgs/main/osx-64::pycosat-0.6.3-py39h9ed2024_0
     pycparser          pkgs/main/noarch::pycparser-2.20-py_2
     pyopenssl          pkgs/main/noarch::pyopenssl-20.0.1-pyhd3eb1b0_1
     pysocks            pkgs/main/osx-64::pysocks-1.7.1-py39hecd8cb5_0
     python             pkgs/main/osx-64::python-3.9.5-h88f2d9e_3
     python.app         pkgs/main/osx-64::python.app-3-py39h9ed2024_0
     readline           pkgs/main/osx-64::readline-8.1-h9ed2024_0
     requests           pkgs/main/noarch::requests-2.25.1-pyhd3eb1b0_0
     ruamel_yaml        pkgs/main/osx-64::ruamel_yaml-0.15.100-py39h9ed2024_0
     setuptools         pkgs/main/osx-64::setuptools-52.0.0-py39hecd8cb5_0
     six                pkgs/main/noarch::six-1.16.0-pyhd3eb1b0_0
     sqlite             pkgs/main/osx-64::sqlite-3.36.0-hce871da_0
     tk                 pkgs/main/osx-64::tk-8.6.10-hb0a8c7a_0
     tqdm               pkgs/main/noarch::tqdm-4.61.2-pyhd3eb1b0_1
     tzdata             pkgs/main/noarch::tzdata-2021a-h52ac0ba_0
     urllib3            pkgs/main/noarch::urllib3-1.26.6-pyhd3eb1b0_1
     wheel              pkgs/main/noarch::wheel-0.36.2-pyhd3eb1b0_0
     xz                 pkgs/main/osx-64::xz-5.2.5-h1de35cc_0
     yaml               pkgs/main/osx-64::yaml-0.2.5-haf1e3a3_0
     zlib               pkgs/main/osx-64::zlib-1.2.11-h1de35cc_3


   Preparing transaction: done
   Executing transaction: - 
   done
   installation finished.

   # Check the sizes
   MacOSX $ du -sh *
    42M	Miniconda3-py39_4.10.3-MacOSX-x86_64.sh
   208M	miniconda3

   # Activate the base environment
   MacOSX $ . miniconda3/bin/activate
   (base) MacOSX $ which conda
   /Users/mforbes/.../tmp/miniconda3/bin/conda
   
   # Optional: initialize your shell - modifies ~/.bash_profile
   (base) MacOSX $ conda init
   no change     /Users/mforbes/.../tmp/miniconda3/condabin/conda
   ...
   modified      /Users/mforbes/.bash_profile

   # Install anaconda-project in the base environment
   (base) MacOSX $ conda install -qy anaconda-project
   Collecting package metadata (current_repodata.json): ...working... done
   Solving environment: ...working... done

   ## Package Plan ##

     environment location: /Users/mforbes/.../tmp/miniconda3

     added / updated specs:
       - anaconda-project


   The following packages will be downloaded:

       package                    |            build
       ---------------------------|-----------------
       anaconda-client-1.8.0      |   py39hecd8cb5_0         153 KB
       anaconda-project-0.10.1    |     pyhd3eb1b0_0         218 KB
       attrs-21.2.0               |     pyhd3eb1b0_0          46 KB
       clyent-1.2.2               |   py39hecd8cb5_1          21 KB
       conda-pack-0.6.0           |     pyhd3eb1b0_0          29 KB
       importlib-metadata-3.10.0  |   py39hecd8cb5_0          33 KB
       ipython_genutils-0.2.0     |     pyhd3eb1b0_1          27 KB
       jsonschema-3.2.0           |             py_2          47 KB
       jupyter_core-4.7.1         |   py39hecd8cb5_0          68 KB
       markupsafe-2.0.1           |   py39h9ed2024_0          20 KB
       nbformat-5.1.3             |     pyhd3eb1b0_0          44 KB
       pytz-2021.1                |     pyhd3eb1b0_0         181 KB
       pyyaml-5.4.1               |   py39h9ed2024_1         170 KB
       tornado-6.1                |   py39h9ed2024_0         587 KB
       traitlets-5.0.5            |     pyhd3eb1b0_0          81 KB
       zipp-3.5.0                 |     pyhd3eb1b0_0          13 KB
       ------------------------------------------------------------
                                              Total:         1.7 MB

   The following NEW packages will be INSTALLED:

     anaconda-client    pkgs/main/osx-64::anaconda-client-1.8.0-py39hecd8cb5_0
     anaconda-project   pkgs/main/noarch::anaconda-project-0.10.1-pyhd3eb1b0_0
     attrs              pkgs/main/noarch::attrs-21.2.0-pyhd3eb1b0_0
     clyent             pkgs/main/osx-64::clyent-1.2.2-py39hecd8cb5_1
     conda-pack         pkgs/main/noarch::conda-pack-0.6.0-pyhd3eb1b0_0
     importlib-metadata pkgs/main/osx-64::importlib-metadata-3.10.0-py39hecd8cb5_0
     importlib_metadata pkgs/main/noarch::importlib_metadata-3.10.0-hd3eb1b0_0
     ipython_genutils   pkgs/main/noarch::ipython_genutils-0.2.0-pyhd3eb1b0_1
     jinja2             pkgs/main/noarch::jinja2-3.0.1-pyhd3eb1b0_0
     jsonschema         pkgs/main/noarch::jsonschema-3.2.0-py_2
     jupyter_core       pkgs/main/osx-64::jupyter_core-4.7.1-py39hecd8cb5_0
     markupsafe         pkgs/main/osx-64::markupsafe-2.0.1-py39h9ed2024_0
     nbformat           pkgs/main/noarch::nbformat-5.1.3-pyhd3eb1b0_0
     pyrsistent         pkgs/main/osx-64::pyrsistent-0.18.0-py39h9ed2024_0
     python-dateutil    pkgs/main/noarch::python-dateutil-2.8.2-pyhd3eb1b0_0
     pytz               pkgs/main/noarch::pytz-2021.1-pyhd3eb1b0_0
     pyyaml             pkgs/main/osx-64::pyyaml-5.4.1-py39h9ed2024_1
     tornado            pkgs/main/osx-64::tornado-6.1-py39h9ed2024_0
     traitlets          pkgs/main/noarch::traitlets-5.0.5-pyhd3eb1b0_0
     zipp               pkgs/main/noarch::zipp-3.5.0-pyhd3eb1b0_0

   The following packages will be UPDATED:

     openssl                                 1.1.1k-h9ed2024_0 --> 1.1.1l-h9ed2024_0


   Preparing transaction: ...working... done
   Verifying transaction: ...working... done
   Executing transaction: ...working... done
   
   # Check disk usage
   (base) MacOSX $ du -sh *
    42M	Miniconda3-py39_4.10.3-MacOSX-x86_64.sh
   247M	miniconda3

   # Optional: Clean up downloaded packages 
   (base) MacOSX $ rm Miniconda3-py39_4.10.3-MacOSX-x86_64.sh
   (base) MacOSX $ conda clean --all -y
   ...
   (base) MacOSX $ du -sh *
   191M	miniconda3
   
   # Alternatively, create a new environment
   (base) MacOSX $ conda create -qy -n myenv anaconda-project
   Collecting package metadata (current_repodata.json): ...working... done
   Solving environment: ...working... done

   ## Package Plan ##

     environment location: /Users/mforbes/current/courses/581/Course/tmp/miniconda3/envs/myenv

     added / updated specs:
       - anaconda-project


   The following packages will be downloaded:

       package                    |            build
       ---------------------------|-----------------
       anaconda-client-1.8.0      |   py39hecd8cb5_0         153 KB
       anaconda-project-0.10.1    |     pyhd3eb1b0_0         218 KB
       attrs-21.2.0               |     pyhd3eb1b0_0          46 KB
       clyent-1.2.2               |   py39hecd8cb5_1          21 KB
       conda-pack-0.6.0           |     pyhd3eb1b0_0          29 KB
       importlib-metadata-3.10.0  |   py39hecd8cb5_0          33 KB
       importlib_metadata-3.10.0  |       hd3eb1b0_0          11 KB
       ipython_genutils-0.2.0     |     pyhd3eb1b0_1          27 KB
       jsonschema-3.2.0           |             py_2          47 KB
       jupyter_core-4.7.1         |   py39hecd8cb5_0          68 KB
       markupsafe-2.0.1           |   py39h9ed2024_0          20 KB
       nbformat-5.1.3             |     pyhd3eb1b0_0          44 KB
       pytz-2021.1                |     pyhd3eb1b0_0         181 KB
       pyyaml-5.4.1               |   py39h9ed2024_1         170 KB
       tornado-6.1                |   py39h9ed2024_0         587 KB
       traitlets-5.0.5            |     pyhd3eb1b0_0          81 KB
       zipp-3.5.0                 |     pyhd3eb1b0_0          13 KB
       ------------------------------------------------------------
                                              Total:         1.7 MB

   The following NEW packages will be INSTALLED:

     anaconda-client    pkgs/main/osx-64::anaconda-client-1.8.0-py39hecd8cb5_0
     anaconda-project   pkgs/main/noarch::anaconda-project-0.10.1-pyhd3eb1b0_0
     attrs              pkgs/main/noarch::attrs-21.2.0-pyhd3eb1b0_0
     brotlipy           pkgs/main/osx-64::brotlipy-0.7.0-py39h9ed2024_1003
     ca-certificates    pkgs/main/osx-64::ca-certificates-2021.7.5-hecd8cb5_1
     certifi            pkgs/main/osx-64::certifi-2021.5.30-py39hecd8cb5_0
     cffi               pkgs/main/osx-64::cffi-1.14.6-py39h2125817_0
     charset-normalizer pkgs/main/noarch::charset-normalizer-2.0.4-pyhd3eb1b0_0
     clyent             pkgs/main/osx-64::clyent-1.2.2-py39hecd8cb5_1
     conda-pack         pkgs/main/noarch::conda-pack-0.6.0-pyhd3eb1b0_0
     cryptography       pkgs/main/osx-64::cryptography-3.4.7-py39h2fd3fbb_0
     idna               pkgs/main/noarch::idna-3.2-pyhd3eb1b0_0
     importlib-metadata pkgs/main/osx-64::importlib-metadata-3.10.0-py39hecd8cb5_0
     importlib_metadata pkgs/main/noarch::importlib_metadata-3.10.0-hd3eb1b0_0
     ipython_genutils   pkgs/main/noarch::ipython_genutils-0.2.0-pyhd3eb1b0_1
     jinja2             pkgs/main/noarch::jinja2-3.0.1-pyhd3eb1b0_0
     jsonschema         pkgs/main/noarch::jsonschema-3.2.0-py_2
     jupyter_core       pkgs/main/osx-64::jupyter_core-4.7.1-py39hecd8cb5_0
     libcxx             pkgs/main/osx-64::libcxx-10.0.0-1
     libffi             pkgs/main/osx-64::libffi-3.3-hb1e8313_2
     markupsafe         pkgs/main/osx-64::markupsafe-2.0.1-py39h9ed2024_0
     nbformat           pkgs/main/noarch::nbformat-5.1.3-pyhd3eb1b0_0
     ncurses            pkgs/main/osx-64::ncurses-6.2-h0a44026_1
     openssl            pkgs/main/osx-64::openssl-1.1.1l-h9ed2024_0
     pip                pkgs/main/osx-64::pip-21.2.4-py37hecd8cb5_0
     pycparser          pkgs/main/noarch::pycparser-2.20-py_2
     pyopenssl          pkgs/main/noarch::pyopenssl-20.0.1-pyhd3eb1b0_1
     pyrsistent         pkgs/main/osx-64::pyrsistent-0.18.0-py39h9ed2024_0
     pysocks            pkgs/main/osx-64::pysocks-1.7.1-py39hecd8cb5_0
     python             pkgs/main/osx-64::python-3.9.6-h88f2d9e_1
     python-dateutil    pkgs/main/noarch::python-dateutil-2.8.2-pyhd3eb1b0_0
     pytz               pkgs/main/noarch::pytz-2021.1-pyhd3eb1b0_0
     pyyaml             pkgs/main/osx-64::pyyaml-5.4.1-py39h9ed2024_1
     readline           pkgs/main/osx-64::readline-8.1-h9ed2024_0
     requests           pkgs/main/noarch::requests-2.26.0-pyhd3eb1b0_0
     ruamel_yaml        pkgs/main/osx-64::ruamel_yaml-0.15.100-py39h9ed2024_0
     setuptools         pkgs/main/osx-64::setuptools-52.0.0-py39hecd8cb5_0
     six                pkgs/main/noarch::six-1.16.0-pyhd3eb1b0_0
     sqlite             pkgs/main/osx-64::sqlite-3.36.0-hce871da_0
     tk                 pkgs/main/osx-64::tk-8.6.10-hb0a8c7a_0
     tornado            pkgs/main/osx-64::tornado-6.1-py39h9ed2024_0
     tqdm               pkgs/main/noarch::tqdm-4.62.1-pyhd3eb1b0_1
     traitlets          pkgs/main/noarch::traitlets-5.0.5-pyhd3eb1b0_0
     tzdata             pkgs/main/noarch::tzdata-2021a-h5d7bf9c_0
     urllib3            pkgs/main/noarch::urllib3-1.26.6-pyhd3eb1b0_1
     wheel              pkgs/main/noarch::wheel-0.37.0-pyhd3eb1b0_0
     xz                 pkgs/main/osx-64::xz-5.2.5-h1de35cc_0
     yaml               pkgs/main/osx-64::yaml-0.2.5-haf1e3a3_0
     zipp               pkgs/main/noarch::zipp-3.5.0-pyhd3eb1b0_0
     zlib               pkgs/main/osx-64::zlib-1.2.11-h1de35cc_3


   Preparing transaction: ...working... done
   Verifying transaction: ...working... done
   Executing transaction: ...working... done
   (base) MacOSX $ conda activate myenv
   (myenv) MacOSX $ type python3
   python3 is /Users/mforbes/.../tmp/miniconda3/envs/myenv/bin/python3

   # Optionally clean:
   (myenv) MacOSX $ conda clean --all -y
   ...
   (myenv) MacOSX $ du -sh *
   278M	miniconda3
   ```
   </details>

   
2. Clone this repo and change directories to enter the project:

   ```bash
   git clone https://gitlab.com/wsu-courses/physics-581-physics-inspired-computation.git
   cd physics-581-physics-inspired-computation
   ```
   
   *Note: I actually prefer to use [Mercurial] and usually use the [hg-git] plugin, but
   don't recommend this unless you are very familiar with [Mercurial].  See
   {ref}`sec:version-control` for more details: `Hi`*
   
   ```bash
   hg clone https://gitlab.com/wsu-courses/physics-581-physics-inspired-computation.git
   cd physics-581-physics-inspired-computation
   ```
   
3. Use [`anaconda-project`](https://anaconda-project.readthedocs.io/en/latest/) to
   provision the environment, setup the kernel, clone the resources, etc.  This can all
   be done with:

   ```bash
   make init
   ```
   
   Which will do the following:
   
   1. Clone the [Resources project] project into `_ext/Resources`.  Note: this is
      private and requires that your instructor grant you access.
   2. Run `anaconda-project prepare` which uses `conda` or `mamba` to create an
      environment in `envs/phys-581-2021` as specified in the `anaconda-project.yaml`
      file. *(This may take some time when you first run it, and consumes about 2GB of
      disk space.  You can clean up some space after by running `make clean`.)*
   3. Installs this environment as an [IPython
      kernel](https://ipython.readthedocs.io/en/stable/install/kernel_install.html)
      called `phys-581-2021` for use with [Jupyter].  This is done by running
      `anaconda-project run init` which runs [`ipykernel
      install`](https://ipython.readthedocs.io/en/stable/install/kernel_install.html):
      see the `init` target in `anaconda-project.yml` for details.
   4. If you are on [CoCalc] *(technically, if `ANACONDA2020` is defined)*, then `make
      init` will also install the `mmf-setup` package, update some files, create a
      `~/.bash_aliases` file, and insert a line to activate the environment when logging
      in.  This also then runs `make sync` which uses [Jupytext] to populate the
      notebooks so you can use them with [CoCalc].

   <details><summary>Example session on Mac OS X</summary>
   
   In the following, I have already authenticated to my SSH keys which I have registered
   at [GitLab], so there is no need for passwords.
   
   ```console
   (myenv) MacOSX $ git clone git@gitlab.com:wsu-courses/physics-581-physics-inspired-computation.git
   Cloning into 'physics-581-physics-inspired-computation'...
   remote: Enumerating objects: 269, done.
   remote: Counting objects: 100% (98/98), done.
   remote: Compressing objects: 100% (59/59), done.
   remote: Total 269 (delta 53), reused 76 (delta 39), pack-reused 171
   Receiving objects: 100% (269/269), 201.54 KiB | 1.10 MiB/s, done.
   Resolving deltas: 100% (129/129), done.

   (myenv) MacOSX $ cd physics-581-physics-inspired-computation
   (myenv) MacOSX $ ls
   Docs			Notes.md		Resources		anaconda-project.yaml	poetry.lock		tests
   Makefile		README.md		Topics			phys_581_2021		pyproject.toml
   
   (myenv) MacOSX $ make init
   $ make init
   git clone git@gitlab.com:wsu-courses/physics-581-physics-inspired-computation_resources.git _ext/Resources
   Cloning into '_ext/Resources'...
   remote: Enumerating objects: 10, done.
   remote: Counting objects: 100% (10/10), done.
   remote: Compressing objects: 100% (9/9), done.
   remote: Total 10 (delta 0), reused 0 (delta 0), pack-reused 0
   Receiving objects: 100% (10/10), 20.22 MiB | 8.09 MiB/s, done.
   CONDA_EXE=/data/apps/conda/bin/conda anaconda-project prepare
   Collecting package metadata (current_repodata.json): ...working... done
   Solving environment: ...working... failed with repodata from current_repodata.json, will retry with next repodata source.
   Collecting package metadata (repodata.json): ...working... done
   Solving environment: ...working... done

   ## Package Plan ##

     environment location: /Users/mforbes/.../tmp/physics-581-physics-inspired-computation/envs/phys-581-2021

     added / updated specs:
       - anaconda-project[version='>=0.10.1']
       - black
       - conda-forge::myst-nb
       - conda-forge::sphinx-autobuild
       - conda-forge::sphinx-book-theme
       - conda-forge::sphinx-panels
       - conda-forge::uncertainties
       - jupytext
       - matplotlib
       - pandas
       - pip
       - pytest-cov
       - pytest-flake8
       - pytest-xdist
       - python=3.9
       - scipy
       - sphinx


   The following packages will be downloaded:

       package                    |            build
       ---------------------------|-----------------
       blas-1.0                   |              mkl           6 KB
       importlib_metadata-3.10.0  |       hd3eb1b0_0          11 KB
       matplotlib-3.4.2           |   py39hecd8cb5_0          26 KB
       numpy-1.20.3               |   py39h4b4dc7a_0          23 KB
       python_abi-3.9             |           2_cp39           4 KB  conda-forge
       typing-extensions-3.10.0.0 |       hd3eb1b0_0           8 KB
       ------------------------------------------------------------
                                              Total:          78 KB

   The following NEW packages will be INSTALLED:

     alabaster          pkgs/main/noarch::alabaster-0.7.12-pyhd3eb1b0_0
     anaconda-client    pkgs/main/osx-64::anaconda-client-1.8.0-py39hecd8cb5_0
     anaconda-project   pkgs/main/noarch::anaconda-project-0.10.1-pyhd3eb1b0_0
     anyio              pkgs/main/osx-64::anyio-2.2.0-py39hecd8cb5_1
     appdirs            pkgs/main/noarch::appdirs-1.4.4-py_0
     appnope            pkgs/main/osx-64::appnope-0.1.2-py39hecd8cb5_1001
     argon2-cffi        pkgs/main/osx-64::argon2-cffi-20.1.0-py39h9ed2024_1
     async_generator    pkgs/main/noarch::async_generator-1.10-pyhd3eb1b0_0
     attrs              pkgs/main/noarch::attrs-20.3.0-pyhd3eb1b0_0
     babel              pkgs/main/noarch::babel-2.9.1-pyhd3eb1b0_0
     backcall           pkgs/main/noarch::backcall-0.2.0-pyhd3eb1b0_0
     beautifulsoup4     pkgs/main/noarch::beautifulsoup4-4.9.3-pyha847dfd_0
     black              pkgs/main/noarch::black-19.10b0-py_0
     blas               pkgs/main/osx-64::blas-1.0-mkl
     bleach             pkgs/main/noarch::bleach-4.0.0-pyhd3eb1b0_0
     bottleneck         pkgs/main/osx-64::bottleneck-1.3.2-py39he3068b8_1
     brotli             pkgs/main/osx-64::brotli-1.0.9-hb1e8313_2
     brotlipy           pkgs/main/osx-64::brotlipy-0.7.0-py39h9ed2024_1003
     ca-certificates    pkgs/main/osx-64::ca-certificates-2021.7.5-hecd8cb5_1
     certifi            pkgs/main/osx-64::certifi-2021.5.30-py39hecd8cb5_0
     cffi               pkgs/main/osx-64::cffi-1.14.6-py39h2125817_0
     charset-normalizer pkgs/main/noarch::charset-normalizer-2.0.4-pyhd3eb1b0_0
     click              pkgs/main/noarch::click-8.0.1-pyhd3eb1b0_0
     click-completion   conda-forge/osx-64::click-completion-0.5.2-py39h6e9494a_2
     click-log          conda-forge/noarch::click-log-0.3.2-pyh9f0ad1d_0
     clyent             pkgs/main/osx-64::clyent-1.2.2-py39hecd8cb5_1
     colorama           pkgs/main/noarch::colorama-0.4.4-pyhd3eb1b0_0
     conda-pack         pkgs/main/noarch::conda-pack-0.6.0-pyhd3eb1b0_0
     coverage           pkgs/main/osx-64::coverage-5.5-py39h9ed2024_2
     cryptography       pkgs/main/osx-64::cryptography-3.4.7-py39h2fd3fbb_0
     cycler             pkgs/main/osx-64::cycler-0.10.0-py39hecd8cb5_0
     debugpy            pkgs/main/osx-64::debugpy-1.4.1-py39h23ab428_0
     decorator          pkgs/main/noarch::decorator-5.0.9-pyhd3eb1b0_0
     defusedxml         pkgs/main/noarch::defusedxml-0.7.1-pyhd3eb1b0_0
     docutils           pkgs/main/osx-64::docutils-0.16-py39hecd8cb5_1
     entrypoints        pkgs/main/osx-64::entrypoints-0.3-py39hecd8cb5_0
     execnet            pkgs/main/noarch::execnet-1.9.0-pyhd3eb1b0_0
     flake8             pkgs/main/noarch::flake8-3.9.2-pyhd3eb1b0_0
     fonttools          pkgs/main/noarch::fonttools-4.25.0-pyhd3eb1b0_0
     freetype           pkgs/main/osx-64::freetype-2.10.4-ha233b18_0
     future             pkgs/main/osx-64::future-0.18.2-py39hecd8cb5_1
     gitdb              pkgs/main/noarch::gitdb-4.0.7-pyhd3eb1b0_0
     gitpython          pkgs/main/noarch::gitpython-3.1.18-pyhd3eb1b0_1
     greenlet           pkgs/main/osx-64::greenlet-1.1.1-py39h23ab428_0
     idna               pkgs/main/noarch::idna-3.2-pyhd3eb1b0_0
     imagesize          pkgs/main/noarch::imagesize-1.2.0-pyhd3eb1b0_0
     importlib-metadata pkgs/main/osx-64::importlib-metadata-3.10.0-py39hecd8cb5_0
     importlib_metadata pkgs/main/noarch::importlib_metadata-3.10.0-hd3eb1b0_0
     importlib_resourc~ pkgs/main/osx-64::importlib_resources-3.3.1-py39hecd8cb5_0
     iniconfig          pkgs/main/noarch::iniconfig-1.1.1-pyhd3eb1b0_0
     intel-openmp       pkgs/main/osx-64::intel-openmp-2021.3.0-hecd8cb5_3375
     ipykernel          pkgs/main/osx-64::ipykernel-6.2.0-py39hecd8cb5_1
     ipython            pkgs/main/osx-64::ipython-7.26.0-py39h01d92e1_0
     ipython_genutils   pkgs/main/noarch::ipython_genutils-0.2.0-pyhd3eb1b0_1
     ipywidgets         pkgs/main/noarch::ipywidgets-7.6.3-pyhd3eb1b0_1
     jedi               pkgs/main/osx-64::jedi-0.18.0-py39hecd8cb5_1
     jinja2             pkgs/main/noarch::jinja2-3.0.1-pyhd3eb1b0_0
     jpeg               pkgs/main/osx-64::jpeg-9b-he5867d9_2
     jsonschema         pkgs/main/noarch::jsonschema-3.2.0-py_2
     jupyter-cache      conda-forge/noarch::jupyter-cache-0.4.3-pyhd8ed1ab_0
     jupyter-server-ma~ conda-forge/noarch::jupyter-server-mathjax-0.2.3-pyhd8ed1ab_0
     jupyter-sphinx     conda-forge/noarch::jupyter-sphinx-0.3.2-py_0
     jupyter_client     pkgs/main/noarch::jupyter_client-6.1.12-pyhd3eb1b0_0
     jupyter_core       pkgs/main/osx-64::jupyter_core-4.7.1-py39hecd8cb5_0
     jupyter_server     pkgs/main/osx-64::jupyter_server-1.4.1-py39hecd8cb5_0
     jupyterlab_widgets pkgs/main/noarch::jupyterlab_widgets-1.0.0-pyhd3eb1b0_1
     jupytext           conda-forge/noarch::jupytext-1.11.1-pyh44b312d_0
     kiwisolver         pkgs/main/osx-64::kiwisolver-1.3.1-py39h23ab428_0
     lcms2              pkgs/main/osx-64::lcms2-2.12-hf1fd2bf_0
     libcxx             pkgs/main/osx-64::libcxx-10.0.0-1
     libffi             pkgs/main/osx-64::libffi-3.3-hb1e8313_2
     libgfortran        pkgs/main/osx-64::libgfortran-3.0.1-h93005f0_2
     libpng             pkgs/main/osx-64::libpng-1.6.37-ha441bb4_0
     libsodium          pkgs/main/osx-64::libsodium-1.0.18-h1de35cc_0
     libtiff            pkgs/main/osx-64::libtiff-4.2.0-h87d7836_0
     libwebp-base       pkgs/main/osx-64::libwebp-base-1.2.0-h9ed2024_0
     livereload         conda-forge/noarch::livereload-2.6.3-pyh9f0ad1d_0
     lz4-c              pkgs/main/osx-64::lz4-c-1.9.3-h23ab428_1
     markdown-it-py     conda-forge/noarch::markdown-it-py-0.6.2-pyhd8ed1ab_0
     markupsafe         pkgs/main/osx-64::markupsafe-2.0.1-py39h9ed2024_0
     matplotlib         pkgs/main/osx-64::matplotlib-3.4.2-py39hecd8cb5_0
     matplotlib-base    pkgs/main/osx-64::matplotlib-base-3.4.2-py39h8b3ea08_0
     matplotlib-inline  pkgs/main/noarch::matplotlib-inline-0.1.2-pyhd3eb1b0_2
     mccabe             pkgs/main/osx-64::mccabe-0.6.1-py39hecd8cb5_1
     mdit-py-plugins    conda-forge/noarch::mdit-py-plugins-0.2.6-pyhd8ed1ab_0
     mistune            pkgs/main/osx-64::mistune-0.8.4-py39h9ed2024_1000
     mkl                pkgs/main/osx-64::mkl-2021.3.0-hecd8cb5_517
     mkl-service        pkgs/main/osx-64::mkl-service-2.4.0-py39h9ed2024_0
     mkl_fft            pkgs/main/osx-64::mkl_fft-1.3.0-py39h4a7008c_2
     mkl_random         pkgs/main/osx-64::mkl_random-1.2.2-py39hb2f4e1b_0
     more-itertools     pkgs/main/noarch::more-itertools-8.8.0-pyhd3eb1b0_0
     munkres            pkgs/main/noarch::munkres-1.1.4-py_0
     mypy_extensions    pkgs/main/osx-64::mypy_extensions-0.4.3-py39hecd8cb5_0
     myst-nb            conda-forge/noarch::myst-nb-0.12.3-pyhd8ed1ab_0
     myst-parser        conda-forge/noarch::myst-parser-0.13.7-pyhd8ed1ab_0
     nbclient           pkgs/main/noarch::nbclient-0.5.3-pyhd3eb1b0_0
     nbconvert          pkgs/main/noarch::nbconvert-5.5.0-py_0
     nbdime             conda-forge/noarch::nbdime-3.1.0-pyhd8ed1ab_0
     nbformat           pkgs/main/noarch::nbformat-5.1.3-pyhd3eb1b0_0
     ncurses            pkgs/main/osx-64::ncurses-6.2-h0a44026_1
     nest-asyncio       pkgs/main/noarch::nest-asyncio-1.5.1-pyhd3eb1b0_0
     notebook           pkgs/main/osx-64::notebook-6.4.3-py39hecd8cb5_0
     numexpr            pkgs/main/osx-64::numexpr-2.7.3-py39h5873af2_1
     numpy              pkgs/main/osx-64::numpy-1.20.3-py39h4b4dc7a_0
     numpy-base         pkgs/main/osx-64::numpy-base-1.20.3-py39he0bd621_0
     olefile            pkgs/main/noarch::olefile-0.46-py_0
     openjpeg           pkgs/main/osx-64::openjpeg-2.4.0-h66ea3da_0
     openssl            pkgs/main/osx-64::openssl-1.1.1l-h9ed2024_0
     packaging          pkgs/main/noarch::packaging-21.0-pyhd3eb1b0_0
     pandas             pkgs/main/osx-64::pandas-1.3.2-py39h5008ddb_0
     pandoc             pkgs/main/osx-64::pandoc-2.12-hecd8cb5_0
     pandocfilters      pkgs/main/osx-64::pandocfilters-1.4.3-py39hecd8cb5_1
     parso              pkgs/main/noarch::parso-0.8.2-pyhd3eb1b0_0
     pathspec           pkgs/main/noarch::pathspec-0.7.0-py_0
     pexpect            pkgs/main/noarch::pexpect-4.8.0-pyhd3eb1b0_3
     pickleshare        pkgs/main/noarch::pickleshare-0.7.5-pyhd3eb1b0_1003
     pillow             pkgs/main/osx-64::pillow-8.3.1-py39ha4cf6ea_0
     pip                pkgs/main/osx-64::pip-21.2.4-py37hecd8cb5_0
     pluggy             pkgs/main/osx-64::pluggy-0.13.1-py39hecd8cb5_0
     prometheus_client  pkgs/main/noarch::prometheus_client-0.11.0-pyhd3eb1b0_0
     prompt-toolkit     pkgs/main/noarch::prompt-toolkit-3.0.17-pyh06a4308_0
     ptyprocess         pkgs/main/noarch::ptyprocess-0.7.0-pyhd3eb1b0_2
     py                 pkgs/main/noarch::py-1.10.0-pyhd3eb1b0_0
     pycodestyle        pkgs/main/noarch::pycodestyle-2.7.0-pyhd3eb1b0_0
     pycparser          pkgs/main/noarch::pycparser-2.20-py_2
     pydata-sphinx-the~ conda-forge/noarch::pydata-sphinx-theme-0.6.3-pyhd8ed1ab_0
     pyflakes           pkgs/main/noarch::pyflakes-2.3.1-pyhd3eb1b0_0
     pygments           pkgs/main/noarch::pygments-2.10.0-pyhd3eb1b0_0
     pyopenssl          pkgs/main/noarch::pyopenssl-20.0.1-pyhd3eb1b0_1
     pyparsing          pkgs/main/noarch::pyparsing-2.4.7-pyhd3eb1b0_0
     pyrsistent         pkgs/main/osx-64::pyrsistent-0.18.0-py39h9ed2024_0
     pysocks            pkgs/main/osx-64::pysocks-1.7.1-py39hecd8cb5_0
     pytest             pkgs/main/osx-64::pytest-6.2.4-py39hecd8cb5_2
     pytest-cov         pkgs/main/noarch::pytest-cov-2.12.1-pyhd3eb1b0_0
     pytest-flake8      pkgs/main/noarch::pytest-flake8-1.0.7-pyhd3eb1b0_0
     pytest-forked      pkgs/main/noarch::pytest-forked-1.3.0-pyhd3eb1b0_0
     pytest-xdist       pkgs/main/noarch::pytest-xdist-2.3.0-pyhd3eb1b0_0
     python             pkgs/main/osx-64::python-3.9.6-h88f2d9e_1
     python-dateutil    pkgs/main/noarch::python-dateutil-2.8.2-pyhd3eb1b0_0
     python_abi         conda-forge/osx-64::python_abi-3.9-2_cp39
     pytz               pkgs/main/noarch::pytz-2021.1-pyhd3eb1b0_0
     pyyaml             pkgs/main/osx-64::pyyaml-5.4.1-py39h9ed2024_1
     pyzmq              pkgs/main/osx-64::pyzmq-22.2.1-py39h23ab428_1
     readline           pkgs/main/osx-64::readline-8.1-h9ed2024_0
     regex              pkgs/main/osx-64::regex-2021.8.3-py39h9ed2024_0
     requests           pkgs/main/noarch::requests-2.26.0-pyhd3eb1b0_0
     ruamel_yaml        pkgs/main/osx-64::ruamel_yaml-0.15.100-py39h9ed2024_0
     scipy              pkgs/main/osx-64::scipy-1.6.2-py39hd5f7400_1
     send2trash         pkgs/main/noarch::send2trash-1.5.0-pyhd3eb1b0_1
     setuptools         pkgs/main/osx-64::setuptools-52.0.0-py39hecd8cb5_0
     shellingham        pkgs/main/noarch::shellingham-1.3.1-py_0
     six                pkgs/main/noarch::six-1.16.0-pyhd3eb1b0_0
     smmap              pkgs/main/noarch::smmap-4.0.0-pyhd3eb1b0_0
     sniffio            pkgs/main/osx-64::sniffio-1.2.0-py39hecd8cb5_1
     snowballstemmer    pkgs/main/noarch::snowballstemmer-2.1.0-pyhd3eb1b0_0
     soupsieve          pkgs/main/noarch::soupsieve-2.2.1-pyhd3eb1b0_0
     sphinx             pkgs/main/noarch::sphinx-3.5.4-pyhd3eb1b0_0
     sphinx-autobuild   conda-forge/noarch::sphinx-autobuild-2021.3.14-pyhd8ed1ab_0
     sphinx-book-theme  conda-forge/noarch::sphinx-book-theme-0.1.3-pyhd8ed1ab_0
     sphinx-panels      conda-forge/noarch::sphinx-panels-0.6.0-pyhd8ed1ab_0
     sphinx-togglebutt~ conda-forge/noarch::sphinx-togglebutton-0.2.3-pyhd3deb0d_0
     sphinxcontrib-app~ pkgs/main/noarch::sphinxcontrib-applehelp-1.0.2-pyhd3eb1b0_0
     sphinxcontrib-dev~ pkgs/main/noarch::sphinxcontrib-devhelp-1.0.2-pyhd3eb1b0_0
     sphinxcontrib-htm~ pkgs/main/noarch::sphinxcontrib-htmlhelp-2.0.0-pyhd3eb1b0_0
     sphinxcontrib-jsm~ pkgs/main/noarch::sphinxcontrib-jsmath-1.0.1-pyhd3eb1b0_0
     sphinxcontrib-qth~ pkgs/main/noarch::sphinxcontrib-qthelp-1.0.3-pyhd3eb1b0_0
     sphinxcontrib-ser~ pkgs/main/noarch::sphinxcontrib-serializinghtml-1.1.5-pyhd3eb1b0_0
     sqlalchemy         pkgs/main/osx-64::sqlalchemy-1.4.22-py39h9ed2024_0
     sqlite             pkgs/main/osx-64::sqlite-3.36.0-hce871da_0
     terminado          pkgs/main/osx-64::terminado-0.9.4-py39hecd8cb5_0
     testpath           pkgs/main/noarch::testpath-0.5.0-pyhd3eb1b0_0
     tk                 pkgs/main/osx-64::tk-8.6.10-hb0a8c7a_0
     toml               pkgs/main/noarch::toml-0.10.2-pyhd3eb1b0_0
     tornado            pkgs/main/osx-64::tornado-6.1-py39h9ed2024_0
     tqdm               pkgs/main/noarch::tqdm-4.62.1-pyhd3eb1b0_1
     traitlets          pkgs/main/noarch::traitlets-5.0.5-pyhd3eb1b0_0
     typed-ast          pkgs/main/osx-64::typed-ast-1.4.3-py39h9ed2024_1
     typing-extensions  pkgs/main/noarch::typing-extensions-3.10.0.0-hd3eb1b0_0
     typing_extensions  pkgs/main/noarch::typing_extensions-3.10.0.0-pyh06a4308_0
     tzdata             pkgs/main/noarch::tzdata-2021a-h5d7bf9c_0
     uncertainties      conda-forge/noarch::uncertainties-3.1.6-pyhd8ed1ab_0
     urllib3            pkgs/main/noarch::urllib3-1.26.6-pyhd3eb1b0_1
     wcwidth            pkgs/main/noarch::wcwidth-0.2.5-py_0
     webencodings       pkgs/main/osx-64::webencodings-0.5.1-py39hecd8cb5_1
     wheel              pkgs/main/noarch::wheel-0.37.0-pyhd3eb1b0_0
     widgetsnbextension pkgs/main/osx-64::widgetsnbextension-3.5.1-py39hecd8cb5_0
     xz                 pkgs/main/osx-64::xz-5.2.5-h1de35cc_0
     yaml               pkgs/main/osx-64::yaml-0.2.5-haf1e3a3_0
     zeromq             pkgs/main/osx-64::zeromq-4.3.4-h23ab428_0
     zipp               pkgs/main/noarch::zipp-3.5.0-pyhd3eb1b0_0
     zlib               pkgs/main/osx-64::zlib-1.2.11-h1de35cc_3
     zstd               pkgs/main/osx-64::zstd-1.4.9-h322a384_0



   Downloading and Extracting Packages
   typing-extensions-3. | 8 KB      | ########## | 100% 
   importlib_metadata-3 | 11 KB     | ########## | 100% 
   matplotlib-3.4.2     | 26 KB     | ########## | 100% 
   blas-1.0             | 6 KB      | ########## | 100% 
   python_abi-3.9       | 4 KB      | ########## | 100% 
   numpy-1.20.3         | 23 KB     | ########## | 100% 
   Preparing transaction: ...working... done
   Verifying transaction: ...working... done
   Executing transaction: ...working... done
   #
   # To activate this environment, use
   #
   #     $ conda activate /Users/mforbes/.../physics-581-physics-inspired-computation/envs/phys-581-2021
   #
   # To deactivate an active environment, use
   #
   #     $ conda deactivate

   Collecting sphinxcontrib-bibtex
     Using cached sphinxcontrib_bibtex-2.3.0-py3-none-any.whl (35 kB)
   Collecting mmf-setup
     Using cached mmf_setup-0.4.3-py3-none-any.whl (73 kB)
   Collecting sphinxcontrib-zopeext
     Using cached sphinxcontrib_zopeext-0.2.4-py3-none-any.whl
   Collecting pybtex>=0.20
     Using cached pybtex-0.24.0-py2.py3-none-any.whl (561 kB)
   Collecting pybtex-docutils>=1.0.0
     Using cached pybtex_docutils-1.0.1-py3-none-any.whl (4.8 kB)
   Requirement already satisfied: Sphinx>=2.1 in ./envs/phys-581-2021/lib/python3.9/site-packages (from sphinxcontrib-bibtex) (3.5.4)
   Requirement already satisfied: docutils>=0.8 in ./envs/phys-581-2021/lib/python3.9/site-packages (from sphinxcontrib-bibtex) (0.16)
   Collecting tomlkit
     Using cached tomlkit-0.7.2-py2.py3-none-any.whl (32 kB)
   Requirement already satisfied: importlib-metadata in ./envs/phys-581-2021/lib/python3.9/site-packages (from mmf-setup) (3.10.0)
   Collecting zope.interface
     Using cached zope.interface-5.4.0-cp39-cp39-macosx_10_14_x86_64.whl (208 kB)
   Collecting latexcodec>=1.0.4
     Using cached latexcodec-2.0.1-py2.py3-none-any.whl (18 kB)
   Requirement already satisfied: PyYAML>=3.01 in ./envs/phys-581-2021/lib/python3.9/site-packages (from pybtex>=0.20->sphinxcontrib-bibtex) (5.4.1)
   Requirement already satisfied: six in ./envs/phys-581-2021/lib/python3.9/site-packages (from pybtex>=0.20->sphinxcontrib-bibtex) (1.16.0)
   Requirement already satisfied: babel>=1.3 in ./envs/phys-581-2021/lib/python3.9/site-packages (from Sphinx>=2.1->sphinxcontrib-bibtex) (2.9.1)
   Requirement already satisfied: sphinxcontrib-htmlhelp in ./envs/phys-581-2021/lib/python3.9/site-packages (from Sphinx>=2.1->sphinxcontrib-bibtex) (2.0.0)
   Requirement already satisfied: requests>=2.5.0 in ./envs/phys-581-2021/lib/python3.9/site-packages (from Sphinx>=2.1->sphinxcontrib-bibtex) (2.26.0)
   Requirement already satisfied: Pygments>=2.0 in ./envs/phys-581-2021/lib/python3.9/site-packages (from Sphinx>=2.1->sphinxcontrib-bibtex) (2.10.0)
   Requirement already satisfied: sphinxcontrib-devhelp in ./envs/phys-581-2021/lib/python3.9/site-packages (from Sphinx>=2.1->sphinxcontrib-bibtex) (1.0.2)
   Requirement already satisfied: imagesize in ./envs/phys-581-2021/lib/python3.9/site-packages (from Sphinx>=2.1->sphinxcontrib-bibtex) (1.2.0)
   Requirement already satisfied: alabaster<0.8,>=0.7 in ./envs/phys-581-2021/lib/python3.9/site-packages (from Sphinx>=2.1->sphinxcontrib-bibtex) (0.7.12)
   Requirement already satisfied: sphinxcontrib-serializinghtml in ./envs/phys-581-2021/lib/python3.9/site-packages (from Sphinx>=2.1->sphinxcontrib-bibtex) (1.1.5)
   Requirement already satisfied: Jinja2>=2.3 in ./envs/phys-581-2021/lib/python3.9/site-packages (from Sphinx>=2.1->sphinxcontrib-bibtex) (3.0.1)
   Requirement already satisfied: sphinxcontrib-jsmath in ./envs/phys-581-2021/lib/python3.9/site-packages (from Sphinx>=2.1->sphinxcontrib-bibtex) (1.0.1)
   Requirement already satisfied: sphinxcontrib-applehelp in ./envs/phys-581-2021/lib/python3.9/site-packages (from Sphinx>=2.1->sphinxcontrib-bibtex) (1.0.2)
   Requirement already satisfied: snowballstemmer>=1.1 in ./envs/phys-581-2021/lib/python3.9/site-packages (from Sphinx>=2.1->sphinxcontrib-bibtex) (2.1.0)
   Requirement already satisfied: setuptools in ./envs/phys-581-2021/lib/python3.9/site-packages (from Sphinx>=2.1->sphinxcontrib-bibtex) (52.0.0.post20210125)
   Requirement already satisfied: packaging in ./envs/phys-581-2021/lib/python3.9/site-packages (from Sphinx>=2.1->sphinxcontrib-bibtex) (21.0)
   Requirement already satisfied: sphinxcontrib-qthelp in ./envs/phys-581-2021/lib/python3.9/site-packages (from Sphinx>=2.1->sphinxcontrib-bibtex) (1.0.3)
   Requirement already satisfied: pytz>=2015.7 in ./envs/phys-581-2021/lib/python3.9/site-packages (from babel>=1.3->Sphinx>=2.1->sphinxcontrib-bibtex) (2021.1)
   Requirement already satisfied: MarkupSafe>=2.0 in ./envs/phys-581-2021/lib/python3.9/site-packages (from Jinja2>=2.3->Sphinx>=2.1->sphinxcontrib-bibtex) (2.0.1)
   Requirement already satisfied: idna<4,>=2.5 in ./envs/phys-581-2021/lib/python3.9/site-packages (from requests>=2.5.0->Sphinx>=2.1->sphinxcontrib-bibtex) (3.2)
   Requirement already satisfied: certifi>=2017.4.17 in ./envs/phys-581-2021/lib/python3.9/site-packages (from requests>=2.5.0->Sphinx>=2.1->sphinxcontrib-bibtex) (2021.5.30)
   Requirement already satisfied: urllib3<1.27,>=1.21.1 in ./envs/phys-581-2021/lib/python3.9/site-packages (from requests>=2.5.0->Sphinx>=2.1->sphinxcontrib-bibtex) (1.26.6)
   Requirement already satisfied: charset-normalizer~=2.0.0 in ./envs/phys-581-2021/lib/python3.9/site-packages (from requests>=2.5.0->Sphinx>=2.1->sphinxcontrib-bibtex) (2.0.4)
   Requirement already satisfied: zipp>=0.5 in ./envs/phys-581-2021/lib/python3.9/site-packages (from importlib-metadata->mmf-setup) (3.5.0)
   Requirement already satisfied: pyparsing>=2.0.2 in ./envs/phys-581-2021/lib/python3.9/site-packages (from packaging->Sphinx>=2.1->sphinxcontrib-bibtex) (2.4.7)
   Installing collected packages: latexcodec, pybtex, zope.interface, tomlkit, pybtex-docutils, sphinxcontrib-zopeext, sphinxcontrib-bibtex, mmf-setup
   Successfully installed latexcodec-2.0.1 mmf-setup-0.4.3 pybtex-0.24.0 pybtex-docutils-1.0.1 sphinxcontrib-bibtex-2.3.0 sphinxcontrib-zopeext-0.2.4 tomlkit-0.7.2 zope.interface-5.4.0
   The project is ready to run commands.
   Use `anaconda-project list-commands` to see what's available.
   CONDA_EXE=/data/apps/conda/bin/conda anaconda-project run init  # Custom command: see anaconda-project.yaml
   Installed kernelspec phys-581-2021 in /Users/mforbes/Library/Jupyter/kernels/phys-581-2021

   # Optional: run a shell with the installed environment
   (myenv) MacOSX $ anaconda-project run bash
   bash-3.2$ type python3
   python3 is /Users/mforbes/.../tmp/physics-581-physics-inspired-computation/envs/phys-581-2021/bin/python3

   # You could also do this manually by activating the environment with conda
   (myenv) MacOSX $ conda activate envs/phys-581-2021/
   (phys-581-2021) MacOSX $ type python3
   python3 is /Users/mforbes/.../tmp/physics-581-physics-inspired-computation/envs/phys-581-2021/bin/python3
   ```
   </details>

   <details><summary>Example session on CoCalc</summary>

   Before doing this, I first bought a license for my private "student" CoCalc project.
   I also added the User key to my `~/.ssh/config` file with the alias `smc581private`:
   
   ```
   # ~/.ssh/config file
   ...
   Host smc581private
      User f6432a...
   Host smc*
     HostName ssh.cocalc.com
     ForwardAgent yes
     SendEnv LC_HG_USERNAME
     SendEnv LC_GIT_USERNAME
     SendEnv LC_GIT_USEREMAIL
     SetEnv LC_EDITOR=vi
   ```
   
   Before continuing, make sure you connect to the project via the web and start it,
   otherwise you will get the following response:
   
   ```console
   MacOSX $ ssh smc581private
   f6432a...@ssh.cocalc.com: Permission denied (publickey).
   ```

   After starting the project, this works (takes about 5 minutes):
   
   ```console
   MacOSX $ ssh smc581private
   ~$ git clone https://gitlab.com/wsu-courses/physics-581-physics-inspired-computation.git
   Cloning into 'physics-581-physics-inspired-computation'...
   remote: Enumerating objects: 269, done.
   remote: Counting objects: 100% (98/98), done.
   remote: Compressing objects: 100% (59/59), done.
   remote: Total 269 (delta 53), reused 76 (delta 39), pack-reused 171
   Receiving objects: 100% (269/269), 201.54 KiB | 4.58 MiB/s, done.
   Resolving deltas: 100% (129/129), done.
   ~$ cd physics-581-physics-inspired-computation
   ~/physics-581-physics-inspired-computation$ time make init
   python3 -m pip install --user --upgrade mmf-setup
   Collecting mmf-setup
     Downloading mmf_setup-0.4.3-py3-none-any.whl (73 kB)
        |████████████████████████████████| 73 kB 4.7 MB/s 
   Collecting tomlkit
     Downloading tomlkit-0.7.2-py2.py3-none-any.whl (32 kB)
   Requirement already satisfied: importlib-metadata in /usr/lib/python3/dist-packages (from mmf-setup) (1.5.0)
   Installing collected packages: tomlkit, mmf-setup
   Successfully installed mmf-setup-0.4.3 tomlkit-0.7.2
   mmf_setup cocalc
   # Installing mercurial, hg-evolve, hg-git, jupytext for python3...
   python3 -m pip install --upgrade --user pip mercurial hg-evolve hg-git jupytext
   Requirement already satisfied: pip in /usr/local/lib/python3.8/dist-packages (21.2.4)
   Collecting mercurial
     Downloading mercurial-5.9.1.tar.gz (8.1 MB)
        |████████████████████████████████| 8.1 MB 2.6 MB/s 
     Installing build dependencies ... done
     Getting requirements to build wheel ... done
       Preparing wheel metadata ... done
   Collecting hg-evolve
     Downloading hg-evolve-10.3.3.tar.gz (850 kB)
        |████████████████████████████████| 850 kB 66.3 MB/s 
   Collecting hg-git
     Downloading hg_git-0.10.2-py3-none-any.whl (65 kB)
        |████████████████████████████████| 65 kB 48.8 MB/s 
   Requirement already satisfied: jupytext in /usr/local/lib/python3.8/dist-packages (1.11.5)
   Requirement already satisfied: dulwich>=0.19.0 in /usr/lib/python3/dist-packages (from hg-git) (0.19.15)
   Requirement already satisfied: nbformat in /usr/local/lib/python3.8/dist-packages (from jupytext) (5.1.3)
   Requirement already satisfied: markdown-it-py~=1.0 in /usr/local/lib/python3.8/dist-packages (from jupytext) (1.0.0)
   Requirement already satisfied: pyyaml in /usr/lib/python3/dist-packages (from jupytext) (5.3.1)
   Requirement already satisfied: mdit-py-plugins in /usr/local/lib/python3.8/dist-packages (from jupytext) (0.2.4)
   Requirement already satisfied: toml in /usr/lib/python3/dist-packages (from jupytext) (0.10.0)
   Requirement already satisfied: attrs<21,>=19 in /usr/local/lib/python3.8/dist-packages (from markdown-it-py~=1.0->jupytext) (19.3.0)
   Requirement already satisfied: traitlets>=4.1 in /usr/local/lib/python3.8/dist-packages (from nbformat->jupytext) (5.0.5)
   Requirement already satisfied: jsonschema!=2.5.0,>=2.4 in /usr/local/lib/python3.8/dist-packages (from nbformat->jupytext) (3.2.0)
   Requirement already satisfied: ipython-genutils in /usr/local/lib/python3.8/dist-packages (from nbformat->jupytext) (0.2.0)
   Requirement already satisfied: jupyter-core in /usr/local/lib/python3.8/dist-packages (from nbformat->jupytext) (4.6.3)
   Requirement already satisfied: pyrsistent>=0.14.0 in /usr/local/lib/python3.8/dist-packages (from jsonschema!=2.5.0,>=2.4->nbformat->jupytext) (0.16.0)
   Requirement already satisfied: setuptools in /usr/local/lib/python3.8/dist-packages (from jsonschema!=2.5.0,>=2.4->nbformat->jupytext) (57.4.0)
   Requirement already satisfied: six>=1.11.0 in /usr/local/lib/python3.8/dist-packages (from jsonschema!=2.5.0,>=2.4->nbformat->jupytext) (1.15.0)
   Building wheels for collected packages: mercurial, hg-evolve
     Building wheel for mercurial (PEP 517) ... done
     Created wheel for mercurial: filename=mercurial-5.9.1-cp38-cp38-linux_x86_64.whl size=6648296 sha256=9e819907db0cac0861851fc83d215ed29e8aa06756ffaa73fb3fcbfa5629c3bb
     Stored in directory: /tmp/pip-ephem-wheel-cache-9bf8f4mm/wheels/2f/b2/78/7e602145b2ba0555351230b0376f139080ae51126e77d18ace
     Building wheel for hg-evolve (setup.py) ... done
     Created wheel for hg-evolve: filename=hg_evolve-10.3.3-py3-none-any.whl size=214847 sha256=791480885a6532a7d4a211a40f8ac375d4d8a352a1605c29fc64ec7b7b73f88f
     Stored in directory: /tmp/pip-ephem-wheel-cache-9bf8f4mm/wheels/d4/a6/97/55c036c6a151d1735117ec1ed4ff7c3dd5d1628041a4016325
   Successfully built mercurial hg-evolve
   Installing collected packages: mercurial, hg-git, hg-evolve
   Successfully installed hg-evolve-10.3.3 hg-git-0.10.2 mercurial-5.9.1
   # Setting up config files for CoCalc...
   mv ~/.bashrc ~/.bashrc_cocalc
   /home/user/.local/bin/mmf_initial_setup -v /home/user/.local/lib/python3.8/site-packages/mmf_setup/_data/config_files/cocalc
   Using <home> = /home/user
   Using dir = /home/user/.local/lib/python3.8/site-packages/mmf_setup/_data/config_files/cocalc
   Warning: No dest = 2nd line in file '/home/user/.local/lib/python3.8/site-packages/mmf_setup/_data/config_files/cocalc/README.md'... ignoring
   os.symlink('.local/lib/python3.8/site-packages/mmf_setup/_data/config_files/cocalc/bash_aliases', '/home/user/.bash_aliases')
   os.symlink('.local/lib/python3.8/site-packages/mmf_setup/_data/config_files/cocalc/bashrc', '/home/user/.bashrc')
   Warning: No dest = 2nd line in file '/home/user/.local/lib/python3.8/site-packages/mmf_setup/_data/config_files/cocalc/gitconfig'... ignoring
   os.symlink('.local/lib/python3.8/site-packages/mmf_setup/_data/config_files/cocalc/gitignore', '/home/user/.gitignore')
   os.symlink('.local/lib/python3.8/site-packages/mmf_setup/_data/config_files/cocalc/hgignore', '/home/user/.hgignore')
   os.symlink('.local/lib/python3.8/site-packages/mmf_setup/_data/config_files/cocalc/hgrc', '/home/user/.hgrc')
   os.symlink('.local/lib/python3.8/site-packages/mmf_setup/_data/config_files/cocalc/inputrc', '/home/user/.inputrc')
   Warning: No dest = 2nd line in file '/home/user/.local/lib/python3.8/site-packages/mmf_setup/_data/config_files/cocalc/message.txt'... ignoring
   os.symlink('../lib/python3.8/site-packages/mmf_setup/_data/config_files/cocalc/mr', '/home/user/.local/bin/mr')
   os.symlink('.local/lib/python3.8/site-packages/mmf_setup/_data/config_files/cocalc/mrconfig', '/home/user/.mrconfig')
   os.symlink('.local/lib/python3.8/site-packages/mmf_setup/_data/config_files/cocalc/pdbrc', '/home/user/.pdbrc')
   Configurations for your CoCalc project have been symlinked as described above.

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
   source $ANACONDA2020/bin/activate root && CONDA_EXE=mamba anaconda-project prepare
   pkgs/main/noarch          
   pkgs/r/linux-64           
   cvxgrp/linux-64           
   plotly/linux-64           
   pytorch/noarch            
   pkgs/r/noarch             
   vpython/noarch            
   bioconda/linux-64         
   plotly/noarch             
   gimli/noarch              
   pkgs/main/linux-64        
   vpython/linux-64          
   bokeh/noarch              
   gimli/linux-64            
   cvxgrp/noarch             
   bioconda/noarch           
   scitools/noarch           
   astropy/noarch            
   pytorch/linux-64          
   bokeh/linux-64            
   astropy/linux-64          
   scitools/linux-64         
   conda-forge/noarch        
   conda-forge/linux-64      
   ERROR   Caught a filesystem error: Read-only file system: '/ext/anaconda2020.02/pkgs/sphinxcontrib-jsmath-1.0.1-py_0'
   ERROR   Caught a filesystem error: Read-only file system: '/ext/anaconda2020.02/pkgs/imagesize-1.2.0-py_0'
   Transaction

     Prefix: /home/user/physics-581-physics-inspired-computation/envs/phys-581-2021

     Updating specs:

      - scipy
      - conda-forge::sphinx-panels
      - conda-forge::sphinx-autobuild
      - pandas
      - conda-forge::sphinx-book-theme
      - python==3.9
      - conda-forge::myst-nb
      - pip
      - anaconda-project[version='>=0.10.1']
      - conda-forge::uncertainties
      - pytest-flake8
      - matplotlib
      - pytest-cov
      - jupytext
      - black
      - pytest-xdist
      - sphinx


     Package                             Version  Build                Channel                    Size
   ─────────────────────────────────────────────────────────────────────────────────────────────────────
     Install:
   ─────────────────────────────────────────────────────────────────────────────────────────────────────

     _libgcc_mutex                           0.1  conda_forge          conda-forge/linux-64       3 KB
     _openmp_mutex                           4.5  1_gnu                conda-forge/linux-64      22 KB
     alabaster                            0.7.12  py_0                 conda-forge/noarch        15 KB
     alsa-lib                              1.2.3  h516909a_0           conda-forge/linux-64     560 KB
     anaconda-client                       1.8.0  py39h06a4308_0       pkgs/main/linux-64       153 KB
     anaconda-project                     0.10.1  pyhd8ed1ab_0         conda-forge/noarch       Cached
     anyio                                 3.3.0  py39hf3d152e_0       conda-forge/linux-64     148 KB
     argon2-cffi                          20.1.0  py39hbd71b63_2       conda-forge/linux-64      47 KB
     async_generator                        1.10  py_0                 conda-forge/noarch        18 KB
     attrs                                20.3.0  pyhd3deb0d_0         conda-forge/noarch        41 KB
     babel                                 2.9.1  pyh44b312d_0         conda-forge/noarch         6 MB
     backcall                              0.2.0  pyh9f0ad1d_0         conda-forge/noarch        13 KB
     backports                               1.0  py_2                 conda-forge/noarch         4 KB
     backports.functools_lru_cache         1.6.4  pyhd8ed1ab_0         conda-forge/noarch         9 KB
     beautifulsoup4                        4.9.3  pyhb0f4dca_0         conda-forge/noarch        86 KB
     black                                21.8b0  pyhd8ed1ab_0         conda-forge/noarch       116 KB
     bleach                                4.1.0  pyhd8ed1ab_0         conda-forge/noarch       121 KB
     brotlipy                              0.7.0  py39h3811e60_1001    conda-forge/linux-64     341 KB
     ca-certificates                    2021.7.5  h06a4308_1           pkgs/main/linux-64       Cached
     certifi                           2021.5.30  py39hf3d152e_0       conda-forge/linux-64     141 KB
     cffi                                 1.14.6  py39he32792d_0       conda-forge/linux-64     227 KB
     chardet                               4.0.0  py39hf3d152e_1       conda-forge/linux-64     205 KB
     charset-normalizer                    2.0.0  pyhd8ed1ab_0         conda-forge/noarch        32 KB
     click                                 8.0.1  py39hf3d152e_0       conda-forge/linux-64     146 KB
     click-completion                      0.5.2  py39hf3d152e_2       conda-forge/linux-64      20 KB
     click-log                             0.3.2  pyh9f0ad1d_0         conda-forge/noarch         8 KB
     clyent                                1.2.2  py_1                 conda-forge/noarch         9 KB
     colorama                              0.4.4  pyh9f0ad1d_0         conda-forge/noarch        18 KB
     conda-pack                            0.6.0  pyhd3deb0d_0         conda-forge/noarch       Cached
     coverage                                5.5  py39h3811e60_0       conda-forge/linux-64     270 KB
     cryptography                          3.4.7  py39hbca0aa6_0       conda-forge/linux-64       1 MB
     cycler                               0.10.0  py_2                 conda-forge/noarch         9 KB
     dataclasses                             0.8  pyhc8e2a94_3         conda-forge/noarch        10 KB
     dbus                                1.13.18  hb2f20db_0           pkgs/main/linux-64       504 KB
     debugpy                               1.4.1  py39he80948d_0       conda-forge/linux-64       2 MB
     decorator                             5.0.9  pyhd8ed1ab_0         conda-forge/noarch        11 KB
     defusedxml                            0.7.1  pyhd8ed1ab_0         conda-forge/noarch        23 KB
     docutils                               0.16  py39hf3d152e_3       conda-forge/linux-64     737 KB
     entrypoints                             0.3  py39hde42818_1002    conda-forge/linux-64      11 KB
     execnet                               1.9.0  pyhd8ed1ab_0         conda-forge/noarch        33 KB
     expat                                 2.4.1  h9c3ff4c_0           conda-forge/linux-64     182 KB
     flake8                                3.9.2  pyhd8ed1ab_0         conda-forge/noarch        90 KB
     fontconfig                           2.13.1  hba837de_1005        conda-forge/linux-64     357 KB
     freetype                             2.10.4  h0708190_1           conda-forge/linux-64     890 KB
     future                               0.18.2  py39hf3d152e_3       conda-forge/linux-64     718 KB
     gettext                              0.21.0  hf68c758_0           pkgs/main/linux-64         3 MB
     gitdb                                 4.0.7  pyhd8ed1ab_0         conda-forge/noarch        46 KB
     gitpython                            3.1.18  pyhd8ed1ab_0         conda-forge/noarch       117 KB
     glib                                 2.68.4  h9c3ff4c_0           conda-forge/linux-64     447 KB
     glib-tools                           2.68.4  h9c3ff4c_0           conda-forge/linux-64      86 KB
     greenlet                              1.1.1  py39he80948d_0       conda-forge/linux-64      83 KB
     gst-plugins-base                     1.18.4  hf529b03_2           conda-forge/linux-64       3 MB
     gstreamer                            1.18.4  h76c114f_2           conda-forge/linux-64       2 MB
     icu                                    68.1  h58526e2_0           conda-forge/linux-64      13 MB
     idna                                    3.2  pyhd3eb1b0_0         pkgs/main/noarch          48 KB
     imagesize                             1.2.0  py_0                 conda-forge/noarch         8 KB
     importlib-metadata                    4.8.1  py39hf3d152e_0       conda-forge/linux-64      32 KB
     importlib_resources                   3.3.1  py39hf3d152e_0       conda-forge/linux-64      37 KB
     iniconfig                             1.1.1  pyh9f0ad1d_0         conda-forge/noarch         8 KB
     ipykernel                             6.3.1  py39hef51801_0       conda-forge/linux-64     173 KB
     ipython                              7.27.0  py39hef51801_0       conda-forge/linux-64       1 MB
     ipython_genutils                      0.2.0  py_1                 conda-forge/noarch        21 KB
     ipywidgets                            7.6.4  pyhd8ed1ab_0         conda-forge/noarch       101 KB
     jbig                                    2.1  h7f98852_2003        conda-forge/linux-64      43 KB
     jedi                                 0.18.0  py39hf3d152e_2       conda-forge/linux-64     922 KB
     jinja2                                3.0.1  pyhd8ed1ab_0         conda-forge/noarch        99 KB
     jpeg                                     9d  h516909a_0           conda-forge/linux-64     Cached
     jsonschema                            3.2.0  pyhd8ed1ab_3         conda-forge/noarch        45 KB
     jupyter-cache                         0.4.3  pyhd8ed1ab_0         conda-forge/noarch        27 KB
     jupyter-server-mathjax                0.2.3  pyhd8ed1ab_0         conda-forge/noarch         2 MB
     jupyter-sphinx                        0.3.2  py_0                 conda-forge/noarch        19 KB
     jupyter_client                        7.0.2  pyhd8ed1ab_0         conda-forge/noarch        85 KB
     jupyter_core                          4.7.1  py39hf3d152e_0       conda-forge/linux-64      72 KB
     jupyter_server                       1.10.2  pyhd8ed1ab_0         conda-forge/noarch       265 KB
     jupyterlab_widgets                    1.0.1  pyhd8ed1ab_0         conda-forge/noarch       131 KB
     jupytext                             1.11.1  pyh44b312d_0         conda-forge/noarch       191 KB
     kiwisolver                            1.3.2  py39h1a9c180_0       conda-forge/linux-64      79 KB
     krb5                                 1.19.2  hcc1bbae_0           conda-forge/linux-64       1 MB
     lcms2                                  2.12  hddcbb42_0           conda-forge/linux-64     443 KB
     ld_impl_linux-64                     2.36.1  hea4e1c9_2           conda-forge/linux-64     667 KB
     lerc                                  2.2.1  h9c3ff4c_0           conda-forge/linux-64     213 KB
     libblas                               3.9.0  11_linux64_openblas  conda-forge/linux-64      12 KB
     libcblas                              3.9.0  11_linux64_openblas  conda-forge/linux-64      11 KB
     libclang                             11.1.0  default_ha53f305_1   conda-forge/linux-64      19 MB
     libdeflate                              1.7  h7f98852_5           conda-forge/linux-64      67 KB
     libedit                        3.1.20210714  h7f8727e_0           pkgs/main/linux-64       165 KB
     libevent                             2.1.10  hcdb4288_3           conda-forge/linux-64       1 MB
     libffi                                  3.3  h58526e2_2           conda-forge/linux-64      51 KB
     libgcc-ng                            11.1.0  hc902ee8_8           conda-forge/linux-64     Cached
     libgfortran-ng                       11.1.0  h69a702a_8           conda-forge/linux-64      19 KB
     libgfortran5                         11.1.0  h6c583b3_8           conda-forge/linux-64       2 MB
     libglib                              2.68.4  h3e27bee_0           conda-forge/linux-64       3 MB
     libgomp                              11.1.0  hc902ee8_8           conda-forge/linux-64     Cached
     libiconv                               1.16  h516909a_0           conda-forge/linux-64     Cached
     liblapack                             3.9.0  11_linux64_openblas  conda-forge/linux-64      11 KB
     libllvm11                            11.1.0  hf817b99_2           conda-forge/linux-64     Cached
     libogg                                1.3.5  h27cfd23_1           pkgs/main/linux-64       199 KB
     libopenblas                          0.3.17  pthreads_h8fe5266_1  conda-forge/linux-64       9 MB
     libopus                               1.3.1  h7f98852_1           conda-forge/linux-64     255 KB
     libpng                               1.6.37  hed695b0_2           conda-forge/linux-64     359 KB
     libpq                                  13.3  hd57d9b9_0           conda-forge/linux-64       3 MB
     libsodium                            1.0.18  h516909a_1           conda-forge/linux-64     366 KB
     libstdcxx-ng                         11.1.0  h56837e0_8           conda-forge/linux-64     Cached
     libtiff                               4.3.0  hf544144_1           conda-forge/linux-64     668 KB
     libuuid                              2.32.1  h14c3975_1000        conda-forge/linux-64     Cached
     libvorbis                             1.3.7  he1b5a44_0           conda-forge/linux-64     Cached
     libwebp-base                          1.2.1  h7f98852_0           conda-forge/linux-64     845 KB
     libxcb                                 1.14  h7b6447c_0           pkgs/main/linux-64       505 KB
     libxkbcommon                          1.0.3  he3ba5ed_0           conda-forge/linux-64     581 KB
     libxml2                              2.9.12  h72842e0_0           conda-forge/linux-64     772 KB
     livereload                            2.6.3  pyh9f0ad1d_0         conda-forge/noarch        24 KB
     lz4-c                                 1.9.3  h9c3ff4c_1           conda-forge/linux-64     179 KB
     markdown-it-py                        0.6.2  pyhd8ed1ab_0         conda-forge/noarch        55 KB
     markupsafe                            2.0.1  py39h3811e60_0       conda-forge/linux-64      22 KB
     matplotlib                            3.4.3  py39hf3d152e_0       conda-forge/linux-64       7 KB
     matplotlib-base                       3.4.3  py39h2fa2bec_0       conda-forge/linux-64       7 MB
     matplotlib-inline                     0.1.2  pyhd8ed1ab_2         conda-forge/noarch        11 KB
     mccabe                                0.6.1  py_1                 conda-forge/noarch         8 KB
     mdit-py-plugins                       0.2.6  pyhd8ed1ab_0         conda-forge/noarch        29 KB
     mistune                               0.8.4  py39h3811e60_1004    conda-forge/linux-64      54 KB
     more-itertools                        8.8.0  pyhd8ed1ab_0         conda-forge/noarch        39 KB
     mypy_extensions                       0.4.3  py39hf3d152e_3       conda-forge/linux-64      10 KB
     mysql-common                         8.0.25  ha770c72_2           conda-forge/linux-64       2 MB
     mysql-libs                           8.0.25  hfa10184_2           conda-forge/linux-64       2 MB
     myst-nb                              0.12.3  pyhd8ed1ab_0         conda-forge/noarch        32 KB
     myst-parser                          0.13.7  pyhd8ed1ab_0         conda-forge/noarch        37 KB
     nbclient                              0.5.4  pyhd8ed1ab_0         conda-forge/noarch        60 KB
     nbconvert                             5.6.0  py_0                 conda-forge/noarch       381 KB
     nbdime                                3.1.0  pyhd8ed1ab_0         conda-forge/noarch         4 MB
     nbformat                              5.1.3  pyhd8ed1ab_0         conda-forge/noarch        47 KB
     ncurses                                 6.2  h58526e2_4           conda-forge/linux-64     Cached
     nest-asyncio                          1.5.1  pyhd8ed1ab_0         conda-forge/noarch         9 KB
     notebook                              6.4.3  pyha770c72_0         conda-forge/noarch         6 MB
     nspr                                   4.30  h9c3ff4c_0           conda-forge/linux-64     233 KB
     nss                                    3.69  hb5efdd6_0           conda-forge/linux-64       2 MB
     numpy                                1.21.2  py39hdbf815f_0       conda-forge/linux-64       6 MB
     olefile                                0.46  pyh9f0ad1d_1         conda-forge/noarch        32 KB
     openjpeg                              2.4.0  hb52868f_1           conda-forge/linux-64     444 KB
     openssl                              1.1.1l  h7f8727e_0           pkgs/main/linux-64         3 MB
     packaging                              21.0  pyhd8ed1ab_0         conda-forge/noarch        35 KB
     pandas                                1.3.2  py39hde0f152_0       conda-forge/linux-64      13 MB
     pandoc                               2.14.2  h7f98852_0           conda-forge/linux-64      12 MB
     pandocfilters                         1.4.3  py39h06a4308_1       pkgs/main/linux-64        14 KB
     parso                                 0.8.2  pyhd8ed1ab_0         conda-forge/noarch        68 KB
     pathspec                              0.9.0  pyhd8ed1ab_0         conda-forge/noarch        31 KB
     pcre                                   8.45  h9c3ff4c_0           conda-forge/linux-64     253 KB
     pexpect                               4.8.0  pyh9f0ad1d_2         conda-forge/noarch        47 KB
     pickleshare                           0.7.5  py39hde42818_1002    conda-forge/linux-64      13 KB
     pillow                                8.3.1  py39ha612740_0       conda-forge/linux-64     687 KB
     pip                                  21.2.4  pyhd8ed1ab_0         conda-forge/noarch         1 MB
     platformdirs                          2.3.0  pyhd8ed1ab_0         conda-forge/noarch        14 KB
     pluggy                               0.13.1  py39hf3d152e_4       conda-forge/linux-64      29 KB
     prometheus_client                    0.11.0  pyhd8ed1ab_0         conda-forge/noarch        46 KB
     prompt-toolkit                       3.0.20  pyha770c72_0         conda-forge/noarch       246 KB
     ptyprocess                            0.7.0  pyhd3deb0d_0         conda-forge/noarch        16 KB
     py                                   1.10.0  pyhd3deb0d_0         conda-forge/noarch        73 KB
     pycodestyle                           2.7.0  pyhd8ed1ab_0         conda-forge/noarch        39 KB
     pycparser                              2.20  pyh9f0ad1d_2         conda-forge/noarch        94 KB
     pydata-sphinx-theme                   0.6.3  pyhd8ed1ab_0         conda-forge/noarch         1 MB
     pyflakes                              2.3.1  pyhd8ed1ab_0         conda-forge/noarch        57 KB
     pygments                             2.10.0  pyhd8ed1ab_0         conda-forge/noarch       760 KB
     pyopenssl                            20.0.1  pyhd8ed1ab_0         conda-forge/noarch        48 KB
     pyparsing                             2.4.7  pyh9f0ad1d_0         conda-forge/noarch        60 KB
     pyqt                                 5.12.3  py39hf3d152e_7       conda-forge/linux-64      21 KB
     pyqt-impl                            5.12.3  py39h0fcd23e_7       conda-forge/linux-64       6 MB
     pyqt5-sip                           4.19.18  py39he80948d_7       conda-forge/linux-64     310 KB
     pyqtchart                              5.12  py39h0fcd23e_7       conda-forge/linux-64     253 KB
     pyqtwebengine                        5.12.1  py39h0fcd23e_7       conda-forge/linux-64     174 KB
     pyrsistent                           0.18.0  py39h7f8727e_0       pkgs/main/linux-64        90 KB
     pysocks                               1.7.1  py39hf3d152e_3       conda-forge/linux-64      28 KB
     pytest                                6.2.5  py39hf3d152e_0       conda-forge/linux-64     433 KB
     pytest-cov                           2.12.1  pyhd8ed1ab_0         conda-forge/noarch        21 KB
     pytest-flake8                         1.0.7  pyhd3deb0d_0         conda-forge/noarch        10 KB
     pytest-forked                         1.3.0  pyhd3deb0d_0         conda-forge/noarch         8 KB
     pytest-xdist                          2.3.0  pyhd8ed1ab_0         conda-forge/noarch        31 KB
     python                                3.9.7  h49503c6_0_cpython   conda-forge/linux-64      28 MB
     python-dateutil                       2.8.2  pyhd8ed1ab_0         conda-forge/noarch       240 KB
     python_abi                              3.9  2_cp39               conda-forge/linux-64       4 KB
     pytz                                 2021.1  pyhd8ed1ab_0         conda-forge/noarch       239 KB
     pyyaml                                5.4.1  py39h3811e60_1       conda-forge/linux-64     196 KB
     pyzmq                                22.2.1  py39h37b5a0c_0       conda-forge/linux-64     506 KB
     qt                                   5.12.9  hda022c4_4           conda-forge/linux-64     100 MB
     readline                                8.1  h46c0cb4_0           conda-forge/linux-64     295 KB
     regex                             2021.8.28  py39h3811e60_0       conda-forge/linux-64     368 KB
     requests                             2.26.0  pyhd8ed1ab_0         conda-forge/noarch        52 KB
     requests-unixsocket                   0.2.0  py_0                 conda-forge/noarch        14 KB
     ruamel_yaml                        0.15.100  py39h27cfd23_0       pkgs/main/linux-64       260 KB
     scipy                                 1.7.1  py39hee8e79c_0       conda-forge/linux-64      22 MB
     send2trash                            1.8.0  pyhd8ed1ab_0         conda-forge/noarch        17 KB
     setuptools                           57.4.0  py39hf3d152e_0       conda-forge/linux-64     934 KB
     shellingham                           1.4.0  pyh44b312d_0         conda-forge/noarch        11 KB
     six                                  1.16.0  pyh6c4a22f_0         conda-forge/noarch        14 KB
     smmap                                 3.0.5  pyh44b312d_0         conda-forge/noarch       Cached
     sniffio                               1.2.0  py39hf3d152e_1       conda-forge/linux-64      15 KB
     snowballstemmer                       2.1.0  pyhd8ed1ab_0         conda-forge/noarch        57 KB
     soupsieve                             2.2.1  pyhd3eb1b0_0         pkgs/main/noarch          32 KB
     sphinx                                3.5.4  pyh44b312d_0         conda-forge/noarch         1 MB
     sphinx-autobuild                  2021.3.14  pyhd8ed1ab_0         conda-forge/noarch        13 KB
     sphinx-book-theme                     0.1.3  pyhd8ed1ab_0         conda-forge/noarch       208 KB
     sphinx-panels                         0.6.0  pyhd8ed1ab_0         conda-forge/noarch        74 KB
     sphinx-togglebutton                   0.2.3  pyhd3deb0d_0         conda-forge/noarch         9 KB
     sphinxcontrib-applehelp               1.0.2  py_0                 conda-forge/noarch        28 KB
     sphinxcontrib-devhelp                 1.0.2  py_0                 conda-forge/noarch        22 KB
     sphinxcontrib-htmlhelp                2.0.0  pyhd8ed1ab_0         conda-forge/noarch        31 KB
     sphinxcontrib-jsmath                  1.0.1  py_0                 conda-forge/noarch         7 KB
     sphinxcontrib-qthelp                  1.0.3  py_0                 conda-forge/noarch        25 KB
     sphinxcontrib-serializinghtml         1.1.5  pyhd8ed1ab_0         conda-forge/noarch        27 KB
     sqlalchemy                           1.4.23  py39h3811e60_0       conda-forge/linux-64       2 MB
     sqlite                               3.36.0  h9cd32fc_0           conda-forge/linux-64       1 MB
     terminado                            0.11.1  py39hf3d152e_0       conda-forge/linux-64      27 KB
     testpath                              0.5.0  pyhd8ed1ab_0         conda-forge/noarch        86 KB
     tk                                   8.6.11  h27826a3_1           conda-forge/linux-64       3 MB
     toml                                 0.10.2  pyhd8ed1ab_0         conda-forge/noarch        18 KB
     tomli                                 1.2.1  pyhd8ed1ab_0         conda-forge/noarch        15 KB
     tornado                                 6.1  py39h3811e60_1       conda-forge/linux-64     646 KB
     tqdm                                 4.62.2  pyhd8ed1ab_0         conda-forge/noarch        80 KB
     traitlets                             5.1.0  pyhd8ed1ab_0         conda-forge/noarch        82 KB
     typed-ast                             1.4.3  py39h3811e60_0       conda-forge/linux-64     213 KB
     typing_extensions                  3.10.0.0  pyha770c72_0         conda-forge/noarch       Cached
     tzdata                                2021a  he74cb21_1           conda-forge/noarch       121 KB
     uncertainties                         3.1.6  pyhd8ed1ab_0         conda-forge/noarch        76 KB
     urllib3                              1.26.6  pyhd8ed1ab_0         conda-forge/noarch        99 KB
     wcwidth                               0.2.5  pyh9f0ad1d_2         conda-forge/noarch        33 KB
     webencodings                          0.5.1  py_1                 conda-forge/noarch        12 KB
     websocket-client                     0.58.0  py39h06a4308_4       pkgs/main/linux-64        66 KB
     wheel                                0.37.0  pyhd8ed1ab_1         conda-forge/noarch        31 KB
     widgetsnbextension                    3.5.1  py39hf3d152e_4       conda-forge/linux-64       2 MB
     xz                                    5.2.5  h516909a_1           conda-forge/linux-64     Cached
     yaml                                  0.2.5  h516909a_0           conda-forge/linux-64      82 KB
     zeromq                                4.3.4  h9c3ff4c_1           conda-forge/linux-64     351 KB
     zipp                                  3.5.0  pyhd8ed1ab_0         conda-forge/noarch        12 KB
     zlib                                 1.2.11  h516909a_1010        conda-forge/linux-64     106 KB
     zstd                                  1.5.0  ha95c52a_0           conda-forge/linux-64     490 KB

     Summary:

     Install: 233 packages

     Total download: 323 MB

   ─────────────────────────────────────────────────────────────────────────────────────────────────────

   Finished _libgcc_mutex                        (00m:00s)               3 KB     17 KB/s
   Finished ld_impl_linux-64                     (00m:00s)             667 KB      3 MB/s
   Finished jbig                                 (00m:00s)              43 KB    130 KB/s
   Finished libffi                               (00m:00s)              51 KB    118 KB/s
   Finished libgfortran5                         (00m:01s)               2 MB      5 MB/s
   Finished mysql-common                         (00m:03s)               2 MB      4 MB/s
   Finished libwebp-base                         (00m:03s)             845 KB      2 MB/s
   Finished zstd                                 (00m:07s)             490 KB    888 KB/s
   Finished tk                                   (00m:08s)               3 MB      3 MB/s
   Finished freetype                             (00m:08s)             890 KB    772 KB/s
   Finished nss                                  (00m:09s)               2 MB      2 MB/s
   Finished fontconfig                           (00m:09s)             357 KB    248 KB/s
   Finished libopenblas                          (00m:20s)               9 MB      6 MB/s
   Finished pandoc                               (00m:23s)              12 MB      7 MB/s
   Finished libxcb                               (00m:22s)             505 KB    272 KB/s
   Finished icu                                  (00m:27s)              13 MB      7 MB/s
   Finished shellingham                          (00m:25s)              11 KB      5 KB/s
   Finished libpq                                (00m:26s)               3 MB      1 MB/s
   Finished backports                            (00m:26s)               4 KB      2 KB/s
   Finished send2trash                           (00m:26s)              17 KB      7 KB/s
   Finished more-itertools                       (00m:26s)              39 KB     17 KB/s
   Finished dataclasses                          (00m:26s)              10 KB      4 KB/s
   Finished openssl                              (00m:27s)               3 MB      1 MB/s
   Finished setuptools                           (00m:26s)             934 KB    380 KB/s
   Finished pycodestyle                          (00m:26s)              39 KB     16 KB/s
   Finished backcall                             (00m:26s)              13 KB      5 KB/s
   Finished ipython_genutils                     (00m:26s)              21 KB      8 KB/s
   Finished six                                  (00m:26s)              14 KB      5 KB/s
   Finished execnet                              (00m:26s)              33 KB     12 KB/s
   Finished pytz                                 (00m:26s)             239 KB     91 KB/s
   Finished attrs                                (00m:26s)              41 KB     16 KB/s
   Finished imagesize                            (00m:26s)               8 KB      3 KB/s
   Finished sphinxcontrib-htmlhelp               (00m:26s)              31 KB     11 KB/s
   Finished snowballstemmer                      (00m:26s)              57 KB     21 KB/s
   Finished beautifulsoup4                       (00m:26s)              86 KB     31 KB/s
   Finished matplotlib-inline                    (00m:26s)              11 KB      4 KB/s
   Finished cycler                               (00m:26s)               9 KB      3 KB/s
   Finished gitdb                                (00m:26s)              46 KB     16 KB/s
   Finished libclang                             (00m:33s)              19 MB      8 MB/s
   Finished wcwidth                              (00m:31s)              33 KB     12 KB/s
   Finished bleach                               (00m:31s)             121 KB     42 KB/s
   Finished mistune                              (00m:31s)              54 KB     18 KB/s
   Finished prompt-toolkit                       (00m:31s)             246 KB     84 KB/s
   Finished regex                                (00m:31s)             368 KB    125 KB/s
   Finished pickleshare                          (00m:31s)              13 KB      4 KB/s
   Finished certifi                              (00m:31s)             141 KB     47 KB/s
   Finished click                                (00m:31s)             146 KB     48 KB/s
   Finished glib                                 (00m:31s)             447 KB    147 KB/s
   Finished tornado                              (00m:31s)             646 KB    211 KB/s
   Finished pytest                               (00m:31s)             433 KB    138 KB/s
   Finished jedi                                 (00m:31s)             922 KB    292 KB/s
   Finished future                               (00m:32s)             718 KB    221 KB/s
   Finished cryptography                         (00m:32s)               1 MB    323 KB/s
   Finished pandocfilters                        (00m:32s)              14 KB      4 KB/s
   Finished soupsieve                            (00m:31s)              32 KB      9 KB/s
   Finished click-log                            (00m:31s)               8 KB      2 KB/s
   Finished pytest-forked                        (00m:31s)               8 KB      2 KB/s
   Finished jsonschema                           (00m:31s)              45 KB     12 KB/s
   Finished matplotlib-base                      (00m:33s)               7 MB      2 MB/s
   Finished nbformat                             (00m:29s)              47 KB      6 KB/s
   Finished nbconvert                            (00m:29s)             381 KB     49 KB/s
   Finished sphinx                               (00m:30s)               1 MB    186 KB/s
   Finished sphinx-book-theme                    (00m:30s)             208 KB     27 KB/s
   Finished click-completion                     (00m:30s)              20 KB      2 KB/s
   Finished matplotlib                           (00m:30s)               7 KB    920  B/s
   Finished pyqtwebengine                        (00m:30s)             174 KB     22 KB/s
   Finished pydata-sphinx-theme                  (00m:30s)               1 MB    168 KB/s
   Finished jupyter-sphinx                       (00m:30s)              19 KB      2 KB/s
   Finished jupyter-cache                        (00m:30s)              27 KB      3 KB/s
   Finished _openmp_mutex                        (00m:30s)              22 KB      3 KB/s
   Finished pcre                                 (00m:30s)             253 KB     31 KB/s
   Finished libsodium                            (00m:30s)             366 KB     44 KB/s
   Finished expat                                (00m:30s)             182 KB     22 KB/s
   Finished zeromq                               (00m:30s)             351 KB     43 KB/s
   Finished liblapack                            (00m:30s)              11 KB      1 KB/s
   Finished libpng                               (00m:30s)             359 KB     43 KB/s
   Finished libtiff                              (00m:30s)             668 KB     80 KB/s
   Finished python                               (00m:43s)              28 MB      3 MB/s
   Finished tzdata                               (00m:37s)             121 KB     14 KB/s
   Finished wheel                                (00m:37s)              31 KB      4 KB/s
   Finished olefile                              (00m:37s)              32 KB      4 KB/s
   Finished pandas                               (00m:45s)              13 MB      2 MB/s
   Finished mysql-libs                           (00m:40s)               2 MB    208 KB/s
   Finished mccabe                               (00m:40s)               8 KB    982  B/s
   Finished gstreamer                            (00m:41s)               2 MB    234 KB/s
   Finished defusedxml                           (00m:41s)              23 KB      3 KB/s
   Finished prometheus_client                    (00m:41s)              46 KB      5 KB/s
   Finished platformdirs                         (00m:41s)              14 KB      2 KB/s
   Finished pyparsing                            (00m:41s)              60 KB      7 KB/s
   Finished iniconfig                            (00m:40s)               8 KB    940  B/s
   Finished notebook                             (00m:45s)               6 MB    747 KB/s
   Finished zipp                                 (00m:45s)              12 KB      1 KB/s
   Finished py                                   (00m:45s)              73 KB      8 KB/s
   Finished alabaster                            (00m:45s)              15 KB      2 KB/s
   Finished pygments                             (00m:45s)             760 KB     85 KB/s
   Finished packaging                            (00m:45s)              35 KB      4 KB/s
   Finished mdit-py-plugins                      (00m:45s)              29 KB      3 KB/s
   Finished markdown-it-py                       (00m:45s)              55 KB      6 KB/s
   Finished greenlet                             (00m:45s)              83 KB      9 KB/s
   Finished markupsafe                           (00m:45s)              22 KB      2 KB/s
   Finished kiwisolver                           (00m:45s)              79 KB      9 KB/s
   Finished pyyaml                               (00m:45s)             196 KB     22 KB/s
   Finished terminado                            (00m:45s)              27 KB      3 KB/s
   Finished importlib-metadata                   (00m:45s)              32 KB      4 KB/s
   Finished debugpy                              (00m:45s)               2 MB    225 KB/s
   Finished gettext                              (00m:46s)               3 MB    296 KB/s
   Finished brotlipy                             (00m:45s)             341 KB     37 KB/s
   Finished pytest-cov                           (00m:45s)              21 KB      2 KB/s
   Finished black                                (00m:45s)             116 KB     12 KB/s
   Finished ruamel_yaml                          (00m:45s)             260 KB     28 KB/s
   Finished requests                             (00m:45s)              52 KB      5 KB/s
   Finished requests-unixsocket                  (00m:45s)              14 KB      1 KB/s
   Finished dbus                                 (00m:45s)             504 KB     53 KB/s
   Finished anyio                                (00m:45s)             148 KB     15 KB/s
   Finished ipywidgets                           (00m:45s)             101 KB     11 KB/s
   Finished myst-parser                          (00m:45s)              37 KB      4 KB/s
   Finished libopus                              (00m:45s)             255 KB     26 KB/s
   Finished zlib                                 (00m:45s)             106 KB     11 KB/s
   Finished jupyter_server                       (00m:45s)             265 KB     27 KB/s
   Finished libblas                              (00m:45s)              12 KB      1 KB/s
   Finished libcblas                             (00m:45s)              11 KB      1 KB/s
   Finished nspr                                 (00m:45s)             233 KB     24 KB/s
   Finished python_abi                           (00m:45s)               4 KB    404  B/s
   Finished numpy                                (00m:49s)               6 MB    650 KB/s
   Finished pycparser                            (00m:48s)              94 KB      9 KB/s
   Finished clyent                               (00m:48s)               9 KB    967  B/s
   Finished ptyprocess                           (00m:48s)              16 KB      2 KB/s
   Finished pyflakes                             (00m:48s)              57 KB      6 KB/s
   Finished krb5                                 (00m:49s)               1 MB    147 KB/s
   Finished libogg                               (00m:49s)             199 KB     20 KB/s
   Finished pyqt-impl                            (00m:50s)               6 MB    609 KB/s
   Finished toml                                 (00m:50s)              18 KB      2 KB/s
   Finished sphinxcontrib-serializinghtml        (00m:50s)              27 KB      3 KB/s
   Finished charset-normalizer                   (00m:50s)              32 KB      3 KB/s
   Finished backports.functools_lru_cache        (00m:50s)               9 KB    891  B/s
   Finished pysocks                              (00m:50s)              28 KB      3 KB/s
   Finished sniffio                              (00m:50s)              15 KB      1 KB/s
   Finished pluggy                               (00m:50s)              29 KB      3 KB/s
   Finished pyzmq                                (00m:50s)             506 KB     50 KB/s
   Finished jinja2                               (00m:50s)              99 KB     10 KB/s
   Finished cffi                                 (00m:50s)             227 KB     22 KB/s
   Finished nbclient                             (00m:50s)              60 KB      6 KB/s
   Finished flake8                               (00m:50s)              90 KB      9 KB/s
   Finished pytest-flake8                        (00m:50s)              10 KB    953  B/s
   Finished ipython                              (00m:50s)               1 MB    112 KB/s
   Finished python-dateutil                      (00m:50s)             240 KB     23 KB/s
   Finished sphinx-autobuild                     (00m:50s)              13 KB      1 KB/s
   Finished pyqt                                 (00m:50s)              21 KB      2 KB/s
   Finished ipykernel                            (00m:50s)             173 KB     17 KB/s
   Finished lz4-c                                (00m:50s)             179 KB     17 KB/s
   Finished sqlalchemy                           (00m:53s)               2 MB    224 KB/s
   Finished alsa-lib                             (00m:53s)             560 KB     53 KB/s
   Finished lcms2                                (00m:53s)             443 KB     42 KB/s
   Finished openjpeg                             (00m:53s)             444 KB     42 KB/s
   Finished libxml2                              (00m:53s)             772 KB     73 KB/s
   Finished widgetsnbextension                   (00m:53s)               2 MB    175 KB/s
   Finished webencodings                         (00m:53s)              12 KB      1 KB/s
   Finished sphinxcontrib-qthelp                 (00m:53s)              25 KB      2 KB/s
   Finished parso                                (00m:53s)              68 KB      6 KB/s
   Finished traitlets                            (00m:53s)              82 KB      8 KB/s
   Finished mypy_extensions                      (00m:53s)              10 KB    976  B/s
   Finished importlib_resources                  (00m:53s)              37 KB      3 KB/s
   Finished typed-ast                            (00m:53s)             213 KB     20 KB/s
   Finished colorama                             (00m:53s)              18 KB      2 KB/s
   Finished livereload                           (00m:53s)              24 KB      2 KB/s
   Finished gst-plugins-base                     (00m:54s)               3 MB    251 KB/s
   Finished pyopenssl                            (00m:54s)              48 KB      4 KB/s
   Finished argon2-cffi                          (00m:54s)              47 KB      4 KB/s
   Finished jupyter_core                         (00m:54s)              72 KB      7 KB/s
   Finished libgfortran-ng                       (00m:54s)              19 KB      2 KB/s
   Finished yaml                                 (00m:54s)              82 KB      8 KB/s
   Finished pyqtchart                            (00m:54s)             253 KB     23 KB/s
   Finished libxkbcommon                         (00m:54s)             581 KB     53 KB/s
   Finished libevent                             (00m:54s)               1 MB     99 KB/s
   Finished jupytext                             (00m:54s)             191 KB     17 KB/s
   Finished nest-asyncio                         (00m:54s)               9 KB    808  B/s
   Finished jupyterlab_widgets                   (00m:54s)             131 KB     12 KB/s
   Finished babel                                (00m:58s)               6 MB    566 KB/s
   Finished sphinxcontrib-jsmath                 (00m:58s)               7 KB    662  B/s
   Finished sphinxcontrib-devhelp                (00m:58s)              22 KB      2 KB/s
   Finished gitpython                            (00m:58s)             117 KB     10 KB/s
   Finished coverage                             (00m:58s)             270 KB     24 KB/s
   Finished sphinx-togglebutton                  (00m:58s)               9 KB    835  B/s
   Finished jupyter_client                       (00m:58s)              85 KB      8 KB/s
   Finished pyrsistent                           (00m:58s)              90 KB      8 KB/s
   Finished lerc                                 (00m:58s)             213 KB     19 KB/s
   Finished jupyter-server-mathjax               (00m:58s)               2 MB    205 KB/s
   Finished pip                                  (00m:59s)               1 MB     98 KB/s
   Finished libedit                              (00m:59s)             165 KB     14 KB/s
   Finished pathspec                             (00m:59s)              31 KB      3 KB/s
   Finished testpath                             (00m:59s)              86 KB      7 KB/s
   Finished docutils                             (00m:59s)             737 KB     63 KB/s
   Finished entrypoints                          (00m:59s)              11 KB    994  B/s
   Finished idna                                 (00m:59s)              48 KB      4 KB/s
   Finished readline                             (00m:59s)             295 KB     25 KB/s
   Finished anaconda-client                      (00m:59s)             153 KB     13 KB/s
   Finished pillow                               (00m:59s)             687 KB     58 KB/s
   Finished decorator                            (00m:59s)              11 KB    970  B/s
   Finished glib-tools                           (00m:59s)              86 KB      7 KB/s
   Finished urllib3                              (00m:59s)              99 KB      8 KB/s
   Finished tomli                                (00m:59s)              15 KB      1 KB/s
   Finished websocket-client                     (00m:59s)              66 KB      6 KB/s
   Finished tqdm                                 (00m:59s)              80 KB      7 KB/s
   Finished pyqt5-sip                            (00m:55s)             310 KB     20 KB/s
   Finished sqlite                               (00m:59s)               1 MB     93 KB/s
   Finished async_generator                      (00m:55s)              18 KB      1 KB/s
   Finished chardet                              (00m:56s)             205 KB     13 KB/s
   Finished sphinx-panels                        (00m:55s)              74 KB      5 KB/s
   Finished uncertainties                        (00m:56s)              76 KB      5 KB/s
   Finished pytest-xdist                         (00m:55s)              31 KB      2 KB/s
   Finished myst-nb                              (00m:55s)              32 KB      2 KB/s
   Finished libglib                              (00m:57s)               3 MB    196 KB/s
   Finished sphinxcontrib-applehelp              (00m:57s)              28 KB      2 KB/s
   Finished libdeflate                           (00m:57s)              67 KB      4 KB/s
   Finished pexpect                              (00m:57s)              47 KB      3 KB/s
   Finished scipy                                (01m:04s)              22 MB      1 MB/s
   Finished nbdime                               (01m:05s)               4 MB    260 KB/s
   Finished qt                                   (01m:36s)             100 MB      5 MB/s

                     __    __    __    __
                    /  \  /  \  /  \  /  \
                   /    \/    \/    \/    \
   ███████████████/  /██/  /██/  /██/  /████████████████████████
                 /  / \   / \   / \   / \  \____
                /  /   \_/   \_/   \_/   \    o \__,
               / _/                       \_____/  `
               |/
           ███╗   ███╗ █████╗ ███╗   ███╗██████╗  █████╗
           ████╗ ████║██╔══██╗████╗ ████║██╔══██╗██╔══██╗
           ██╔████╔██║███████║██╔████╔██║██████╔╝███████║
           ██║╚██╔╝██║██╔══██║██║╚██╔╝██║██╔══██╗██╔══██║
           ██║ ╚═╝ ██║██║  ██║██║ ╚═╝ ██║██████╔╝██║  ██║
           ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚═════╝ ╚═╝  ╚═╝

           mamba (0.13.0) supported by @QuantStack

           GitHub:  https://github.com/mamba-org/mamba
           Twitter: https://twitter.com/QuantStack

   █████████████████████████████████████████████████████████████


   Looking for: ['scipy', 'conda-forge::sphinx-panels', 'conda-forge::sphinx-autobuild', 'pandas', 'conda-forge::sphinx-book-theme', 'python=3.9', 'conda-forge::myst-nb', 'pip', "anaconda-project[version='>=0.10.1']", 'conda-forge::uncertainties', 'pytest-flake8', 'matplotlib', 'pytest-cov', 'jupytext', 'black', 'pytest-xdist', 'sphinx']

   Preparing transaction: ...working... done
   Verifying transaction: ...working... done
   Executing transaction: ...working... Enabling notebook extension jupyter-js-widgets/extension...
         - Validating: OK

   done
   #
   # To activate this environment, use
   #
   #     $ conda activate /home/user/physics-581-physics-inspired-computation/envs/phys-581-2021
   #
   # To deactivate an active environment, use
   #
   #     $ conda deactivate

   Collecting mmf-setup
     Downloading mmf_setup-0.4.3-py3-none-any.whl (73 kB)
   Collecting sphinxcontrib-bibtex
     Downloading sphinxcontrib_bibtex-2.3.0-py3-none-any.whl (35 kB)
   Collecting sphinxcontrib-zopeext
     Downloading sphinxcontrib-zopeext-0.2.4.tar.gz (6.7 kB)
   Collecting tomlkit
     Downloading tomlkit-0.7.2-py2.py3-none-any.whl (32 kB)
   Requirement already satisfied: importlib-metadata in ./envs/phys-581-2021/lib/python3.9/site-packages (from mmf-setup) (4.8.1)
   Requirement already satisfied: docutils>=0.8 in ./envs/phys-581-2021/lib/python3.9/site-packages (from sphinxcontrib-bibtex) (0.16)
   Collecting pybtex-docutils>=1.0.0
     Downloading pybtex_docutils-1.0.1-py3-none-any.whl (4.8 kB)
   Requirement already satisfied: Sphinx>=2.1 in ./envs/phys-581-2021/lib/python3.9/site-packages (from sphinxcontrib-bibtex) (3.5.4)
   Collecting pybtex>=0.20
     Downloading pybtex-0.24.0-py2.py3-none-any.whl (561 kB)
   Collecting zope.interface
     Downloading zope.interface-5.4.0-cp39-cp39-manylinux2010_x86_64.whl (255 kB)
   Collecting latexcodec>=1.0.4
     Downloading latexcodec-2.0.1-py2.py3-none-any.whl (18 kB)
   Requirement already satisfied: six in ./envs/phys-581-2021/lib/python3.9/site-packages (from pybtex>=0.20->sphinxcontrib-bibtex) (1.16.0)
   Requirement already satisfied: PyYAML>=3.01 in ./envs/phys-581-2021/lib/python3.9/site-packages (from pybtex>=0.20->sphinxcontrib-bibtex) (5.4.1)
   Requirement already satisfied: requests>=2.5.0 in ./envs/phys-581-2021/lib/python3.9/site-packages (from Sphinx>=2.1->sphinxcontrib-bibtex) (2.26.0)
   Requirement already satisfied: sphinxcontrib-jsmath in ./envs/phys-581-2021/lib/python3.9/site-packages (from Sphinx>=2.1->sphinxcontrib-bibtex) (1.0.1)
   Requirement already satisfied: snowballstemmer>=1.1 in ./envs/phys-581-2021/lib/python3.9/site-packages (from Sphinx>=2.1->sphinxcontrib-bibtex) (2.1.0)
   Requirement already satisfied: sphinxcontrib-htmlhelp in ./envs/phys-581-2021/lib/python3.9/site-packages (from Sphinx>=2.1->sphinxcontrib-bibtex) (2.0.0)
   Requirement already satisfied: babel>=1.3 in ./envs/phys-581-2021/lib/python3.9/site-packages (from Sphinx>=2.1->sphinxcontrib-bibtex) (2.9.1)
   Requirement already satisfied: sphinxcontrib-qthelp in ./envs/phys-581-2021/lib/python3.9/site-packages (from Sphinx>=2.1->sphinxcontrib-bibtex) (1.0.3)
   Requirement already satisfied: sphinxcontrib-serializinghtml in ./envs/phys-581-2021/lib/python3.9/site-packages (from Sphinx>=2.1->sphinxcontrib-bibtex) (1.1.5)
   Requirement already satisfied: sphinxcontrib-applehelp in ./envs/phys-581-2021/lib/python3.9/site-packages (from Sphinx>=2.1->sphinxcontrib-bibtex) (1.0.2)
   Requirement already satisfied: imagesize in ./envs/phys-581-2021/lib/python3.9/site-packages (from Sphinx>=2.1->sphinxcontrib-bibtex) (1.2.0)
   Requirement already satisfied: setuptools in ./envs/phys-581-2021/lib/python3.9/site-packages (from Sphinx>=2.1->sphinxcontrib-bibtex) (57.4.0)
   Requirement already satisfied: sphinxcontrib-devhelp in ./envs/phys-581-2021/lib/python3.9/site-packages (from Sphinx>=2.1->sphinxcontrib-bibtex) (1.0.2)
   Requirement already satisfied: alabaster<0.8,>=0.7 in ./envs/phys-581-2021/lib/python3.9/site-packages (from Sphinx>=2.1->sphinxcontrib-bibtex) (0.7.12)
   Requirement already satisfied: packaging in ./envs/phys-581-2021/lib/python3.9/site-packages (from Sphinx>=2.1->sphinxcontrib-bibtex) (21.0)
   Requirement already satisfied: Jinja2>=2.3 in ./envs/phys-581-2021/lib/python3.9/site-packages (from Sphinx>=2.1->sphinxcontrib-bibtex) (3.0.1)
   Requirement already satisfied: Pygments>=2.0 in ./envs/phys-581-2021/lib/python3.9/site-packages (from Sphinx>=2.1->sphinxcontrib-bibtex) (2.10.0)
   Requirement already satisfied: pytz>=2015.7 in ./envs/phys-581-2021/lib/python3.9/site-packages (from babel>=1.3->Sphinx>=2.1->sphinxcontrib-bibtex) (2021.1)
   Requirement already satisfied: MarkupSafe>=2.0 in ./envs/phys-581-2021/lib/python3.9/site-packages (from Jinja2>=2.3->Sphinx>=2.1->sphinxcontrib-bibtex) (2.0.1)
   Requirement already satisfied: certifi>=2017.4.17 in ./envs/phys-581-2021/lib/python3.9/site-packages (from requests>=2.5.0->Sphinx>=2.1->sphinxcontrib-bibtex) (2021.5.30)
   Requirement already satisfied: urllib3<1.27,>=1.21.1 in ./envs/phys-581-2021/lib/python3.9/site-packages (from requests>=2.5.0->Sphinx>=2.1->sphinxcontrib-bibtex) (1.26.6)
   Requirement already satisfied: charset-normalizer~=2.0.0 in ./envs/phys-581-2021/lib/python3.9/site-packages (from requests>=2.5.0->Sphinx>=2.1->sphinxcontrib-bibtex) (2.0.0)
   Requirement already satisfied: idna<4,>=2.5 in ./envs/phys-581-2021/lib/python3.9/site-packages (from requests>=2.5.0->Sphinx>=2.1->sphinxcontrib-bibtex) (3.2)
   Requirement already satisfied: zipp>=0.5 in ./envs/phys-581-2021/lib/python3.9/site-packages (from importlib-metadata->mmf-setup) (3.5.0)
   Requirement already satisfied: pyparsing>=2.0.2 in ./envs/phys-581-2021/lib/python3.9/site-packages (from packaging->Sphinx>=2.1->sphinxcontrib-bibtex) (2.4.7)
   Building wheels for collected packages: sphinxcontrib-zopeext
     Building wheel for sphinxcontrib-zopeext (setup.py): started
     Building wheel for sphinxcontrib-zopeext (setup.py): finished with status 'done'
     Created wheel for sphinxcontrib-zopeext: filename=sphinxcontrib_zopeext-0.2.4-py3-none-any.whl size=5988 sha256=c69b6b753152973c7b6bfbe3d7f1cb188972c8bc4a56fe53ed5af92602a0da2a
     Stored in directory: /tmp/pip-ephem-wheel-cache-ejlglin8/wheels/36/50/14/83293d1a160781dcf9648481020f775bac6596ab55ffcba75a
   Successfully built sphinxcontrib-zopeext
   Installing collected packages: latexcodec, pybtex, zope.interface, tomlkit, pybtex-docutils, sphinxcontrib-zopeext, sphinxcontrib-bibtex, mmf-setup
   Successfully installed latexcodec-2.0.1 mmf-setup-0.4.3 pybtex-0.24.0 pybtex-docutils-1.0.1 sphinxcontrib-bibtex-2.3.0 sphinxcontrib-zopeext-0.2.4 tomlkit-0.7.2 zope.interface-5.4.0
   The project is ready to run commands.
   Use `anaconda-project list-commands` to see what's available.
   source $ANACONDA2020/bin/activate root && CONDA_EXE=mamba anaconda-project run init  # Custom command: see anaconda-project.yaml
   Installed kernelspec phys-581-2021 in /home/user/.local/share/jupyter/kernels/phys-581-2021
   if ! grep -Fq 'source $ANACONDA2020/bin/activate /home/user/physics-581-physics-inspired-computation/envs/phys-581-2021' ~/.bash_aliases; then \
     echo 'source $ANACONDA2020/bin/activate /home/user/physics-581-physics-inspired-computation/envs/phys-581-2021' >> ~/.bash_aliases; \
   fi
   make[1]: Entering directory '/home/user/physics-581-physics-inspired-computation'
   find . -name ".ipynb_checkpoints" -prune -o \
          -name "_ext" -prune -o \
          -name "envs" -prune -o \
          -name "*.ipynb" -o -name "*.md" \
          -exec jupytext --sync {} + 2> >(grep -v "is not a paired notebook" 1>&2)
   [jupytext] Reading ./README.md in format md
   [jupytext] Reading ./Docs/Assignments/Assignment-1.md in format md
   [jupytext] Updating ./Docs/Assignments/Assignment-1.ipynb
   [jupytext] Updating ./Docs/Assignments/Assignment-1.md
   [jupytext] Reading ./Docs/Assignments/Assignment-0.md in format md
   [jupytext] Updating ./Docs/Assignments/Assignment-0.ipynb
   [jupytext] Updating ./Docs/Assignments/Assignment-0.md
   [jupytext] Reading ./Docs/index.md in format md
   [jupytext] Reading ./Docs/Syllabus.md in format md
   [jupytext] Reading ./Docs/Syllabus_Assignments.md in format md
   [jupytext] Reading ./Docs/Notes.md in format md
   [jupytext] Reading ./Docs/References.md in format md
   [jupytext] Reading ./Docs/Syllabus_Prerequisites.md in format md
   [WARNING] Deprecated: --atx-headers. Use --markdown-headings=atx instead.
   [jupytext] Reading ./Docs/CourseInfo.md in format md
   [jupytext] Reading ./Docs/README.md in format md
   [jupytext] Reading ./Docs/Assignments.md in format md
   [jupytext] Reading ./Docs/Links.md in format md
   [jupytext] Reading ./Docs/Reading.md in format md
   [jupytext] Reading ./Notes.md in format md
   make[1]: Leaving directory '/home/user/physics-581-physics-inspired-computation'

   real	5m14.144s
   user	3m4.389s
   sys	0m27.096s
   ```
   
   Now when you log out, then reconnect to the CoCalc project, it should automatically
   activate the `phys-581-2021` environment due to the line at the end of
   `~/.bash_aliases`:
   
   ```console
   MacOSX $ ssh smc581private
   (phys-581-2021) ~$ type python3
   python3 is /home/user/physics-581-physics-inspired-computation/envs/phys-581-2021/bin/python3
   ```
   </details>
   
At this point you can start using the project, viewing the notebooks, running and
editing code, etc.  If you need additional packages, you should add them with
`anaconda-project`.  I recommend the following strategy. See if the package is available
from the default conda repos, and install from there if it is available.  If it is only
available from [`conda-forge`] then explicitly install it from there, otherwise use `pip`:
   
```bash
conda search --override-channels -c defaults sphinx
conda search --override-channels -c conda-forge uncertainties
anaconda-project add-packages sphinx
anaconda-project add-packages conda-forge::uncertainties  # Not available in defaults
anaconda-project add-packages --pip mmf-setup             # Only available through pip
```

Note: I am explicitly using `--override-channels`: this is crucial on CoCalc for now as
the default `/ext/anaconda2020.02/.condarc` file has so many channels that `conda` will
run out of memory.

There are a few more things you should do if you are registered in the course:

5. [Create SSH keys](https://doc.cocalc.com/project-settings.html#ssh-keys), and add
   them [to your CoCalc account](https://doc.cocalc.com/account/ssh.html) and [to your
   GitLab account](https://docs.gitlab.com/ee/ssh/).
   your project with SSH, forwarding your SSH agent.
4. Create a [GitLab] account and send the username to your instructor so that they can
   give you access to the [Resources project].
5. Create a [GitLab] repository for this course, and add this as a remote so that you
   can push your work to it.  *You may make this project public or private as you prefer,
   but note that private projects may have more limited access to CI resources.  See
   [GitLab pricing](https://about.gitlab.com/pricing/) for details.*

### GitLab Fork

1. Create an account on [GitLab].
2. Fork the [Official Course Repository] (I suggest making this private since your grade
   is associated with the tests, but you are welcome to make it public whenever you are
   comfortable.)
3. Add your instructor `@mforbes` as a **Developer** for the project:

   * **Project Information > Members**
   
4. Clone this to your [CoCalc] project and/or your computer.  Do your work etc. and push
   your changes.
5. Trigger the CI pipeline if it was not triggered by your push.

   * **CI/CD > Pipelines > Run pipeline**

6. Add the badges *(I don't know how to automate this or store this in a file
   yet... could maybe use [the Badges API](https://docs.gitlab.com/ee/api/project_badges.html))*:

   * **Settings > General > Badges**

    The following list the required fields:
    
    ```
    Name
    Link
    Badge image URL
    ```
    
    ```
    Docs
    https://wsu-phys-581-fall-2021.readthedocs.io/en/latest/?badge=latest
    https://readthedocs.org/projects/wsu-phys-581-fall-2021/badge/?version=latest
    ```
    ```
    Pipeline
    https://gitlab.com/%{project_path}
    https://gitlab.com/%{project_path}/badges/%{default_branch}/pipeline.svg
    ```
    ```
    Tests
    https://gitlab.com/%{project_path}
    https://gitlab.com/%{project_path}/-/jobs/artifacts/%{default_branch}/raw/_artifacts/test-badge.svg?job=test
    ```
    ```
    Coverage
    https://gitlab.com/%{project_path}
    https://gitlab.com/%{project_path}/-/jobs/artifacts/%{default_branch}/raw/_artifacts/coverage-badge.svg?job=test
    ```
    ```
    Assignment-0
   https://gitlab.com/%{project_path}
    https://gitlab.com/%{project_path}/-/jobs/artifacts/%{default_branch}/raw/_artifacts/test-0-badge.svg?job=test-0
    ```
    ```
    Assignment-1
    https://gitlab.com/%{project_path}
    https://gitlab.com/%{project_path}/-/jobs/artifacts/%{default_branch}/raw/_artifacts/test-1-badge.svg?job=test-1
    ```

    etc.

### Optional: SSH Keys

Typing your password every time you want to pull or push quickly gets tiring.  A better
option is to use [SSH] to authenticate, connect, and to forward your agent so you don't
need to re-authenticate.  The basic ideas are explained in [connecting to CoCalc with
SSH](https://doc.cocalc.com/project-settings.html#ssh-keys).

### Optional: GitHub Mirror

You can create a mirror on [GitHub] of your [GitLab] project which is updated whenever
you commit to your `main` branch.  Maintaining a [GitHub] mirror like this allows you to
use the [GitHub CI] tools, which differ somewhat from those on [GitLab].  In particular,
[LGTM] integration is quite interesting.

3. *(Optional)* Create an account on [GitHub].


## References

* [Python Tutorial](https://docs.python.org/3/tutorial/): This is the definative tutorial for the python language.  If you have not read this and plan to use python, then you should.
* [NumPy Tutorial](https://numpy.org/numpy-tutorials/): Growing repository of tutorials for using NumPy.  Being able to "think" in terms of arrays *(vectorization)* can greatly simplify your understanding of algorithms, while simultaneously improving your code, both from a performance and a reliability standpoint.  Not every problem benefits from this approach, but many of those in physics do.  *(We should try to [contribute](https://github.com/numpy/numpy-tutorials) to these.)*
* [Hypermodern Python](https://cjolowicz.github.io/posts/hypermodern-python-01-setup/): Deals with issues about packaging, testing, etc.  I plan to follow this (with some modifications discussed in [Hypothes.is annotations](https://hypothes.is/groups/z7AoNvZ1/computing) to setup the coding framework.



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
anaconda-project add-packages conda-forge::uncertainties
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

[CoCalc]: <https://cocalc.com> "CoCalc: Collaborative Calculation and Data Science"
[Conda]: <https://docs.conda.io/en/latest/> "Conda: Package, dependency and environment management for any language—Python, R, Ruby, Lua, Scala, Java, JavaScript, C/ C++, FORTRAN, and more."
[Miniconda]: <https://docs.conda.io/en/latest/miniconda.html> "Miniconda is a free minimal installer for conda."
[GitHub]: <https://github.com> "GitHub"
[GitLab]: <https://gitlab.com> "GitLab"
[GitHub CI]: <https://docs.github.com/en/actions/guides/about-continuous-integration> "GitHub CI"
[LGTM]: <https://lgtm.com/> "Continuous security analysis: A code analysis platform for finding zero-days and preventing critical vulnerabilities"
[Git]: <https://git-scm.com> "Git"
[Heptapod]: <https://heptapod.net> "Heptapod: is a community driven effort to bring Mercurial SCM support to GitLab"
[Jupyter]: <https://jupyter.org> "Jupyter"
[Jupytext]: <https://jupytext.readthedocs.io> "Jupyter Notebooks as Markdown Documents, Julia, Python or R Scripts"
[Mercurial]: <https://www.mercurial-scm.org> "Mercurial"
[Official Course Repository]: <https://gitlab.com/wsu-courses/physics-581-physics-inspired-computation/> "Official Physics 581 Repository hosted on GitLab"
[Resources project]: <https://gitlab.com/wsu-courses/physics-581-physics-inspired-computation_resources> "Private course resources repository."

[Shared CoCalc Project]: <https://cocalc.com/projects/74852aba-2484-4210-9cf0-e7902e5838f4/> "581-2021 Shared CoCalc Project"

[WSU Courses CoCalc project]: <https://cocalc.com/projects/c31d20a3-b0af-4bf7-a951-aa93a64395f6>
[WSU Physics]: <https://physics.wsu.edu> "WSU Physics Department"
[file an issue]: <https://gitlab.com/wsu-courses/physics-581-physics-inspired-computation/-/issues> "Issues on the class GitLab project."
[hg-git]: <https://hg-git.github.io> "The Hg-Git mercurial plugin"
[`mmf-setup`]: <https://pypi.org/project/mmf-setup/> "PyPI mmf-setup page"
[`conda-forge`]: <https://conda-forge.org/> "A community-led collection of recipes, build infrastructure and distributions for the conda package manager."
