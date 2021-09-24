Project Ideas
=============

Here are some ideas about how to use some of the things taught in this course to achieve
some interesting results.

## Improve `solve_ivp`:

There are issues with `solve_ivp`, especially with the adaptive refinement (see the
issues below).  One could try to improve this in several ways.  Low-hanging fruit would
be to develop some tests to help understand this issue.


* [RK45 produces wrong result for specific setting
  #9899](https://github.com/scipy/scipy/issues/9899): Demonstration of issues with the
  adaptive step refinement with the `RK45` (and `DoPri5`) methods.
* [Proposal: Update Runge-Kutta step size algorithms for predictable performance
  #9822](https://github.com/scipy/scipy/issues/9822): Proposal to improve the algorithm.
* [All `solve_ivp` issues](https://github.com/scipy/scipy/search?q=solve_ivp&type=issues).
