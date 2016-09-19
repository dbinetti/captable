
**DEPRECATION NOTICE: This is no longer under active development.  However, if you're 
interested in the internals of how cap tables work it's still worth cloning.**


========
Captable
========

.. image:: https://travis-ci.org/dbinetti/captable.png
    :target: https://travis-ci.org/dbinetti/captable

.. image:: https://coveralls.io/repos/dbinetti/captable/badge.png?branch=master
    :target: https://coveralls.io/r/dbinetti/captable


Introduction
============

Captable is an application designed to manage capitalization tables.
Typically cap tables are managed though spreadsheets written by attorneys;
however, when capitalization structures get complicated (as often happens
with multiple finacings, convertibles, options, etc.,) it becomes a serious
pain to get Excel to do what you want it to do.  I originally wrote
this app to help me decide whether to finance or sell my last company
by conducting complicated what-if analyses that I didn't want to pay
lawyers to conduct.  (For the record, I had great attorneys -- they are
just really expensive.)

I've extensively documented throughout the application so that you can
understand how different calculations are made, so if you want to learn
more about financing structure I would encourage you to read the source
code.  I've included support for the most common terms that are used in
financings with explanations throughout.

