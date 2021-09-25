
THIS FILE IS WRITTEN BY HENRIK BRUUS 08.02.2016


This directory contains a template (in the form of an example) for writing
a thesis in LaTeX. The important files are the tex-files. LaTeX generates
the typography automatically you 'just' have to provide the text.

If you use the template you are guarantied to fulfil the technical
requirements for writing a thesis at DTU Physics, i.e., you will produce
a thesis in the LaTeX book-style for two-sided printing with

1) a proper title page
2) the required abstract (in English), resume (in Danish), and preface
3) the required table of contents
4) the required lists of figures, tables, and symbols
5) the proper format for chapters
6) the proper format for appendices
7) an optional index
and
8) the proper format for the bibliography


MyThesis.tex
============
This file is the main file controling your document. This is the file that
you compile with LaTeX. It basically sets the overall book style and includes 
the various components of your thesis. In the example the input files are
  chap00.tex, chap01.tex, chap02.tex, chapA.tex, chapB.tex and bib.tex
plus the file with your own LaTeX-macros
  texdef.tex
All parts called by a \include command will be included. This allows you
to write each chapter in a separate file. This enhances your structural
overview. But there is more to it: a very nice feature is the \includeonly
command. If a certain chapter has reached a level where you do not want to
improve it further for a while, you exclude it from the \includeonly command.
It will then not be LaTeX'ed, but you can still cite the equations, tables,
and figures in that chapter and get the proper references correct in your
current chapter. Normally you will only have one file at a time in the
\includeonly command.

texdef.tex
==========
This files contains macros for LaTeX commands and sequences of
LaTeX commands that you use frequently in your thesis. Note in
particular the section marked "Labels" concerning references to
equations, figures, tables etc, and the section marked "SI units"
for formatting SI units inside various math environments, say "\SIm"
produces a roman "m" for meter. The pair "\bsubal" and "\esubal"
produces an aligned sets of equations with frozen numric numbering
and a running alphabetic numbering, such as (14a), (14b), and (14c).
Finally, note how the begin-equation-macro "\beq" requires an argument,
namely the label for the equation. This forces you to label all
equations (good practice).

chap00.tex
=========
This file contains the front page, the abstract, the Danish resume, the
preface, the table of contents, and the lists of figures, tables and
symbols.
  Please, go through chap00.tex line by line and see where you asked to
provide text and information.
  Note that whereas the table of contents and the lists of figures and
tables are generated automatically, you will have to write the list of
symbols yourself between the \begin{tabular} and the \end{tabular}.


chapXX.tex
==========
These are the files containing the actual text of your thesis. These files
all begin with the \chapter command, since each are thought of as a chapter.
Also appendices are written as normal chapters. Whether a chapter appears as
a regular chapter or an appendix is determined by whether it is included
before or after the \appendix command in the main file MyThesis.tex. Note the
two special chapters "chapY_index" and chapZ_bib", which produces an optional
index with keywords (marked throughout the main text by the command "\index")
and the required bibliography using the bibtex-method.

Bibliography
============
The bibliography is created by use of bibtex and a source text file xxx.bib
with the specific style controlled by the yyy.bst file, here in the form of 
"acoustolfluidics.bib" and "TMF_reports.bst". The entries are usually gotten directly 
from the journal websites through bibtex-output (a few lines of text commands),
typically @Article, @Book, or @Misc. Each reference are called by a \cite-command
containing the key "AuthorYear", such as "Bruus2008" (first author's last name 
followed by publication year). For multiple publications the same year, letters
"a", "b" etc is added to subsequent entries, such as "Muller2012", "Muller2012a",
"Muller2012c". Before added a reference, make sure to check that it is not already
present in the bib-file. The bib-file can be manipulated directly in your favorite
text editor or through the free-ware interface JabRef. 

xxxxx.aux
=========
These auxillary files contains the information for cross referencing
within your theses. DO NOT EVER ERASE ANY OF THESE FILES.

*.toc, *.lof, and *.lot
=======================
These files are generated automatically to provide the input for
the various lists of contents, figures and tables. DO NOT ERASE THEM.


List of figures and tables
==========================
These lists are important for readers of your thesis. They are generated
automatically. You just have to provide a short text for the lists. This
is done by enhancing the normal \caption command from
  \caption{A very long a thorough text}
to
  \caption[A short text]{A very long a thorough text}
This will put 'A short text' in the list while maintaining
the 'A very long a thorough text' below the figure/table.

Appendices
==========
Appendices are written as normal chapters. See under chapXX.tex for details.

The directory structure
=======================
All latex-files are kept in the main directory (here ThesisDefault). These
are *.tex, *.aux, *.toc, *.lof, *.lot, and *.log (a log-file for error analysis).
  All figures used directly in the thesis are put away in the
ThesisDefault/figs/chapXX directories. That is all the final
figures for chapXX is found in ThesisDefault/figs/chapXX. Usually
these figures are generated from sub-figures. The sub-figures
(which are normally output from MatLab/Mathematica, LaTeX or
CoralDraw) are put in ThesisDefault/figs/chapXX/makefig. The idea
is that from the files in makefig you should be able to recreate
the final figures in ThesisDefault/figs/chapXX. PLEASE RESPECT
THIS STRUCTURE - I have seen many cases of wasted time due to
disorder in the figure files.

Figures
=======
All figures are placed in ThesisDefault/figs/chapXX as discribed under
the directory structure. 
  It is good practice always to combine sub-figures into one final figure
containing everything. Put sub-figures under ThesisDefault/figs/chapXX/makefig
and the final figures under ThesisDefault/figs/chapXX.
  In ThesisDefault/figs/chapXX/makefig you will find some *.tex files. these
are used to compile many sub-figures into one eps-figure (with labels like
(a), (b) and (c)) using LaTeX. If you use LaTeX through WinEdt then use the
dvi->ps bottom and write "-E -o ZZZZ.eps" in the generic-parameters field
that pops up. Here "-E" is a flag yielding an eps-file as output, while
"-o ZZZZ.eps" is a flag for control of the name of the resulting file (here
obviously "ZZZZ.eps").
  Often you will need to convert jpg, gif, and other graphics files to the
eps format. I prefer to use the free-ware "Gimp" for that operation. You can
download it from "http://www.gimp.org/" for free.

If you have comments or questions, please contact me at bruus@fysik.dtu.dk

THE END
