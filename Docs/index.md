<!-- Physics 581: Physics Inspired Computational Techniques documentation master file, created by
   sphinx-quickstart on Tue Aug 10 12:38:54 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.
-->

<!-- Literally include the README.md file -->
```{include} README.md
```

<!-- We use a hack here to get a relative link in the TOC.  
     This will fail with LaTeX etc.
     https://stackoverflow.com/a/31820846/1088938 
     https://github.com/sphinx-doc/sphinx/issues/701 -->
```{toctree}
---
maxdepth: 2
caption: "Contents:"
titlesonly:
hidden:
---
GettingStarted
Syllabus
Syllabus_Prerequisites
Reading
Assignments
api/index
```

```{toctree}
---
maxdepth: 2
caption: "Other Content:"
hidden:
---
Notes
Projects
InstructorNotes
CoCalc
ClassLog
```

```{toctree}
---
maxdepth: 0
caption: "Includes (for autobuild):"
titlesonly:
hidden:
---
README
```
