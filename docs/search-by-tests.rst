
.. warning:: Documentation status: **alpha**.

Introduction to source code *search by tests*
=============================================


Motivation
----------

    "Have a look at this piece of code that I’m writing--I’m sure it has been written before.
    I wouldn't be surprised to find it verbatim somewhere on GitHub." - `@kr1`_

Every piece of functionality in a software project
requires code that lies somewhere in the wide reusability spectrum that goes
form extremely custom and strongly tied to the specific implementation
to completely generic and highly reusable.

On the *custom* side of the spectrum there is all the code that defines the
features of the software and all the choices of its implementation. That one is code that need
to be written.

On the other hand a seasoned software developer is trained to spot
pieces of functionality that lie far enough on the *generic* side of the range
that with high probability a library already implements it
**and documents it well enough to be discovered with an internet search**.

In between the two extremes there is a huge gray area populated by pieces of functionality
that are not *generic* enough to obviously deserve a place in a library, but are
*common* enough that must have been already implemented by someone else for their
software. This kind of code is doomed to be re-implemented again and again
for the simple reason that **there is no way to search code by functionality**...

Or is it?


*Search by feature* and *search by tests*
-----------------------------------------


Tests validation
----------------

Another use for "pytest-wish" is, with a bit of additional work, to validate a project test suite.
If a test passes when passed an unexpected object there are two possibilities,
either the test is not strict enough and allows for false positives and needs update,
or the *hit* is actually a function you could use instead of your implementation.


Keywords:

 * Source code *search by feature*, *search by functionality*, *search by specification* or *nodev*
 * *Feature-specification test* and test suite or *Requirement-specification test*
 * *search by tests* or *Test-Driven no-Development*


.. _`@kr1`: https://github.com/kr1
