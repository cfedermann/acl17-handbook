#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This script reads all the metadata and creates a bibtex file that contains
# all the information we need for the conference handbook. Unlike the bibtex
# file on the CDROM in the proceedings, bibtex labels correspond to submission
# numbers.

# Usage

# Written by Ulrich Germann, May 2012.
# Modified by Matt Post, June 2014.

from handbook import latex_escape
from paper_info import *
import sys, os, unicodedata, codecs
import re

sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

fdir = sys.argv[1] # i.e., $ACLPUB_ROOT/final
tag  = sys.argv[2] # e.g., main, demos, ws1, ...

try:
    os.makedirs("auto/%s" % (tag))
except:
    pass

try:
    os.makedirs("auto/abstracts")
except:
    pass

paper_ids = [int(n) for n in filter(lambda x: re.match(r'^\d+$', x), os.listdir(fdir))]
BIBFILE   = codecs.open("auto/"+tag+"/papers.bib",'w', encoding='utf-8')
for n in paper_ids:
    n = int(n)
    p = Paper("%s/%d/%d_metadata.txt" % (fdir, n, n))
    author = " and ".join(["%s, %s" % (a.last, a.first) for a in p.authors])
    sortname = ''.join([c for c in unicodedata.normalize('NFD', unicode(author))
                        if unicodedata.category(c) != 'Mn'])

#    print "%s %s -> %s" % (p.id, p.long, escape(p.long))
    print >>BIBFILE, "@INPROCEEDINGS{%s-%03d," % (tag, int(p.id))
    print >>BIBFILE, "   AUTHOR = {%s}," % author
    print >>BIBFILE, "   SORTNAME = {%s}," % sortname
    print >>BIBFILE, "   TITLE = {%s}}" % latex_escape(p.long)
    ABS = codecs.open("auto/abstracts/%s-%03d.tex" % (tag, n),'w', encoding='utf-8')
    print >>ABS, latex_escape(p.abstract)
    
