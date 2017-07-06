If you're reading this, it's likely because you've been asked to
assemble an *ACL handbook. Congratulations!  

You should start your preparation by clearing the entire week before
the printed deadline --- really.  The process of assembling the
handbook is a little bit of scripting and auto-generation followed by
an immense manual effort. You will take the proceedings from the
various workshops and pieces of the main conference, use the scripts
in the `scripts/` subdirectory to generate some LaTeX, and then
hand-assemble and munge everything until it is complete. Then you will
pore through it finding and correcting errors. You will find many of
these errors after you have uploaded the document to the printer, and
the last errors will not be found until after printing has begun.

On the positive side, it can be a very satisfying endeavor, and you
have the consolation that you are producing something very useful to
all the conference attendees, and also something you will likely be
credited for. Unlike the bulk of the work of conference organization,
your labor is visible and immediate.

This guide is intended for Publications Chairs (who I think should be
doing the job of assembling the handbook) and --- assuming my advice
is not heeded --- the Handbook chair. I hope that the information
provided here will be of some aid to you.
  
# Contents of a good handbook

A good conference handbook should have the following

- A nice, customized cover
- Letters from the General Chair and PC Chairs
- Schedules for the main conference, workshops, and any co-located conferences
- Overviews for each day that summarize the main events
- An "at-a-glance" overview page for each parallel session listing times, 
  locations, titles, and authors
- Abstracts for all papers presented in the main conference
- Full pages for special events (the banquet, business meeting, special
  awards and ceremonies)
- A perfect index, pointing to any and every mention of a name within
  the document, and containing no duplicate names (with spelling variations)
- A local guide with restaurants, area attractions, etc
- Sponsors and ads

# Some terminology

- The conference **proceedings** is the book containing all the
  conference's accepted papers and hosted in the
  [ACL anthology](http://aclweb.org/anthology). This is also sometimes
  called the **book**. Typically, separate books are produced for
  short and long papers, the student research workshop, and
  demonstrations. This is in contrast to the conference **handbook**,
  which is used to navigate the actual conference, and which this
  repository helps you to build.
  
- **ACLPUB** is the tool used to assemble the proceedings for a
  conference. This was, I believe, written in the early 2000s by Jason
  Eisner and Philipp Koehn. It usually consists of a directory named
  `proceedings/`, within which are papers, paper metadata, files used to
  generate the proceedings PDF, and, most importantly for handbook,
  the `order` file, which specifies the conference schedule.
  
- **START** is the online system used to manage paper submission,
  reviewing, acceptance / rejection, and so on. It knows about ACLPUB, and provides interfaces
  for editing the `order` file (directly or via their ScheduleMaker
  tool) and for generating the proceedings.tgz files.
  
- **Softconf** is the company that develops START

- **Subconferences**. Conferences hosted in START are assigned a top-level
  directory, e.g., `softconf.com/acl2014`. Beneath this are individual
  "subconferences" representing the workshops and also pieces of the
  the main conference. Main conference papers are typically hosted at
  `papers/`, short papers at `shortpapers`, and so on for "demos",
  "srw", "tutorials", and "tacl". Different sessions are
  self-contained and isolated and do not know about each other or have
  the ability to reference each other. The main conference spreads
  across multiple sessions, while workshops are typically contained in
  a single one.

# Main conference versus workshops

There are two main types of events you have to format for: the main
conference, and workshops. The technical distinction pertinent to
producing the handbook is that 

- Main conferences are multi-track and require you to assemble
  schedules from multiple sessions whose schedules may be interleaved.
  Traditionally, these are main conference papers, short papers,
  demos, student research workshop papers, tutorials, and, since 2013,
  TACL papers.
- Workshops are single-track: the schedule and all papers are
contained in a single session, e.g., `softconf.com/acl2014/WMT14`.

Workshops are fairly easy to format since everything is linear and
typically abstracts are not printed. This can be done fairly
automatically by generating the schedule from the order file, even if
the workshop chairs are derelict in the their duties.

The main conference is another matter. The papers that are presented
are contained in separate subconferences, whose separate schedules must be
assembled and interleaved to produce the consolidated main conference schedule.

# Notes for Publications Chairs

The downside of being the handbook chair is that there is all sorts of
upstream events you have no power to enforce (except through friendly
pub chairs) but that have a large impact on how difficult your job
is. It will be helpful to read this section and pass this information
on to the publications chairs, in the case where you are not them. In
general, it is most helpful if the publications chairs are also
responsible for the handbook (and this is what NAACL has done in 2013
and 2015), but if you are the "handbook chair" and are not also the
pub chair, you should be in touch with them early and often to
minimize the amount of hand-correction you'll have to do.

The single-most important thing you can do is to ensure that the
"order" files are properly formatted, for the workshops, but most
importantly, for all parts of the main conference proceedings.

The "order" file is a human- and machine-readable file that is part of
the ACLPUB package (which Softconf's START system helps you
assemble). It is used to generate the schedule in the proceedings,
where computer-readability isn't very important, but it is also used
to generate the schedules in the handbook, where computer-readability
is very important, since the schedules from many different workshops
and pieces of the main conference (papers, shortpapers, SRW, demos,
tutorials, and, since 2013, TACL) are assembled.

Publications chairs should ensure the following:

- If at all possible, convince the PC chairs **not** to use START's
  "ScheduleMaker" tool. This is a complicated Excel front-end setup
  that generates the "order" file, which is already fairly simple to
  edit. They should just edit the order file directly. It is much
  simpler. 

- The order files should be machine readable. Workshop chairs
  are sometimes tempted to play with the formatting lines in
  order to get a custom look, but this introduces a host of problems
  generating the handbook.
  
  To help ensure compliance, a script has been provided:
  
     cat papers/order | ./scripts/verify_schedule.py

- The main conference schedule --- the one containing all sorts of
  non paper-related events like "Lunch" and "Coffee Break" and
  "Keynote address" --- should be placed in the "papers"
  subconference, which represents the main conference proceedings. The
  other order files should contain _only_ events relevant to those
  workshops. For example, do not repeat coffee breaks and lunches
  in the "shortpapers"; "shortpapers" should contain only lines
  listing days, session titles, and the papers that are presented in
  those sessions. This is to aid in merging the schedules for these
  subconferences into a single unified schedule: the code in
  `scripts/` will group papers in identically-named sessions across
  files. While events like lunches could also be merged, it is better
  to just list them in one place so that changes to one file (e.g.,
  you decide to rename "Coffee Break" to "Tea time" for this year's
  meeting in Cambridge) do not require changes to be made all over the
  place. 

- Parallel sessions should be named using the convention "Session NL: NAME", where
  N is a session number (1..as many as necessary), L is a letter (A..number of parallel tracks),
  and NAME is the session name. Session names should be globally distinct. For example,

       = Session 6D: Machine Translation II

  This aids immensely in generating the handbook and also the poster placards that sit
  outside the rooms and provide a summary of all papers in each track. 
  
- If papers are mixed across workshops (e.g., SRW papers mixed into a
  regular session), the session headers should be identical across the
  order files. e.g., in `papers/order`, you could have
  
       = Session 1D: Syntax, Parsing, and Tagging I 
       247 11:00--11:25 # Tagging The Web: Building A Robust Web Tagger with Neural Network   

  and in `srw/order`, you would put
  
       = Session 1D: Syntax, Parsing, and Tagging I
       6 10:10--10:35 # A Tabular Method for Dynamic Oracles in Transition-Based Parsing
       5 10:35--11:00 # Joint Incremental Disfluency Detection and Dependency Parsin
       12 11:25--11:50 # A Crossing-Sensitive Third-Order Factorization for Dependency Parsing

  The identical session name allows them to be merged and formatted
  automatically when you generate the handbook.
  
- TACL papers are a recent addition to *ACL conferences. Since TACL
  papers are published elsewhere, and are therefore not included with
  the conference proceedings, there is no ACLPUB package for them, and
  you must come up with an alternative. NAACL 2013 and ACL 2014, a fake
  subconference was created and the TACL papers were imported as if it
  TACL were a workshop. In NAACL 2015, we instead do the following:
  
   - Add the TACL papers to the file `input/tacl_papers.yaml`. This is
   a [YAML-formatted](http://yaml.org) document that is processed by
   the file `scripts/tacl_builder.py` to pull out the abstracts and
   paper metadata so they can be seamlessly integrated into the
   conference handbook.
   
   - Run the script:
   
        $ python2.7 ./scripts/tacl_builder.py
        Reading from file input/tacl_papers.yaml
        Write bibtex entries to auto/tacl/papers.bib
        Writing abstract auto/abstracts/tacl-485.tex
        ...

     This will generate the papers bibliography and the abstracts,
     which can then be treated like any paper.
     
   - In the main schedule (`data/papers/order`), you can now reference
     TACL papers using the format `XXX/TACL`, e.g.,
     
        498/TACL 11:05--11:30 # TACL-498: Extracting Lexically Divergent Paraphrases from Twitter %by Wei Xu, Alan Ritter, Chris Callison-Burch, William B. Dolan, and Yangfeng Ji

     The scripts that process this file will know how to transform
     this into a TACL paper reference, so long as it has been built
     from the TACL YAML file.

# The order file

The script `scripts/verify_schedule.py` provides some minimal
sanity-checking on the order file. Here is more detail on how to
produce it and how to handle some common limitations.

The order file permits four types of lines

- Comments
- Papers. Papers are either presented in oral sessions or in poster
  sessions. They are denoted by a number, which is tied to the paper
  submission ID, and is used to locate the paper and the paper's
  metadata in `proceedings/final/NUM/NUM_metadata.txt`. Papers
  presented as part of oral sessions have time ranges, while papers
  presented as posters do not.
- '+' events, which are single events that have a time range but that
  are not associated with a paper. For example, lunch.
- Session headers, denoted by lines starting with '=', which are used
  to group together papers presented in a parallel track.

Here is an example schedule (from `data/papers/proceedings/order`):

    + 7:30--18:00 Registration
    + 7:30--9:00 Breakfast
    + 9:00--10:00 Invited talk II: Zoran Popovic
    + 10:00--10:30 Coffee break
    = Session 4A: Machine Learning for NLP
    321 10:30--10:55 # Kneser-Ney Smoothing on Expected Counts
    605 10:55--11:20 # Robust Entity Clustering via Phylogenetic Inference
    377 11:20--11:45 # Linguistic Structured Sparsity in Text Categorization
    510 11:45--12:10 # Perplexity on Reduced Corpora

If you want to mix papers between sessions, make sure the session
titles are the same. Here are snippets from
`data/papers/order` 

    = Session 1D: Syntax, Parsing, and Tagging I
    247 11:00--11:25 # Tagging The Web: Building A Robust Web Tagger with Neural Network

As mentioned above, we can also refer to TACL papers using something
like the following (where the IDs correspond to those listed in `input/tacl_papers.yaml`):

    = Session 1D: Syntax, Parsing, and Tagging I
    6/TACL 10:10--10:35 # A Tabular Method for Dynamic Oracles in Transition-Based Parsing
    5/TACL 10:35--11:00 # Joint Incremental Disfluency Detection and Dependency Parsin

These will be assembled automatically. Here's how to do a poster
session:

    + 18:50--21:30 Poster and Dinner Session I: TACL Papers, Long Papers, Short Papers, Student Research Workshop; Demonstrations
    249  # Interpretable Semantic Vectors from a Joint Model of Brain- and Text- Based Meaning
    416  # Single-Agent vs. Multi-Agent Techniques for Concurrent Reinforcement Learning of Negotiation Dialogue Policies
    161  # A Linear-Time Bottom-Up Discourse Parser with Constraints and Post-Editing
    178  # Negation Focus Identification with Contextual Discourse Information
    ...  

## Missing features

In START, the code used to verify the order file is not suited to the
handbook. Their verification ensures only that each paper in the final
version of the proceedings is listed exactly once. This prevents a
number of common situations that people require.

1. Listing a paper more than once in the schedule.

   Some people want this, say, when a paper is provided with both an
   oral presentation and is also present in a poster session. This
   can't be done, however, in the current ACLPUB packages, which
   assert a bijection between accepted paper IDs and papers listed in
   the schedule (the schedule is used to determine the paper's order
   in the proceedings, and this helps ensure that no paper is
   forgotten or has an ambiguous place). In EMNLP 2014, working with
   the SoftConf folks,
   [Yuval Marton](http://www1.ccls.columbia.edu/~ymarton/) arranged
   for a new notation, !, which is used to denote events that are a
   little more complicated than typical things like breaks, lunches,
   and so on, which use the '+' designator. You can use this to list a
   paper more than once and get it past START's verifications, e.g.,
   
      ! 11:05--11:30 Extracting Lexically Divergent Paraphrases from Twitter %by Wei Xu, Alan Ritter, Chris Callison-Burch, William B. Dolan, and Yangfeng Ji
   
   The '!' notation also permits keywords, some of which are parsed by the
   conference handbook code to create special formatting and to
   automatically add people to the index. e.g.,

      ! 09:00--10:10 Invited Talk: "A Quest for Visual Intelligence in Computers" %by Fei-fei Li

2. Publishing a paper in the proceedings but not listing it in the
schedule.

   START won't allow this, but you can just comment out the paper in
   the schedule for the handbook and all will be well.
   
3. Listing a paper in the schedule that is not present in the
proceedings. 

   Sometimes there are papers not in the proceedings, but in the
   schedule, and you want the formatting to look the same. To
   accomplish this, you have to manually create new numbered entries
   for those papers in a separate proceedings tarball. Create new
   numbered entries and then the corresponding metadata in 
   
       SUBCONF/final/NUM/NUM_metadata.txt
     
   The handbook code will then find what it needs, and all shall be
   well, and all manner of thing shall be well.

# Layout

Now we get to assembling the handbook.

ACL 2014 had five parallel sessions. This should be useful for any handbook 
where parallel sessions are listed one per page with abstracts.

Directories:

- `input/`: fixed inputs
   - `input/conferences.txt`: list of conferences (used for auto-download)

- `data/`: where the ACLPUB tarballs are downloaded and unpacked to

- `scripts/`: scripts used to generate the handbook sections from the ACLPUB
  proceedings.

- `content/`: handbook tex files used to build the handbook

- `auto/`: the output of scripts, used to generate first-pass LaTeX
  that is then pulled manually into the handbook content.

# Task list

- Download all the main conference proceedings and workshops using
  `scripts/download-proceedings.sh` (after editing
  `input/conferences.txt`). This creates a proceedings tarball in each
  of `data/SUBCONF/proceedings`.

- Verify each of them with `scripts/verify_schedule.py`:

        for file in $(ls data); do 
          num=$(cat data/$file/proceedings/order | ./scripts/verify_schedule.py > /dev/null 2>&1; echo $?) 
          if test $num -ne 0; then 
            echo -e "$file\t$num"
          fi
        done

- Generate the bibtex metadata from each workshop's paper metadata:

        for dir in $(ls data); do 
          [[ ! -d "auto/$dir" ]] && mkdir auto/$dir
          ./scripts/meta2bibtex.py data/$dir/proceedings/final $dir
        done
    
  This creates abstracts in `auto/abstracts` (read in via LaTeX calls
  to `\paperabstract`) and BibTeX metadata used for the index and
  other things (in `auto/SUBCONF/papers.bib`)

- Generate the workshop schedules:

       for dir in $(ls data); do 
         [[ ! -d "auto/$dir" ]] && mkdir auto/$dir
         cat data/$dir/proceedings/order | ./scripts/order2schedule_workshop.pl $dir > auto/$dir/schedule.tex
       done
    
  This leaves you with a ton of `schedule.tex` files which can be
  `\input`ed via LaTeX
  
- Edit `content/workshops/overview.tex` and
  `content/workshops/workshops.tex` to include these files and to be correct.

- Create the workshops bibtex entries in
  `content/workshops/papers.bib`. This is included in the main
  `handbook.tex` so that you can cite the workshop chairs and title automatically.

- Next, fill in the tutorials manually, editing
  `content/tutorials/tutorials-001.tex` and so on. Also edit the tutorial
  overview page in `content/tutorials/tutorials-overview.tex`.

- Generate the paper and poster session files (which you'll have to edit a bit afterwards):

       for name in tacl demos papers srw; do
           cat data/$name/order | ./scripts/order2schedule.perl $name
       done

- Generate the daily overviews, munge them a bit, pull them in

        cat data/{papers,shortpapers,demos,tacl,srw}/order | ./scripts/order2schedule_overview.py

- Email Dragomir Radev, who will run your index against
  [the ACL Anthology Network](http://clair.eecs.umich.edu/aan/index.php),
  correcting spellings and collapsing redundancies.


# Miscellaneous notes

- Take care to ensure the index is correct. Email Drago Radev who can
  help you consolidate names against the ACL Anthology.

- Mausam will cause you trouble. Grep for him. You want just the name,
  no {}s
  
- Also special characters in abstracts (e.g., a real alpha, funny
  latex, chinese, etc). Really this should all be converted over to XeTeX.

# Suggestions for the future

The ACL proceedings and handbook play complementary roles. In one
sense, the proceedings are the main product of a conference; their
life is a long one, stretching into the future, serving up papers from
the Anthology for years to come. However, if that were the only
purpose of a conference, it would be a journal. The handbook is what
allows people to quickly and easily navigate the physical space of the
conference. Its utility may be rooted in a particular time and place,
but it is equally a product of the conference and plays an important
if ephemeral role in bringing people together.

Perhaps in part because of this rooting in a physical space, the task
of generating the handbook in past years has fallen under the purview
of the local arrangements chair. This is a mistake. The job is much
better suited to the publications chair. This is true conceptually,
but also because many of the tasks of handbook generation (in
particular, ensuring machine-readable format of the order files) are
redundant with work already undergone by the publications chairs, since
a version of the schedule is also published in the proceedings.

# Credits

This document was written by Matt Post during assembly of the NAACL
2013 and ACL 2014 handbooks. I inherited from Ulrich Germann the code
and data he used to assemble the 2012 NAACL handbook. I don't know
about any history prior to that.
