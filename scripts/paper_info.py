#!/usr/bin/env python 
# -*- coding: utf-8 -*-

# Module that provides access to the information in the aclpub metadata files.
# Written by Ulrich Germann, May 2012.
# Modified by Matt Post, May 2014.

import re
import sys
import codecs

def clean(str):
    """This is a list of nasty characters that people enter into their papers that break
    various things downstream. Add to it as you see fit."""
    str = str.replace(u"“",u"``")
    str = str.replace(u"”",u"''")
    str = str.replace(u' "',u" ``")
    str = str.replace(u'"',u"''")
    str = str.replace(u'ﬁ',u"fi")
    str = str.replace(u'ﬂ',u"fl")
    str = str.replace(u'’',u"'")
    str = str.replace(u'–',u"---")
    str = str.replace(u'&',u"\\&")
    str = str.replace(u'#',u"\\#")
    str = str.replace(u'_',u"\\_")
    
    return str

class Author:
    def __init__(self):
        self.first = "{}"
        self.last  = ""
        self.email = ""
        return

    def __str__(self):
        return self.first + " " + self.last

class Paper:
    def __init__(self):
        self.id       = 0
        self.short    = "" # short paper title
        self.long     = "" # long  paper title
        self.authors  = []
        self.session  = None
        self.abstract = ""
        return

    def __init__(self, fname):
        f = codecs.open(fname, encoding='utf-8')
        self.authors  = []
        abstract = []

        key = None
        for line in f:
            line = line.strip()

            if line == "" or line.startswith('=========='):
                continue

            x = re.split(r'#=%?=#', line)
            if len(x) == 2:
                (key,val) = x
            elif len(x) == 1:
                val = x[0]
                
            if key == "SubmissionNumber":
                self.id = val
            elif key == "FinalPaperTitle":
                self.long = clean(val)
            elif key == "ShortPaperTitle":
                self.short = val
            elif key.startswith('Author'):
                _, author_id, author_field, _ = re.split(r'[{}]+', key)
                author_id = int(author_id) - 1
                if len(self.authors) <= author_id:
                    self.authors.append(Author())
                if author_field == 'Lastname' and val != '':
                    self.authors[author_id].last = val
                elif author_field == 'Firstname' and val != '':
                    self.authors[author_id].first = val
                elif author_field == 'Email' and val != "":
                    self.authors[author_id].email = val

            elif key == "Abstract":
                #print "ABSTRACT:", val
                abstract.append(val)
            # else:
            #     print >> sys.stderr, "NO MATCH FOR", key

        # Certain UTF-8 characters should be replaced by latex code
        # or latex will complain bitterly.
        self.abstract = ' '.join(abstract)

        self.abstract = clean(self.abstract)


    def escaped_title(self):
        return re.sub(r'&', r'\\&', self.long)

    def __str__(self):
        return ", ".join([str(a) for a in self.authors]) + ": \"" + self.escaped_title() + "\""

    
