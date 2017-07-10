#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Matt Post, June 2014

"""
Generates the daily overviews for the main conference schedule. Amalgamates multiple order
iles containing difference pieces of the schedule and outputs a schedule for each day,
rooted in an optionally-supplied directory.

Usage:

 cat data/{papers,shortpapers,demos,srw}/order | order2schedule_overview.py

"""

import re, os
import sys, csv
import argparse
from handbook import *
from datetime import datetime
from collections import defaultdict

PARSER = argparse.ArgumentParser(description="Generate overview schedules for *ACL handbooks")
PARSER.add_argument("-output_dir", dest="output_dir", default="auto/papers")
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
schedule = defaultdict(lambda : defaultdict(list))
sessions = defaultdict()
session_times = defaultdict()

for line in sys.stdin:
    line = line.rstrip()

    # print "LINE", line

    if line.startswith('*'):
        day, date, year = line[2:].split(', ')
        if not (day, date, year) in dates:
            dates.append((day, date, year))

    elif line.startswith('='):
        str = line[2:]
        time_range, session_name = str.split(' ', 1)
        sessions[session_name] = Session(line, (day, date, year))

    elif line.startswith('+') or line.startswith('!'):
        timerange, title = line[2:].split(' ', 1)
        title, keys = extract_keywords(title)
        if keys.has_key('by'):
            title = "%s (%s)" % (title.strip(), keys['by'])
        session_name = None

        if not schedule[(day, date, year)].has_key(timerange):
            schedule[(day, date, year)][timerange] = []
        schedule[(day, date, year)][timerange].append(title)

    elif re.match(r'^\d+', line) is not None:
        id, rest = line.split(' ', 1)
        if re.match(r'^\d+:\d+-+\d+:\d+', rest) is not None:
            title = rest.split(' ', 1)
        else:
            #title = rest
            continue

        if not sessions.has_key(session_name):
            sessions[session_name] = Session("= %s %s" % (timerange, session_name), (day, date, year))

        sessions[session_name].add_paper(Paper(line, 'papers'))

# Take all the sessions and place them at their time
# Take all the sessions and place them at their time
for session in sorted(sessions.keys()):
    day, date, year = sessions[session].date
    papers = sessions[session].papers
    #print len(papers)
    try:
        times_start = [datetime.strptime(p.time[:5], '%H:%M') for p in papers]
        times_end = [datetime.strptime(p.time[7:], '%H:%M') for p in papers]
        timestart = min(times_start).strftime('%H:%M') 
        timeend = max(times_end).strftime('%H:%M')
        timerange = timestart + '--' + timeend
        #print(timerange)
    except:
        print 'error timerange'
        continue
    
    timeranges = schedule[(day, date, year)].keys()
    if timerange in schedule[(day, date, year)].keys():
        schedule[(day, date, year)][timerange].append(sessions[session])
    else: # might be paper missing
        timestarts = [x[:5] for x in timeranges]
        timeends = [x[7:] for x in timeranges]
        if timestart in timestarts:
            timeend = timeranges[timestarts.index(timestart)][7:]
            timerange = timestart + '--' + timeend
        elif timeend in timeends:
            timestart = timeranges[timeends.index(timeend)][:5]
            timerange = timestart + '--' + timeend
        schedule[(day, date, year)][timerange].append(sessions[session])

def sort_times(a, b):
    ahour, amin = a[0].split('--')[0].split(':')
    bhour, bmin = b[0].split('--')[0].split(':')
    if ahour == bhour:
        return cmp(int(amin), int(bmin))
    return cmp(int(ahour), int(bhour))

def minus12(time):
    hours, minutes = time.split(':')
    if hours.startswith('0'):
        hours = hours[1:]
    if int(hours) >= 13:
        hours = `int(hours) - 12`

    return '%s:%s' % (hours, minutes)

for date in dates:
    day, num, year = date
    path = os.path.join(args.output_dir, '%s-overview.tex' % (day))
    out = open(path, 'w')
    print >> sys.stderr, "Writing file", path
    print >>out, '\\section*{Overview}'
    print >>out, '\\renewcommand{\\arraystretch}{1.2}'
    print >>out, '\\begin{SingleTrackSchedule}'
    for timerange, events in sorted(schedule[date].iteritems(), cmp=sort_times):        
        start, stop = timerange.split('--')
        if stop[-1] == ':':
            stop = stop[:-1]
        print('start stop', date, start, stop, len(events))

        if len(events) >= 2:
            print 'Parallel', len(events)
            # Parallel sessions (assume there are at least 3)
            sessions = [x for x in events]

            # turn "Session 9A" to "Session 9"
            print(sessions[0])
            title = 'Session %s' % (sessions[0].num)
            num_parallel_sessions = len(sessions)
            rooms = ['\emph{\Track%cLoc}' % (chr(65+x)) for x in range(num_parallel_sessions)]
            # column width in inches
            width = 3.3 / num_parallel_sessions
            print >>out, '  %s & -- & %s &' % (start, stop)
            print >>out, '  \\begin{tabular}{|%s|}' % ('|'.join(['p{%.11fin}' % width for x in range(num_parallel_sessions)]))
            print >>out, '    \\multicolumn{%d}{l}{{\\bfseries %s}}\\\\\\hline' % (num_parallel_sessions,title)
            print >>out, ' & '.join([session.desc for session in sessions]), '\\\\'
            print >>out, ' & '.join(rooms), '\\\\'
            print >>out, '  \\hline\\end{tabular} \\\\'

        else:

            for event in events:
                # A regular event
                print >>out, '  %s & -- & %s &' % (start, stop)
                try:
                    loc = event.split(' ')[0].capitalize()
                except:
                    loc = 'locA'
                print >>out, '  {\\bfseries %s} \\hfill \emph{\\%sLoc}' % (event, loc)
                print >>out, '  \\\\'

    print >>out, '\\end{SingleTrackSchedule}'
    out.close()

