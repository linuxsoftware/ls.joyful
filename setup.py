# ----------------------
#  ls.joyful
# ----------------------

import sys
import os
import io
import subprocess
from pathlib import Path
from setuptools import setup, find_packages

# allow setup.py to be run from any path
here = Path(__file__).resolve().parent
os.chdir(str(here))

with io.open("README.rst", encoding="utf-8") as readme:
    README = readme.read()

setup(name="ls.joyful",
      use_scm_version={
          'write_to':  "ls/joyful/_version.py",
      },
      description="A FullCalendar front end to Joyous.",
      long_description=README,
      keywords=["calendar", "wagtail", "fullcalendar", "joyous", "joyful"],
      classifiers=["Development Status :: 4 - Beta",
                   "Framework :: Django",
                   "Framework :: Wagtail",
                   "Framework :: Wagtail :: 2",
                   "License :: OSI Approved :: BSD License",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python",
                   "Programming Language :: Python :: 3",
                   "Topic :: Office/Business :: Groupware",
                   "Topic :: Office/Business :: Scheduling",
                   "Topic :: Software Development :: Libraries :: Python Modules"
                  ],
      platforms="any",
      author="David Moore",
      author_email="david@linuxsoftware.co.nz",
      url="https://github.com/linuxsoftware/ls.joyful",
      license="BSD",
      packages=find_packages(where=".", exclude=["ls.joyful.tests"]),
      package_data={'ls.joyful': ["templates/joyful/*.html",
                                  "templates/joyful/*/*.html",
                                  "templates/joyful/*/*.xml",
                                  "static/joyful/css/*.css",
                                  "static/joyful/css/vendor/*.css",
                                  "static/joyful/img/*.png",
                                  "static/joyful/img/*.jpg",
                                  "static/joyful/js/*.js",
                                  "static/joyful/js/vendor/*.js",
                                  "locale/*/LC_MESSAGES/django.po",
                                  "locale/*/LC_MESSAGES/django.mo"
                                 ],
                   },
      setup_requires=["setuptools_scm"],
      install_requires=["ls.joyous>=1.0",
                        "wagtail>=2.0",],
      zip_safe=False,
     )
