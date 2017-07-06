#!/usr/bin/env python 
# -*- coding: utf-8 -*-

"""
Generates the daily schedules for the main conference schedule. Amalgamates multiple order
files containing difference pieces of the schedule and outputs a schedule for each day,
rooted in an optionally-supplied directory.

Note: order file must be properly formatted.

Bugs: Workshop and program chairs do not like to properly format order files.

Usage: 

    cat data/{papers,shortpapers,demos,srw}/order | python order2schedule.py
"""

import re, os
import sys, csv
import argparse
from handbook import *
from collections import defaultdict

PARSER = argparse.ArgumentParser(description="Generate schedules for *ACL handbooks")
PARSER.add_argument("-output_dir", dest="output_dir", default="auto/papers")
PARSER.add_argument('order_files', nargs='+', help='List of order files')
args = PARSER.parse_args()

if not os.path.exists(args.output_dir):
    os.makedirs(args.output_dir)

def time_min(a, b):
    ahour, amin = a.split(':')
    bhour, bmin = b.split(':')
    if ahour == bhour:
        if amin < bmin:
            return a
        elif amin > bmin:
            return b
        else:
            return a
    elif ahour < bhour:
        return a
    else:
        return b

def time_max(a, b):
    if time_min(a, b) == a:
        return b
    return a

# List of dates
dates = []
schedule = defaultdict(defaultdict)
sessions = defaultdict()
session_times = defaultdict()

for file in args.order_files:
    subconf_name = file.split('/')[1]
    for line in open(file):
        line = line.rstrip()

        # print "LINE", line

        if line.startswith('*'):
            # This sets the day
            day, date, year = line[2:].split(', ')
            if not (day, date, year) in dates:
                dates.append((day, date, year))

        elif line.startswith('='):
            # This names a parallel session that runs at a certain time
            str = line[2:]
            time_range, session_name = str.split(' ', 1)
            sessions[session_name] = Session(line, (day, date, year))

        elif line.startswith('+'):
            # This names an event that takes place at a certain time
            timerange, title = line[2:].split(' ', 1)

            if "poster" in title.lower() or "demo" in title.lower() or "best paper session" in title.lower():
                session_name = title
                sessions[session_name] = Session(line, (day, date, year))

        elif re.match(r'^\d+', line) is not None:
            id, rest = line.split(' ', 1)
            if re.match(r'^\d+:\d+-+\d+:\d+', rest) is not None:
                title = rest.split(' ', 1)
            else:
                title = rest

            if not sessions.has_key(session_name):
                sessions[session_name] = Session("= %s %s" % (timerange, session_name), (day, date, year))

            sessions[session_name].add_paper(Paper(line, subconf_name))

# Take all the sessions and place them at their time
for session in sorted(sessions.keys()):
    day, date, year = sessions[session].date
    timerange = sessions[session].time
#    print >> sys.stderr, "SESSION", session, day, date, year, timerange
    if not schedule[(day, date, year)].has_key(timerange):
        schedule[(day, date, year)][timerange] = []
    schedule[(day, date, year)][timerange].append(sessions[session])

def sort_times(a, b):
    ahour, amin = a[0].split('--')[0].split(':')
    bhour, bmin = b[0].split('--')[0].split(':')
    if ahour == bhour:
        return cmp(int(amin), int(bmin))
    return cmp(int(ahour), int(bhour))

def minus12(time):
    if "--" in time:
        return '--'.join(map(lambda x: minus12(x), time.split('--')))

    hours, minutes = time.split(':')
    if hours.startswith('0'):
        hours = hours[1:]
    if int(hours) >= 13:
        hours = `int(hours) - 12`

    return '%s:%s' % (hours, minutes)

# Now iterate through the combined schedule, printing, printing, printing.
# Write a file for each date. This file can then be imported and, if desired, manually edited.
for date in dates:
    day, num, year = date
    for timerange, events in sorted(schedule[date].iteritems(), cmp=sort_times):
        start, stop = timerange.split('--')

        if not isinstance(events, list):
            continue

        parallel_sessions = filter(lambda x: isinstance(x, Session) and not x.poster, events)
        poster_sessions = filter(lambda x: isinstance(x, Session) and x.poster, events)

        # PARALLEL SESSIONS

        # Print the Session overview (single-page at-a-glance grid)
        if len(parallel_sessions) > 0:
            session_num = parallel_sessions[0].num

            path = os.path.join(args.output_dir, '%s-parallel-session-%s.tex' % (day, session_num))
            out = open(path, 'w')
            print >> sys.stderr, "\\input{%s}" % (path)
            
            print >>out, '\\clearpage'
            print >>out, '\\setheaders{Session %s}{\\daydateyear}' % (session_num)
            print >>out, '\\begin{ThreeSessionOverview}{Session %s}{\daydateyear}' % (session_num)
            # print the session overview
            for session in parallel_sessions:
                print >>out, '  {%s}' % (session.desc)
                times = [minus12(p.time.split('--')[0]) for p in parallel_sessions[0].papers]

            num_papers = len(parallel_sessions[0].papers)
            for paper_num in range(num_papers):
                if paper_num > 0:
                    print >>out, '  \\hline'
                print >>out, '  \\marginnote{\\rotatebox{90}{%s}}[2mm]' % (times[paper_num])
                papers = [session.papers[paper_num] for session in parallel_sessions]
                print >>out, ' ', ' & '.join(['\\papertableentry{%s}' % (p.id) for p in papers])
                print >>out, '  \\\\'

            print >>out, '\\end{ThreeSessionOverview}\n'

            # Now print the papers in each of the sessions
            # Print the papers
            print >>out, '\\newpage'
            print >>out, '\\section*{Parallel Session %s}' % (session_num)
            for i, session in enumerate(parallel_sessions):
                chair = session.chair()
                print >>out, '{\\bfseries\\large %s: %s}\\\\' % (session.name, session.desc)
                print >>out, '\\Track%cLoc\\hfill\\sessionchair{%s}{%s}' % (chr(i + 65),chair[0],chair[1])
                for paper in session.papers:
                    print >>out, '\\paperabstract{\\day}{%s}{}{}{%s}' % (paper.time, paper.id)
                print >>out, '\\clearpage'

            print >>out, '\n'

            out.close()

        # POSTER SESSIONS
        for session in poster_sessions:
            path = os.path.join(args.output_dir, '%s-%s.tex' % (day, session.name.replace(' ', '-')))
            out = open(path, 'w')
            print >> sys.stderr, "\\input{%s}" % (path)

            print >>out, '{\\section{%s}' % (session.name)
            print >>out, '{\\setheaders{%s}{\\daydateyear}' % (session.name)
            print >>out, '{\large Time: \emph{%s}\\hfill Location: \\PosterLoc}\\\\' % (minus12(session.time))
            chair = session.chair()
            if chair[1] != '':
                print >>out, '\\emph{\\sessionchair{%s}{%s}}' % (chair[0], chair[1])
            print >>out, '\\\\'
            for paper in session.papers:
                print >>out, '\\posterabstract{%s}' % (paper.id)
            print >>out

            out.close()
