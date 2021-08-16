# Syllabus

# Phys. 521, Fall 2020: Classical Mechanics I

```{contents}
```



```{toctree}
---
maxdepth: 2
caption: "Prerequisites:"
---
Prerequisites
```


## Textbooks
I am not completely set on the text yet, but Alex Gezerlis' book may be a good reference:

* [A. Gezerlis: "Numerical Methods in Physics with Python" (2020)](https://ntserver1.wsulibs.wsu.edu:2532/core/books/numerical-methods-in-physics-with-python/563DF013576DCC535668A100B8F7D2F9)

It covers many useful algorithms with a focus on implementing them from scratch rather than using them as black-box routines.  Another resource more focused on data science is by Jake VanderPlas:

* [J. VanderPlas: "Python Data Science Handbook"](https://ntserver1.wsulibs.wsu.edu:2171/lib/wsu/detail.action?docID=4746657&pq-origsite=primo):


## Grading
Throughout the course, several problems will be posed for which students will be expected to develop software solutions.  I envisage running this like coding competitions: students will submit a program which meets a specific interface.  This will then be run on a sample set of problems, and the grade will be determined based on the performance of the submitted code (accuracy, speed, etc. – metrics will be specified as relevant for each individual problem).

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
----
# Request for faculty and students:
**Please tell me what computational techniques you would like to see offered in this course.**  This could come as the answer to a variety  of questions:

1. What problems come up in your research that require or could benefit from computational techniques?  *(Even if you don't know exactly what techniques would help, please start a discussion here and we can iterate to see if there is a good solution.)*
2. What computational techniques would help your students do their research or course-work?  *(If you already know which techniques would be useful.)*
3. What computational techniques would be useful for our students later in their careers?

*The goal of this course is to start building a solid computational background for our students to prepare them for their research and their careers: I need your help determining what is needed in other fields, so please don't hesitate to open the discussion here.*

Thanks,
Michael.


```{include} Prerequisites.md
```

# Syllabus

## Grading and Assessment

```{eval-rst}
.. default-role:: math
```

During the course you will receive points `P` by completing various activities.
Your grade at the end of the course will be determined by the following table
where `P` is the number of points you obtain by the end of the term.

| Points P       | Grade     |
| -------------- | --------- |
| 85 \<= P       | A-, A     |
| 70 \<= P \< 85 | B-, B, B+ |
| 55 \<= P \< 70 | C-, C, C+ |
| 40 \<= P \< 55 | D, D+     |
| P \< 40        | F         |

The following table shows how many point you may earn at most from each
component of the course:

> - 25: Homework
> - 25: Midterm Exams:
> - 25: Project
> - 25: Final Exam

### Project

There will be a project in this course.  Further details will be
discussed later: you may choose the topic, but must run your proposal
by the instructor.

### Final Exam

The final exam is scheduled for Thursday 12 December at 8:00am.

## Other Information

### Academic Integrity

Academic integrity is the cornerstone of higher education.  As such,
all members of the university community share responsibility for
maintaining and promoting the principles of integrity in all
activities, including academic integrity and honest
scholarship. Academic integrity will be strongly enforced in this
course.  Students who violate WSU's Academic Integrity Policy
(identified in Washington Administrative Code (WAC) [WAC
504-26-010(3)][wac 504-26-010(3)] and -404) will fail the course, will not have the
option to withdraw from the course pending an appeal, and will be
Graduate: 6300, 26300
reported to the Office of Student Conduct.

Cheating includes, but is not limited to, plagiarism and unauthorized
collaboration as defined in the Standards of Conduct for Students, [WAC
504-26-010(3)][wac 504-26-010(3)]. You need to read and understand all of the [definitions
of cheating][definitions of cheating].  If you have any questions about what is and is not
allowed in this course, you should ask course instructors before
proceeding.

If you wish to appeal a faculty member's decision relating to academic
integrity, please use the form available at
\_communitystandards.wsu.edu. Make sure you submit your appeal within 21
calendar days of the faculty member's decision.

Academic dishonesty, including all forms of cheating, plagiarism, and
fabrication, is prohibited. Violations of the academic
standards for the lecture or lab, or the Washington Administrative Code on
academic integrity

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

The main objective of this course is to enable students to explain physical
phenomena within the realm of classical mechanics, making appropriate
simplifying approximations to formulate and solve for the behavior of
mechanical systems using mathematical models, and communicating these results
to peers.

By the end of this course, the students should be able to take a particular
physical system of interest and:

1. **Understand the Physics:** Identify the appropriate quantities required to
   describe the system, making simplifying assumptions where appropriate with a
   quantitative understanding as to the magnitude of the errors incurred by
   making these assumptions.
2. **Define the Problem:** Formulate a well-defined model describing the
   dynamics of the system, with confidence that the model is solvable.  At this
   point, one should be able to describe a brute force solution to the problem
   that would work given sufficient computing resources and precision.
3. **Formulate the Problem:** Simplify the mathematical formulation of the
   problem as much as possible using appropriate theoretical frameworks such as
   the Lagrangian or Hamiltonian frameworks.
4. **Solve the Problem:** Use analytic and numerical techniques to solve the
   problem at hand.
5. **Assess the Solution:** Assess the validity of the solutions by applying
   physical principles such as conservation laws and dimensional analysis, use
   physical intuition to make sure quantities are of a reasonable magnitude and sign,
   and use various limiting cases to check the validity of the obtained
   solutions.
6. **Communicate and Defend the Solution:** Communicate the results with peers,
   defending the approximations made, the accuracy of the techniques used, and
   the assessment of the solutions.  Demonstrate insight into the nature of the
   solutions, making appropriate generalizations, and providing intuitive
   descriptions of the quantitative behavior found from solving the problem.

A further outcome relates to the department requirement for students to
demonstrate this proficiency through a series of general examinations, and a
more general requirement for the students to interact face-to-face with other
physicists.

7. **Proficiency**: Be able to demonstrate proficiency with these skills.  In
   particular, be able to rapidly formulate and analyze many classical
   mechanics problems without external references.

These learning outcomes will be assessed as follows:

**Assignments:**

: Throughout the course, students will be expected to demonstrate outcomes 1-6
  applied to well-formulated problems demonstrating the techniques currently
  being taught (see the following [Course Outline]).  Successful completion
  of the assignments will assess the student's ability with these skills while
  they have access to external resources such as the textbook, and without
  stringent time constraints.  A peer-grading component of the course will
  help ensure that written solutions effectively communicate the results as
  per outcome 6.

**Exams:**

: The proficiency of the students to rapidly apply these skills without
  external resources (outcome 7) will be assessed through time-limited midterm
  and final examinations.

**Forums:**

: Students will be expected to participate in online discussion forums,
  assessing their ability to communicate about classical mechanics.

**Final Project:**

: The ability of the students to analysis an unstructured mechanics problem in
  an open-ended context will be assessed through their completion and defense
  of a final class project in an area of their choosing.  This will give the
  students a chance to exercise their skills in a context much closer to that
  in which they will encounter while performing physics research.

## Expectations of the Student

Students are expected to:

1. Stay up to date with reading assignments as outlined in the [Reading
   Schedule][reading schedule].

2. Participate in the online forums, both asking questions and addressing peers
   questions.

3. Identify areas of weakness, work with peers to understand difficult
   concepts, then present remaining areas of difficulty to the instructor for
   personal attention or for discussion in class.

4. Complete assignments on time, providing well crafted solutions to the posed
   problems that demonstrate mastery of the material through the [Learning
   Outcomes][learning outcomes] 1-6.  Final solutions much be written using proper English,
   including **complete sentences** with a clear logical progression through
   all steps of the solution.  Excessive verbosity is not required, but the
   progression through the solution must be clear to the reader, along with a
   justification of all assumptions and approximations made.

   Submitted solutions should not contain incomplete or random attempts at
   solving a problem: they should contain a streamline approach proceeding
   directly and logically from the formulation of the problem to the solution.
   (Student's are encouraged to discuss their intended approach with peers and
   with the instructor **well before the deadline** in order to obtain the
   feedback required to formulate a proper solution for submission).

5. Find or formulate exam problems at a level appropriate for completion of the
   physics department comprehensive examinations, and practice solving these
   under exam conditions, seeking help from the instructor as required to
   develop the required proficiency of the material.

6. Choose a topic for the final project, and obtain approval from the
   instructor by **November 1**.

7. Complete the final project, and present at the end of semester (typically
   one evening during the last week of classes, but the final date will chosen
   by polling everyone's schedules.

8. Successfully complete both the midterm and final examinations.

For each hour of lecture equivalent, students should expect to have a minimum
of two hours of work outside class.

## Reading Schedule

The following details the content of the course.  It essentially
follows the main textbook.  Content from the supplement will be
inserted as appropriate throughout. Details and further resources will
be included on the lecture pages on the [Blackboard] server.

### Course Outline

1. Introduction and Basic Principles  (~1 week)

> - Why study classical mechanics?
> - Newtonian mechanics.
> - Symmetry and Conservation.
> - Central Forces
> - Kepler
> - Scattering

2. Accelerated Coordinate Systems (~1 week)

> - Change of coordinates
> - Centripetal acceleration
> - Coriolis effect

3. Lagrangian Dynamics (~2 weeks)

> - Why another formulation?
> - Constraints
> - Euler-Lagrange Equations
> - Calculus of Variations
> - Hamilton's Principle
> - Generalized momenta
> - The Path Integral approach to Quantum Mechanics

4. Small Oscillations (~1 week)

> - Normal modes
> - Linear Equations
> - Stability

5. Rigid Bodies (~1 week)

> - Moment of Inertia
> - Euler's Equations

6. Hamilton Dynamics (~2 weeks)

> - Canonical Transformations
> - Hamilton-Jacobi Theory
> - Action-Angle Variables
> - The Canonical Quantization approach to Quantum Mechanics

7. Strings, Waves, and Drums (~1 week)

> - Lagrangian for continuous systems
> - Boundary conditions
> - Numerical solutions of the wave equation

10. Non-linear Mechanics (SIII: Discrete Dynamical Systems) (~2 weeks)

> These topics will be introduced as we progress through the course,
> inserted into the appropriate locations.

11. Special topics and review.

> - How these topics will be covered depends on interest.  One option
>   is to discuss superfluidity with some numerical examples
>   demonstrating vortices, vortex dynamics, and related phenomena.
> - Duffing Oscillator
> - Stability Analysis
> - Chaos
> - Fluids
> - Special Relativity

[communitystandards.wsu.edu]: https://communitystandards.wsu.edu/
[definitions of cheating]: https://apps.leg.wa.gov/WAC/default.aspx?cite=504-26-010
[run, hide, fight]: https://oem.wsu.edu/emergency-procedures/active-shooter/
[the wsu safety portal]: https://oem.wsu.edu/about-us/
[wac 504-26-010(3)]: https://apps.leg.wa.gov/WAC/default.aspx?cite=504-26
