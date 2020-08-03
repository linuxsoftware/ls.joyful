ls.joyful
=========

.. image:: /docs/joyful-demo-0.png

About
------
Joyful is a `FullCalendar <https://fullcalendar.io>`_ front-end for the 
`Joyous <http://github.com/linuxsoftware/ls.joyous>`_ Wagtail Calendar.

Installation
------------
Follow the instructions for installing ls.joyous with the following additions for ls.joyful.

Install the package.

.. code-block:: console

    $ pip install ls.joyful

Add ls.joyful to your INSTALLED_APPS.

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'ls.joyful',
        'ls.joyous',
        'wagtail.contrib.modeladmin',
        ...
    ]

Usage
-----
After installing ls.joyful you will have the option of adding a 
Full calendar page.  This is much the same as a regular Joyous Calendar
page, but uses the FullCalendar javascript library to display the events.

Demo
----
Yet another demonstration Wagtail website `code <http://github.com/linuxsoftware/orange-wagtail-site>`_ | `live <http://demo.linuxsoftware.nz>`_

Getting Help
-------------
Please report bugs or ask questions using the `Issue Tracker <http://github.com/linuxsoftware/ls.joyful/issues>`_.

