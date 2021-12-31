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

<!-- This includes another README.md rendering that will get updated if the file is
     changed so that we can see updates when using make doc-sever.  The reason is that,
     because we generate the main page using a literal include ({include} README.md...),
     the main page will only get updated if we change this index.md file.
     
     We do not include this extra link when we build on RTD.  We do this using the
     sphinx.ext.ifconfig extension:
     
     https://www.sphinx-doc.org/en/master/usage/extensions/ifconfig.html
-->

```{eval-rst}
.. ifconfig:: not on_rtd

   .. toctree::
      :maxdepth: 0
      :caption: "Includes (for autobuild):"
      :titlesonly:
      :hidden:

      README
   
```
