#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Matt Post, June 2014

"""
Generates the placards posted outside each room listing the sessions hosted there.

Usage:

  make_placards.py papers shortpapers tacl srw

Generates files in auto/placards, one for each session+day.

"""

import re
import os
import sys
import codecs
import argparse
import jinja2
from collections import defaultdict
from paper_info import Paper

sys.stdout = codecs.getwriter('utf8')(sys.stdout)

PARSER = argparse.ArgumentParser(description="Generate overview schedules for *ACL handbooks")
PARSER.add_argument("subconferences", nargs='+')
PARSER.add_argument("-template", dest="template", default='input/placard.jinja2', help="location of Jinja2 LaTeX template")
PARSER.add_argument("-output_dir", dest="output_dir", default="auto/placards")
PARSER.add_argument("-logo", dest="logo", default="content/fmatter/logos/harbor.png")
args = PARSER.parse_args()

if not os.path.exists(args.output_dir):
    os.makedirs(args.output_dir)

def minus12(time):
    hours, minutes = time.split(':')
    if hours.startswith('0'):
        hours = hours[1:]
    if int(hours) >= 13:
        hours = `int(hours) - 12`

    return '%s:%s' % (hours, minutes)

def minus12range(timerange):
    return '--'.join(map(minus12, timerange.split('--')))

class Vividict(dict):
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value

sessions = Vividict()

for subconf in args.subconferences:
    for line in open('data/%s/proceedings/order' % subconf):
        line = line.rstrip()

        # print "LINE", line

        if line.startswith('*'):
            day, date, year = line[2:].split(', ')
            daydate = '%s, %s' % (day, date)
            
        elif line.startswith('='):
            session_name = line[2:]
            match = re.match(r'Session \d([A-E])', session_name)
            if match is not None:
                session_track = match.group(1)
                if not sessions[daydate][session_track].has_key(session_name):
                    sessions[daydate][session_track][session_name] = {
                        'date': '%s, %s' % (day, date),
                        'title': session_name,
                        'track': session_track,
                        'papers': []
                    }

        elif re.match(r'\d+ \d+:\d+', line):
            """For the overview, we don't print sessions or papers, but we do need to look at
            oral presentations in order to determine the time range of the session (if any applies)"""
            if session_name is None:
                print "* WARNING: paper without a session name"
                continue

            if sessions[daydate][session_track].has_key(session_name):
                paper_id, timerange, _ = line.split(' ', 2)
                start, stop = timerange.split('--')

                p = Paper('data/%s/proceedings/final/%s/%s_metadata.txt' % (subconf, paper_id, paper_id))
                if not sessions[daydate][session_track][session_name].has_key('papers'):
                    sessions[daydate][session_track][session_name]['papers'] = []
                sessions[daydate][session_track][session_name]['papers'].append({
                    'time': minus12range(timerange),
                    'title': p.escaped_title(),
                    'authors': (', '.join(map(unicode, p.authors)))
                })

templateEnv = jinja2.Environment(loader = jinja2.FileSystemLoader( searchpath="." ))
template = templateEnv.get_template(args.template)

def sort_times(a, b):
    ahour, amin = a['time'].split('--')[0].split(':')
    bhour, bmin = b['time'].split('--')[0].split(':')
    if ahour == bhour:
        return cmp(int(amin), int(bmin))
    return cmp(int(ahour), int(bhour))

for day, data in sessions.iteritems():
    for track in data.keys():

        all_data = {
            'date': day,
            'sessions': [],
            'track': track,
        }

        for session in sorted(data[track].keys()):
            all_data['sessions'].append({
                'title': session,
                'papers': sorted(data[track][session]['papers'], lambda x,y: sort_times(x,y))
            })

        out = codecs.open('%s/%s-%s.tex' % (args.output_dir, day, track), 'w', 'utf-8')
        out.write(template.render(all_data))
        out.close()
