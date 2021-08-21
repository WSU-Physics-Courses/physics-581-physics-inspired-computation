(sec:assignments)=
# Assignments

Assignments will be distributed in two stages, announced through the course management
tools.

## Stage 1
For the first stage of assignment X, you will fetch the `main` branch of the [Official
Course Repository] and merge this into your repository.  This will contain the
assignment definition, formally specified as a set of skeleton functions in the file {{
course_package }}`/assignments/assignment_X.py`.
     
In addition, the `main` branch will contain files
`tests/assignment_X/test_official_assignment_X.py` demonstrating the desired behavior of
your functions.
     
You must edit the skeleton functions in {{ course_package
}}`/assignments/assignment_X.py` to make these tests pass.  As you do this, you should
consider whether any parts of your solution might be helpful with other problems, and
try to refactor these into more general tools that you keep in the {{ course_package }}
package for use in other assignments and in your future work.

Although you are not permitted to edit the `test_official_assignment_X.py` files,
you are encouraged to add additional tests to the `tests/assignment_X/` folder,
thoroughly testing your implementation of the solution in preparation for the
second stage.

Push your solution to your [GitLab] project, ensuring that the CI tests run, and
the corresponding assignment badge indicates success.

Once you are happy, tag your final revision `assignment_X:v1`.  This will be your
first submission, and must be completed before the specified assignment due date.
**You must keep this revision with the appropriate date-stamp to get credit.**
Successful on-time completion of this stage will be considered for partial credit,
and completing a sufficient number of assignments at level will ensure that you get
at least an A- in the course.

## Stage 2

After the due date, the second stage wiil begin.  An additional branch will be
pushed to your project with more comprehensive tests added to
`tests/assignment_X/test_official_assignment_X.py`.  These new tests will attempt to
break your code by looking for edge cases, testing performance, memory usage etc.
If you have properly tested your code, then these tests should pass, and you should
be proud (and may receive additional bonus points).  Otherwise you will need to
investigate to see which tests cause your code to fail, and then to implement
improvements in your code to get the tests passing again.

Once you are happy, tag your final revision `assignment_X:v2`.  This will be your
final submission.  It will be due before the last week of class.

## Notes

Ultimately, you will have access to all of the tests: it is therefore possible to "game"
the automated system by writing stubs that make the specific test-cases pass.  This
strategy can be very useful as part of what is called Test-Driven Development (TDD) and
is encouraged, however, must not be used as part of your final submission.

Some of your code will be selected for randomized code review.  If such stubs are found
in your final tagged submissions it will considered a form of cheating.  To be safe,
write your own tests with different input parameters etc. which will form the basis of
such a TDD strategy.
