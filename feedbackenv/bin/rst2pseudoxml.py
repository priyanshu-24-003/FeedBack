#!/run/media/priyanshu-first-of-his-name/New Volume/LIFE_Of_ENJOYMENT/Attention_concentration/A_C_1/Mislaneous_Process/MLoptionized_Flow/2_Mlops/MLOPS_26th_Project_Internship_Job/Learnings/20.21.22.23.24.25/FeedBack/feedbackenv/bin/python3

# $Id: rst2pseudoxml.py 4564 2006-05-21 20:44:42Z wiemann $
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
A minimal front end to the Docutils Publisher, producing pseudo-XML.
"""

try:
    import locale
    locale.setlocale(locale.LC_ALL, '')
except:
    pass

from docutils.core import publish_cmdline, default_description


description = ('Generates pseudo-XML from standalone reStructuredText '
               'sources (for testing purposes).  ' + default_description)

publish_cmdline(description=description)
