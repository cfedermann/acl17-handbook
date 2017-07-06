# $@ the target
# $* the matched prefix
# $< the matched dependent

# -recorder records the files opened in a file with a .fls extension. This is used to infer
# the list of file dependencies.

latex = pdflatex

all: handbook.pdf

# In many cases, you can just run latex once to get your updates in
handbook.pdf: handbook.tex handbook.ind
	${latex} handbook
	${latex} handbook

# Build the handbook, then fix the index, run biber, and rebuild
handbook.ind: handbook.dep handbook.idx
	${latex} handbook
	cat handbook.idx | perl scripts/fix-index.perl > handbook.idx.fixed
	makeindex handbook.idx.fixed -o handbook.ind
	biber handbook
	${latex} handbook

# Run latex in recorder mode to see all the files opened, use that to build a .dep file
# which is -include'd at the end of this file. Now you have a dependency on all tex files
# for the top-level PDF. This step has no dependency, so if you need to retrigger it, you
# have to delete it manually.
handbook.dep:
	${latex} -recorder handbook
	grep "INPUT.*tex$$" handbook.fls | sort | uniq | perl -pe "s/INPUT /handbook.pdf:/" > handbook.dep

.PHONY: clean handbook.tex

EXTENSIONS  = .ilg .ps .dvi .dep .idx .idx.fixed .ind .aux .idx.ilg .bbl .blg .bcf .toc .fls .log -blx.bib .run.xml .out

clean: 
	rm -f $(addprefix handbook, ${EXTENSIONS})

-include handbook.dep

.SECONDARY:
