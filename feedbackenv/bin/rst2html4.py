#!/run/media/priyanshu-first-of-his-name/New Volume/LIFE_Of_ENJOYMENT/Attention_concentration/A_C_1/Mislaneous_Process/MLoptionized_Flow/2_Mlops/MLOPS_26th_Project_Internship_Job/Learnings/20.21.22.23.24.25/FeedBack/feedbackenv/bin/python3

# $Id: rst2html4.py 7994 2016-12-10 17:41:45Z milde $
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
A minimal front end to the Docutils Publisher, producing (X)HTML.

The output conforms to XHTML 1.0 transitional
and almost to HTML 4.01 transitional (except for closing empty tags).
"""

try:
    import locale
    locale.setlocale(locale.LC_ALL, '')
except:
    pass

from docutils.core import publish_cmdline, default_description


description = ('Generates (X)HTML documents from standalone reStructuredText '
               'sources.  ' + default_description)

publish_cmdline(writer_name='html4', description=description)
