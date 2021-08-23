# Syllabus

## Course Information

- **Instructor:** {{ instructor }}
- **Office:** {{ office }}
- **Office Hours:** {{ office_hours }}
- **Course Homepage:** {{ class_homepage }}
- **Class Number:** {{ class_number }}
- **Title:** "{{ class_name }}"
- **Credits:** 3
- **Meeting Time and Location:** {{ class_time }}, {{ class_room }},  Washington State University,
  Pullman, WA


```{contents}
```


## {ref}`sec:prerequisites`

```{toctree}
---
maxdepth: 2
---
Prerequisites
Assignments
```

There are no formal prerequisites for the course, but I will expect you to be
comfortable with the material discussed in the {ref}`sec:prerequisites` section, which
contains links to additional resources should you need to refresh your knowledge.
Please work with your classmates to try to share knowledge as needed.
Generally, I will expect familiarity with the following:

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
  of the software on your computer.  See the {ref}`sec:prerequisites` section for details
  and learning resources.


## Textbooks

There is no formal textbook, but the following (available electronically from the WSU
Library) will be useful: 

* [A. Gezerlis: "Numerical Methods in Physics with Python" (2020)](https://ntserver1.wsulibs.wsu.edu:2532/core/books/numerical-methods-in-physics-with-python/563DF013576DCC535668A100B8F7D2F9)

This covers many useful algorithms with a focus on implementing them from scratch rather than using them as black-box routines.  Another resource more focused on data science is by Jake VanderPlas:

* [J. VanderPlas: "Python Data Science Handbook"](https://ntserver1.wsulibs.wsu.edu:2171/lib/wsu/detail.action?docID=4746657&pq-origsite=primo):

Readings will be assigned as needed.  See {ref}`sec:References` for details and
additional resources.

## Grading

Grading will be largely automated: you are expected to maintain a project on [GitLab]
where you keep the code in a [Git] clone of the [Official Course Repository].  Your
projects should contain all of the code you develop for this course, including solutions
to the assignments.  This code should be well-documented, and well-tested using
[GitLab]'s continuous integration (CI) tools.

Each assignment (see {ref}`sec:assignments` for details) will be distributed as a set of
files made available through the `main` branch of the [Official Course Repository]: you
will be instructed when to pull and merge these with your project.  These assignments
will contain skeleton code and tests.  You will be expected to complete the skeleton
code so that the tests pass.

These will include python code with skeleton functions, class, etc. which you are
expected to complete, along with automated tests (which you must not modify) for the
assignment, and CI instructions such that these tests can be run on [GitLab], producing
a badge for that assignment.

Your numeric grade for the course will be the percentage of passing assignment test
badges for your code.  Thus, if there are 10 assignments in the course and
you have passing tests for 8 of those, you will have a grade of 80% to be converted to a
letter grade according to the following table:

| Percent P        | Grade     |
| ---------------- | --------- |
| 85% \<= P        | A-, A     |
| 70% \<= P \< 85% | B-, B, B+ |
| 55% \<= P \< 70% | C-, C, C+ |
| 40% \<= P \< 55% | D, D+     |
| P \< 40%         | F         |

As discussed in section {ref}`sec:assignments`, there will be two stages of testing for each
assignment.  Completion of the first stage tests will allow you to get up to a grade of
A-.  Successful completion of sufficient second stages will be required for an overall A
in the course.  *Currently there is no other mechanism for partial credit, but I will
attempt to implement this during the course.*

As a fail-safe, you will get a minimum grade of a B+ if you meet the following
requirements:

* You make a reasonable attempt to solve the assignments by writing functioning code in
  your project.  This code should be well documented, appropriately commented, and
  should follow best coding practices.
* You write comprehensive automated tests for your code which pass when run using the
  [GitLab] CI, resulting in at least 85% code coverage.
* You participate in at least one formal code review of either code pertaining to a
  project in your domain of focus, or a randomly selected assignment, where we go
  over your code as a class, looking for potential bugs, places for optimizing
  performance, etc.

The `main` branch of the [Official Course Repository] will meet these requirements, and
will provide a skeleton of all the code needed to make and run the tests.  Thus, you should be
able to easily maintain this standard as you develop code, obtaining a minimum
grade of B+ with modest effort.  I expect some of the assignments will be challenging,
so to obtain a grade of A will require some commitment and skill.

There will be no exams in this course.

## Topics
Exact topics and techniques will be chosen to match the interests and needs of the participants (who are expected to communicate these needs to the instructor in advance of the course), but may include:

* Case-studies: Part of the course will explore real-world examples of how physics has inspired solutions to hard problems in other fields of study.
  * [Renormalization Group Theory to understand traffic flow](https://discourse.iscimath.org/t/mar-17-renormalization-group-theory-the-systems-engineering-perspective/491).
* Root-finding and Optimization
  * Finding ground states and excited states in quantum mechanics.
  * Density Functional Theory (DFT)
  * Machine learning *(Probably not in the first year...)*
* Reaction/Diffusion networks:
  * Heat flow.
  * Hair follicle morphogenesis ([Turing's problem](https://en.wikipedia.org/wiki/The_Chemical_Basis_of_Morphogenesis)).
* Ordinary Differential equations and Boundary Value Problems:
  * Classical Mechanics
  * Classical Chaos
  * Time-dependent Schrödinger equation.
* Partial Differential Equations
  * Time-dependent Schrödinger equation/Time-dependent DFT (TDDFT)
  * Fluid dynamics *(Continuing from Matt's course)*.
    * Simple parallization: what to do when your data does not fit on a single node.  *(@m.duez)*
  * Numerical Relativity *(Probably not in the first year...)*
  * Finite element techniques + Green's Functions for wave dynamics *(Talk to Phil)*.
* Monte Carlo
  * Simulation of thermodynamic systems 
  * Numerical experiments with Renormalization Group
  * Quantum Monte Carlo (QMC)  *(Probably not in the first year...)*
* Bayesian Analysis
  * Linear and Non-linear model fitting which properly characterized errors.
  * Manifold reduction techniques.
* Data Analysis
  * How to access, store, and analyze data.
  * Clustering and searching in high dimensions. *(@gworthey)*


## Other Information

### COVID-19 Statement
Per the proclamation of Governor Inslee on August 18, 2021, **masks that cover both the
nose and mouth must be worn by all people over the age of five while indoors in public
spaces.**  This includes all WSU owned and operated facilities. The state-wide mask mandate
goes into effect on Monday, August 23, 2021, and will be effective until further
notice. 
 
Public health directives may be adjusted throughout the year to respond to the evolving
COVID-19 pandemic. Directives may include, but are not limited to, compliance with WSU’s
COVID-19 vaccination policy, wearing a cloth face covering, physically distancing, and
sanitizing common-use spaces.  All current COVID-19 related university policies and
public health directives are located at
[https://wsu.edu/covid-19/](https://wsu.edu/covid-19/).  Students who choose not to
comply with these directives may be required to leave the classroom; in egregious or
repetitive cases, student non-compliance may be referred to the Center for Community
Standards for action under the Standards of Conduct for Students.

### Academic Integrity

Academic integrity is the cornerstone of higher education.  As such, all members of the
university community share responsibility for maintaining and promoting the principles
of integrity in all activities, including academic integrity and honest
scholarship. Academic integrity will be strongly enforced in this course.  Students who
violate WSU's Academic Integrity Policy (identified in Washington Administrative Code
(WAC) [WAC 504-26-010(3)][wac 504-26-010(3)] and -404) will fail the course, will not
have the option to withdraw from the course pending an appeal, and will be Graduate:
6300, 26300 reported to the Office of Student Conduct.

Cheating includes, but is not limited to, plagiarism and unauthorized collaboration as
defined in the Standards of Conduct for Students, [WAC 504-26-010(3)][wac
504-26-010(3)]. You need to read and understand all of the [definitions of
cheating][definitions of cheating].  If you have any questions about what is and is not
allowed in this course, you should ask course instructors before proceeding.

If you wish to appeal a faculty member's decision relating to academic integrity, please
use the form available at \_communitystandards.wsu.edu. Make sure you submit your appeal
within 21 calendar days of the faculty member's decision.

Academic dishonesty, including all forms of cheating, plagiarism, and fabrication, is
prohibited. Violations of the academic standards for the lecture or lab, or the
Washington Administrative Code on academic integrity

### Students with Disabilities

Reasonable accommodations are available for students with a documented
disability. If you have a disability and need accommodations to fully
participate in this class, please either visit or call the Access
Center at (Washington Building 217, Phone: 509-335-3417, E-mail:
<mailto:Access.Center@wsu.edu>, URL: <https://accesscenter.wsu.edu>) to schedule
an appointment with an Access Advisor. All accommodations MUST be
approved through the Access Center. For more information contact a
Disability Specialist on your home campus.

### Campus Safety

Classroom and campus safety are of paramount importance at Washington
State University, and are the shared responsibility of the entire
campus population. WSU urges students to follow the “Alert, Assess,
Act,” protocol for all types of emergencies and the “[Run, Hide, Fight]”
response for an active shooter incident. Remain ALERT (through direct
observation or emergency notification), ASSESS your specific
situation, and ACT in the most appropriate way to assure your own
safety (and the safety of others if you are able).

Please sign up for emergency alerts on your account at MyWSU. For more
information on this subject, campus safety, and related topics, please
view the FBI’s [Run, Hide, Fight] video and visit [the WSU safety
portal][the wsu safety portal].

## Learning Outcomes

The main objective of this course is for students to be able to effectively use
numerical techniques to solve complex problems following principles of good software
engineering and reproducible computing.

1. **Reproducible Computing:** Write and communicate computational results in a way that
   allows one to reproduce these results in the future, possibly on different computing
   platforms.
2. **Problem Assessment:** Be able to assess complex problems to determine if computational
   techniques will contribute to their solutions.
3. **Choice of Algorithm/Technique:** Be able to identify which algorithms are appropriate for
   solving the computational problems.
4. **Implementation:** Be able to implement the chosen algorithm.
5. **Convergence and Performance Analysis:** Be able to quantify and understand the
   convergence and performance of the algorithm being used.
6. **Solution Assessment:** Be able to assess the validity of the solution.  For
   example, to quantify the uncertainties associated with the results, accounting for
   the accumulation of round-off, truncation, and discretization errors, with an
   understanding of the conditioning of both the problem and the algorithm.
7. **Communicate and Defend the Solution:** Communicate the results with peers,
   defending the approximations made, the accuracy of the techniques used, and
   the assessment of the solutions.  Demonstrate insight into the nature of the
   solutions, making appropriate generalizations, and providing intuitive
   descriptions of the quantitative behavior found from solving the problem.

These learning outcomes will be assessed through the assignments as follows:

* By maintaining a code repository subject to automated testing, students will have to
    master all skills needed for reproducible computing (1).
* Through the successful completion of their assignments, students will demonstrate the
    ability to choose a technique (3) and implement it (4).
* Class assignments will test both accuracy and performance of the code.  Passing the
    associated tests will require that students have understood the convergence and
    performance properties of there code (5).
* Code coverage will ensure that students implement tests for their code, assessing
    their solutions (6).
* Through code reviews and documentation, students will be required to communicate and
  defend their solutions (7).

## Expectations of the Student

Students are expected to:

1. Stay up to date with reading assignments.
2. Participate in online forums, both asking questions and addressing peers questions.
3. Identify areas of weakness, work with peers to understand difficult
   concepts, then present remaining areas of difficulty to the instructor for
   personal attention or for discussion in class.
4. Complete assignments on time, providing well crafted solutions to the posed problems
   that demonstrate mastery of the material through the [Learning
   Outcomes](#learning-outcomes) 1-7.
   
   Student's are encouraged to discuss their intended approach with peers and with the
   instructor, but must ultimately write their own code.

For each hour of lecture equivalent, students should expect to have a minimum
of two hours of work outside class.

## Reading Schedule

The following details the content of the course.  It essentially
follows the main textbook.  Content from the supplement will be
inserted as appropriate throughout. Details and further resources will
be included on the lecture pages on the {{ Canvas }} server.

### Course Outline
<!-- 16 Weeks -->

1. Introduction and Basic Principles *(~2-3 week)*
    - Structure of the course.
    - Establish accounts and appropriate projects on [CoCalc] and [GitLab]
    - Numerical Evaluation of functions: Round-off error etc. (Assignment 0).
    - The Monty Hall Problem: Simple Monte Carlo Analysis (Assignment 1).
2. Basic Techniques *(~2-3 weeks)*
    - Differentiation and Integration.
    - Optimization and Root Finding.
    - Interpolation: Splines, Polynomials, Radial Basis Functions (RBF), Gaussian
      Processes.
    - Loops, Arrays, etc.
    - Bases.
3. Curve Fitting/Cycle Finding *(~2 week)*
   - Finding cycles in data.
   - Least squares fitting.
   - Fourier analysis.
   - Other techniques.
   - Bayesian techniques.
4. Ordinary Differential Equations (ODEs) *(~1-2 week)*
   - Orbiting Planets.
   - Falling Objects.
   - Agent-Based Modeling.
5. Partial Differential Equations (PDFs) *(~2 weeks)*
   - Schrodinger Equation
   - Fluid Dynamics
   - Diffusion
6. Other Topics/Domain Specific Problems *(~4-6 weeks)*
   - Renormalization Group, Effective Theories
   - Cellular Automata
   - Domain specific problems designed to address challenging problems in the fields of
       study represented by participants in the class.
   - Visualization techniques.
   - Profiling and Optimization.

[communitystandards.wsu.edu]: https://communitystandards.wsu.edu/
[definitions of cheating]: https://apps.leg.wa.gov/WAC/default.aspx?cite=504-26-010
[run, hide, fight]: https://oem.wsu.edu/emergency-procedures/active-shooter/
[the wsu safety portal]: https://oem.wsu.edu/about-us/
[wac 504-26-010(3)]: https://apps.leg.wa.gov/WAC/default.aspx?cite=504-26
[SSH]: <https://en.wikipedia.org/wiki/Secure_Shell> "SSH on Wikipedia"
[CoCalc]: <https://cocalc.com> "CoCalc: Collaborative Calculation and Data Science"
[GitLab]: <https://gitlab.com> "GitLab"
[GitHub]: <https://github.com> "GitHub"
[Git]: <https://git-scm.com> "Git"
[Official Course Repository]: <https://gitlab.com/wsu-courses/physics-581-physics-inspired-computation/> "Official Physics 581 Repository hosted on GitLab"
