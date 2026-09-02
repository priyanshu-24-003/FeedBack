#!/run/media/priyanshu-first-of-his-name/New Volume/LIFE_Of_ENJOYMENT/Attention_concentration/A_C_1/Mislaneous_Process/MLoptionized_Flow/2_Mlops/MLOPS_26th_Project_Internship_Job/Learnings/20.21.22.23.24.25/FeedBack/feedbackenv/bin/python3

# $Id: rst2latex.py 5905 2009-04-16 12:04:49Z milde $
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
A minimal front end to the Docutils Publisher, producing LaTeX.
"""

try:
    import locale
    locale.setlocale(locale.LC_ALL, '')
except:
    pass

from docutils.core import publish_cmdline

description = ('Generates LaTeX documents from standalone reStructuredText '
               'sources. '
               'Reads from <source> (default is stdin) and writes to '
               '<destination> (default is stdout).  See '
               '<http://docutils.sourceforge.net/docs/user/latex.html> for '
               'the full reference.')

publish_cmdline(writer_name='latex', description=description)
