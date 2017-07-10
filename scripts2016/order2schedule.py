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
from datetime import datetime, timedelta
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
schedule = defaultdict(lambda : defaultdict(list))
sessions = defaultdict()
session_times = defaultdict()

for file in args.order_files:
    for line in open(file):
        subconf_name = file.split('/')[1]
        line = line.rstrip()

        #print "LINE", line

        if line.startswith('*'):
            # This sets the day
            day, date, year = line[2:].split(', ')
            if not (day, date, year) in dates:
                dates.append((day, date, year))

        elif line.startswith('='):
            # This names a parallel session that runs at a certain time
            time_range, session_name = line[2:].split(' ', 1)
            sessions[session_name] = Session(line, (day, date, year))

        elif line.startswith('+'):
            # This names an event that takes place at a certain time
            timerange, title = line[2:].split(' ', 1)

            if "poster" in title.lower() or "demo" in title.lower() or "best paper session" in title.lower():
                session_name = title
                sessions[session_name] = Session(line, (day, date, year))
                sessions[session_name].poster = True

        elif re.match(r'^\d+', line) is not None:
            id, rest = line.split(' ', 1)
            if re.match(r'^\d+:\d+-+\d+:\d+', rest) is not None:
                title = rest.split(' ', 1)
            else:
                title = rest
            if re.search('\d+/TACL', title[-1]):
                subconf_name = 'tacl'           

            if not sessions.has_key(session_name):
                sessions[session_name] = Session("= %s %s" % (timerange, session_name), (day, date, year))
    
            sessions[session_name].add_paper(Paper(line, subconf_name))

# Take all the sessions and place them at their time
for session in sorted(sessions.keys()):
    day, date, year = sessions[session].date
    papers = sessions[session].papers
    if sessions[session].time == 'Session': # parallel session
        times_start = [datetime.strptime(p.time[:5], '%H:%M') for p in papers]
        times_end = [datetime.strptime(p.time[7:], '%H:%M') for p in papers]
        timestart = min(times_start).strftime('%H:%M')
        timeend = max(times_end).strftime('%H:%M')
        timerange = timestart + '--' + timeend
        
        timeranges = schedule[(day, date, year)].keys()
        if timerange in schedule[(day, date, year)].keys():
            schedule[(day, date, year)][timerange].append(sessions[session])
        else: # there might be blank slots
            timestarts = [x[:5] for x in timeranges]
            timeends = [x[7:] for x in timeranges]
            if timestart in timestarts:
                timeend = timeranges[timestarts.index(timestart)][7:]
                timerange = timestart + '--' + timeend
            elif timeend in timeends:
                timestart = timeranges[timeends.index(timeend)][:5]
                timerange = timestart + '--' + timeend
            schedule[(day, date, year)][timerange].append(sessions[session])
    else: # session already has timerange
        timerange = sessions[session].time
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

        print parallel_sessions
        print poster_sessions

        # PARALLEL SESSIONS
        # Print the Session overview (single-page at-a-glance grid)
        if len(parallel_sessions) > 0:
            session_num = parallel_sessions[0].num

            path = os.path.join(args.output_dir, '%s-parallel-session-%s.tex' % (day, session_num))
            out = open(path, 'w')
            print >> sys.stderr, "\\input{%s}" % (path)
            
            print >>out, '\\clearpage'
            print >>out, '\\setheaders{Session %s}{\\daydateyear}' % (session_num)

            print len(parallel_sessions), len(poster_sessions)
            out1 = 'UNDEFINED'
            out2 = 'UNDEFINED'         
            if len(parallel_sessions) == 2:
                out1 = '\\begin{TwoSessionOverview}{Session %s}{\daydateyear}' % (session_num)
                out2 = '\\end{TwoSessionOverview}\n'
            elif len(parallel_sessions) == 3:
                out1 = '\\begin{ThreeSessionOverview}{Session %s}{\daydateyear}' % (session_num)
                out2 = '\\end{ThreeSessionOverview}\n'
            elif len(parallel_sessions) == 5:
                out1 = '\\begin{SessionOverview}{Session %s}{\daydateyear}' % (session_num)
                out2 = '\\end{SessionOverview}\n'
            elif len(parallel_sessions) == 6:
                out1 = '\\begin{SixSessionOverview}{Session %s}{\daydateyear}' % (session_num)
                out2 = '\\end{SixSessionOverview}\n'                
            elif len(parallel_sessions) == 7:
                out1 = '\\begin{SevenSessionOverview}{Session %s}{\daydateyear}' % (session_num)
                out2 = '\\end{SevenSessionOverview}\n'
            
            print >>out, out1
                # print the session overview
            for session in parallel_sessions:
                print >>out, '  {%s}' % (session.desc)
                #times = [p.time.split('--')[0] for p in parallel_sessions[0].papers]

                times = []
                print "DEBUG", times, session.time
                for u in range(len(parallel_sessions)):
                    try:
                        times.extend([p.time.split('--')[0] for p in parallel_sessions[u].papers])
                    except:
                        pass

                if len(times) == 0:
                    times.append(session.time.split('--')[0])

            num_papers = max([len(x.papers) for x in parallel_sessions])
            for paper_num in range(num_papers):
                if paper_num > 0:
                    print >>out, '  \\hline'
                t = times[paper_num]
                if len(t.split(':')[0]) == 1:
                    t = '0' + t
                print >>out, '  \\marginnote{\\rotatebox{90}{%s}}[2mm]' % (t)
                    
                papers = []
                for session in parallel_sessions:
                    try:
                        ts = [datetime.strptime(p.time[:5], '%H:%M').strftime('%H:%M') for p in session.papers]
                    except:
                        ts = [datetime.strptime(session.time[:5], '%H:%M').strftime('%H:%M')]
                    if t in ts:
                        p = session.papers[ts.index(t)]
#                        if len(parallel_sessions) >= 6:                    
#                            papers.append('\\papertableentrysmall{%s}' % (p.id))
#                        else:
                        papers.append('\\papertableentry{%s}' % (p.id))
                    else:
                        papers.append('')
                print >>out, ' ', ' & '.join(papers)
                print >>out, '  \\\\'

            print >>out, out2

            # Now print the papers in each of the sessions
            # Print the papers
            print >>out, '\\newpage'
            print >>out, '\\section*{Parallel Session %s}' % (session_num)
            for i, session in enumerate(parallel_sessions):
                print session.name
                print >>out, '\par\centerline{\\bfseries\\large Session %s: %s}\\vspace{1em}\\par' % (session.name, session.desc)
                for paper in session.papers:
                    print >>out, '\\paperabstract{\\day}{%s}{}{}{%s}' % (paper.time, paper.id)
                print >>out, '\\clearpage'

            print >>out, '\n'

            out.close()

        # POSTER SESSIONS
        for session in poster_sessions:
            path = os.path.join(args.output_dir, '%s-%s.tex' % (day, session.name.replace(' ', '-')))
            out = open(path, 'w')
            print 'POSTER', path
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
