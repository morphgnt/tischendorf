            Tischendorf's 8th edition Greek New Testament
                       with morphological tags
                             Version 1.2

              Based on G. Clint Yale's Tischendorf text
                   and on Dr. Maurice A. Robinson's
                   Public Domain Westcott-Hort text

                       Edited by Ulrik Petersen

                    This text and its analysis are
                  in the Public Domain. Copy freely.


Introduction
============

The present work is Tischendorf's 8th edition of the Greek New
Testament, augmented with morphological tags, Strong's numbers, and
lemmas.

Even though I am designated as the editor, the bulk of the work in the
preparation of this text was done by two other men, namely G. Clint
Yale and Maurice A. Robinson.  Thus they deserve most of the credit
for the existence of this work.  Clint Yale provided the base
Tischendorf text, while Dr. Robinson provided a fully parsed and
lemmatized Westcott-Hort text (with some errors that were mutually
corrected in the preparation of this edition).  I heartily thank them
both.


Preparation of the text
=======================

Clint Yale has published two Tischendorf texts.  The first was
published in the Public Domain on the Internet in 1997, and only
contained the text -- without diacritics, punctuation, or apparatus.
Mr. Yale's second Tischendorf text was published later, and contained
both diacritics, punctuation, and Tischendorf's apparatus.

The basis of the present work was originally Mr. Yale's Public Domain
1997 Tischendorf text, since most of the analysis was carried out
using that text.  However, during the last stages of preparation of
the text, Mr. Yale very graciously permitted me to distribute, in the
Public Domain, an accentuated version based on his later Tischendorf,
for which I am very grateful.  The Greek NT community owes him a debt
of gratitude for this generosity.

The text has been corrected (though not thoroughly checked) against a
facsimile copy of Tischendorf.  The text thus mostly conforms with the
printed Tischendorf.  Even in cases of clear typographical errors, the
text has been retained as it was printed.  As Mr. Yale notes in the
introduction to his later Tischendorf edition, the printed version was
"typographically challenged".  Having dealt with the text in detail, I
can only confirm Mr. Yale's judgment on this account.


Preparation of the analysis
===========================

Westcott-Hort and Tischendorf's 8th edition share a large percentage
of common text.  Therefore, the decision was made to base the
morphological analysis and lemmatization on Dr. Robinson's Public
Domain Westcott-Hort text.

A computer program was written to port over as much as possible of
Dr. Robinson's Westcott-Hort analysis, with manual analyses being
added where necessary.  Only about 10740 words could not be ported
over directly.  Of these, only about 900 words needed manual analyses,
while about another 300 word-forms were merely differences in
spelling.  An analytical lexicon totalling about 290 word-forms was
developed for those forms which were peculiar to Tischendorf, or which
needed other special attention.  For the rest, an analytical lexicon
was constructed automatically from the Westcott-Hort text, which was
then utilized in giving parses and Strong's numbers to forms which had
a unique analysis in that lexicon.

After the analysis was complete, numerous consistency-checks were made
on the analysis.  Grammatical relations such as agreement were checked
using the linguistic search engine "Emdros", with subsequent manual
checking and correction of the cases where agreement had been broken
by the process of porting the tags over from the Westcott-Hort text.
After this, all instances of ambiguity in either the lemma or the
parsing of a word were checked, numbering about 1030.  In checking
these instances, linguistic searches were again run in cases that were
not attributable to genuine morphological ambiguity. If it turned out
that there was a mistake, it was corrected, and the search was run
again to ensure that the error was gone.  After that, searches were
run on all individual parts of speech (except verbs and nouns),
listing all unique forms, their Strong's number, and their lemma.  The
surface forms were compared to the lemmas, and irregularities were
weeded out.

Whenever a word-form was found which seemed not to be correct Greek,
it was checked against the facsimile, and corrected if necessary.

Finally, all neuter nouns which were present either as nominative or
accusative, but not both, were carefully checked to ensure that the
correct case had been assigned.


Assignment of lemmas
====================

Two lemmas are provided: One conforms to Strong's dictionary, while
the other mostly conforms to Friberg, Friberg, and Miller's ANLEX.
ANLEX represents more than a century's worth of additional scholarship
compared to Strong's dictionary.  This and other factors entail that
ANLEX has, in some respects, a more fine-grained lemma-division than
Strong's.  

Now, the lemmas were added automatically, based solely on the assigned
Strong's number.  Therefore, in a few cases, a distinction which ANLEX
makes is lost, since it was not made by Strong.  One such example is
H)=XOS which in ANLEX is two lemmas, one being masculine and the other
being neuter.  In Strong's dictionary, there is only one lemma, hence
only one number, and hence, since the lemmas are based on the Strong's
number, the distinction is lost.

The process was carried out with constant reference to a number of
grammars and lexica, including BDAG, Thayer, Strong's, Abbott-Smith,
Perschbacher, Liddell-Scott, and last, but not least, Friberg, Friberg
and Miller's ANLEX.  Blass-Debrunner-Rehkopf and Blass-Debrunner-Funk
were consulted on occasion, as were a number of introductory grammars.

During the process described above, the editor had much pleasant
interaction both with Professor Robinson and with Mr. Yale, resulting
in mutual correction of our respective databases.  All remaining
errors are, of course, my own responsibility.


Feedback
========

The editor welcomes feedback and suggestions for improvement.  He can
be reached via electronic mail:

ulrikp<write-the-sign>emdros.org


Website
=======

This text has a website:

http://ulrikp.org/Tischendorf



Ulrik Petersen
Aalborg, December 2005



------------------ end of introduction ------------------



Tagging scheme
==============

The tagging scheme is exactly the same as that used by Dr. Robinson in
all of his texts.  See the following Internet URL for more
information:

http://www.byztxt.com


Lemmas
======

There are two lemmas for each word:

1) The first lemma mostly conforms to that which is found in "The NEW
   Strong's Complete Dictionary of Bible Words" by James Strong,
   LL.D., S.T.D., Thomas Nelson Publishers, 1996.

2) The second lemma mostly conforms to that which is found in
   "Analytical Lexicon of the Greek New Testament" by Friberg, Friberg
   and Miller.


Format
======

The format is as follows:

- One word per line
- Space-separated fields
- Up to ten fields (at least eight):
  - Book (corresponds to the filename, which is the Online Bible standard)
  - Chapter:Verse.word-within-verse
  - The text
  - The morphological tag
  - The Strong's number
  - The lemma in two versions:
    - The first version, which corresponds to The NEW Strong's
      Complete Dictionary of Bible Words.
    - Followed by an "exclamation mark" ("!")
    - Then the second version, which corresponds to Friberg, Friberg
      and Miller's ANLEX.
    There may be several words in each lemma.

All Strong's numbers are single numbers with 1,2,3, or 4 digits.

The text exists in two versions: One with a ".TSP" extension for each
file, and one with a ".TUP" extension for each file. The former is in
TLG BETA encoding, whereas the latter is in Unicode UTF-8.


ChangeLog
=========

v. 1.0 (2005-12-13): Initial release.

v. 1.1 (2005-12-19):
   - Proofed the text against a facsimile, and made around 830 changes.
   - Changed a few parsings and lemmas.

v. 1.2 (2005-12-27):
   - Proofed the text against a facsimile, and made around 230 changes.
   - Changed a few parsings.
   - Rearranged diacritics such that they appear before a capital
     letter, not after it.
   - Fixed some Unicode-conversion errors.


