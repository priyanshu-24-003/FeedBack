#!/run/media/priyanshu-first-of-his-name/New Volume/LIFE_Of_ENJOYMENT/Attention_concentration/A_C_1/Mislaneous_Process/MLoptionized_Flow/2_Mlops/MLOPS_26th_Project_Internship_Job/Learnings/20.21.22.23.24.25/FeedBack/feedbackenv/bin/python3

# Author:
# Contact: grubert@users.sf.net
# Copyright: This module has been placed in the public domain.

"""
man.py
======

This module provides a simple command line interface that uses the
man page writer to output from ReStructuredText source.
"""

import locale
try:
    locale.setlocale(locale.LC_ALL, '')
except:
    pass

from docutils.core import publish_cmdline, default_description
from docutils.writers import manpage

description = ("Generates plain unix manual documents.  " + default_description)

publish_cmdline(writer=manpage.Writer(), description=description)
