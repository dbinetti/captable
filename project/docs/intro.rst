Captable
--------

Note
====
This is in early alpha.  I'm a fan of releasing stuff early even when
it isn't ready.  But simply be aware: it isn't ready.  It is very rough,
raw, and altogether unsuitable for production.


Introduction
============

This application is designed to manage capitalization tables.  Typically cap tables are managed though spreadsheets written by attorneys; however, when capitalization structures get complicated (as often happens with multiple finacings, convertibles, options, etc.,) it becomes a serious pain to get Excel to do what you want it to do.  I originally wrote this app to help me decide whether to finance or sell my last company by conducting complicated what-if analyses that I didn't want to pay lawyers to conduct.  (For the record, I had great attorneys -- they are just really expensive.)

I've extensively documented throughout the application so that you can understand how different calculations are made, so if you want to learn more about financing structure I would encourage you to read the source code.  I've included support for the most common terms that are used in financings with explanations throughout.

If you have any suggestions for future improvements or find bugs please let me know.  I hope this tool will be used by entrepreneurs who are frustrated by Excel and find code a better vehicle by which to run financial calculations.

Features
========
- Handles convertibles.
- Handles stacked or sequenced preferences in liquidation.
- (more)

Installation
============
- Standard django installation
- Create admin

Tutorial
========

1.  Log in as admin.
2.  Add a new company.
3.  Go to your user and add that new company to your permisssions.
4.  Add all your securities.
5.  Add all your investors.
6.  Add shareholders attached to those investors (could be the same name
as the investors.)
7.  Add your certificates, meaning your stock certificates, options granted,
convertible notes, etc.

Examples
========
To see a fairly complicated example, load the 'example' fixture, go into
the admin and grant yourself permission through the MobileUser class.

Tests
=====
Tests are all currently broken.

