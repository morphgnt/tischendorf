            Tischendorf's 8th edition Greek New Testament
                       with morphological tags
                             Version 2.7

              Based on G. Clint Yale's Tischendorf text
                   and on Dr. Maurice A. Robinson's
                   Public Domain Westcott-Hort text

		  Edited by Ulrik Sandborg-Petersen

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


Kethiv/Qere
===========

As of version 2.0 of the text, there is an extra field in the
database, namely the "qere" for each word.  In Hebrew Masoretic texts,
there is a distinction between the "Kethiv" (that which is written)
and the "Qere" (that which should be read).  This distinction is
present in versions 2.0 and above of this database.  The Kethiv is
that which is written in the printed Tischendorf.  The Qere is what
the editor thinks it should have been.

Most often, this amounts to differences in accentuation or diacritics.
In a few cases, it amounts to a change in the word itself (e.g.,
Revelation 14:18, where the printed text reads TOI\S BO/TRUAS, where
this editor thinks it should have been TOU\S BO/TRUAS, on account of
the grammar).

For the vast majority of words, the Qere is identical to the Kethiv.

The parsing always follows the Qere, not the Kethiv.


Feedback
========

The editor welcomes feedback and suggestions for improvement.  He can
be reached via electronic mail:

ulrikp<write-the-sign>emdros.org


Website
=======

This text has a website:

http://morphgnt.org/projects/tischendorf



Ulrik Sandborg-Petersen
Aalborg, April 2010




------------------ end of introduction ------------------



Tagging scheme
==============

The tagging scheme is exactly the same as that used by Dr. Robinson in
all of his texts.  It is described in the accompanying file, called
"parsing.txt".


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
- Space-separated fields (except for the last two)
- - fields:
  0. Book (corresponds to the filename, which is the Online Bible standard)
  1. Chapter:Verse.word-within-verse
  2. Pagraph break ("P") / Chapter break ("C") / No break (".") (see
     below)
  3. The text as it is written in the printed Tischendorf (Kethiv)
  4. The text as the editor thinks it should have been (Qere)
  5. The morphological tag (following the Qere)
  6. The Strong's number (following the Qere)
  7. The lemma in two versions:
    7.a The first version, which corresponds to The NEW Strong's
      Complete Dictionary of Bible Words.
    7.b Followed by the string " ! "
    7.c Then the second version, which corresponds to Friberg, Friberg
      and Miller's ANLEX.
    There may be several words in each lemma.

All Strong's numbers are single numbers with 1,2,3, or 4 digits.

The text exists in two versions: One in the "BETA" directory and one
in the "Unicode" directory. The only difference is the encoding: The
former is in TLG BETA encoding, whereas the latter is in Unicode NFC
UTF-8.

The third column (designated "2." above) has precisely one of three
values:

- "." : No break occurs
- "P" : A paragraph break occurs
- "C" : A chapter break occurs

Most paragraph breaks occur on a verse boundary, but not all paragraph
breaks do.

A program counting the "C"s can rely on them to count the chapters,
i.e., even if a chapter break occurs in a verse which belongs to
chapter X, that means that Tischendorf thought that that verse belongs
to chapter X+1.  This occurs, for example, in Revelation 12:18, where
the chapter break occurs in chapter 12, meaning that verse 12:18 needs
to be shown with chapter 13.


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

v. 1.3 (2006-01-03)
   - Fixed 16 parsing-errors, 2 to do with case and 14 to do with
     A)/RA being misparsed as non-interrogative.
   - Changed structure such that BETA and Unicode versions are in
     separate directories, and the file extension is always .txt.

v. 1.4 (2006-03-14)
   - Fixed 151 words, some of which were parsing-errors (particularly
     with respect to 2nd Aorist analyses of stems with *LQ*), and some
     of which were wrongly assigned lemmas and/or Strong's numbers.

v. 1.5 (2007-01-09)
   - Fixed 350 words, most of which were parsing errors, but some of
     which were lemmatization errors.

v. 2.0 (2008-01-20)
   - Fixed Strong's number of H(MEI=S, H(MA=S, H(MI=N, and H(MW=N.
     All of them should be 2249, but were 2248.
   - Added kethiv/qere.
   - Various changes to the text itself.
   - 448 changes in total.

v. 2.5 (2009-01-01)
   - Added an extra column with paragraph breaks and chapter breaks.
   - Changed the punctuation to be more in accordance with the printed
     Tischendorf.
   - Got rid of some [square brackets] which were not in Tischendorf.
   - Fixed a few typos in the text itself, thereby making the text
     conform more to the printed Tischendorf.
   - Proof-read the "preicope adulterae" (John 7:53-8:11).
   - Updated the analysis and lemma assignment for a number of words.

v 2.6 (2010-??-??)
   - Added paragraph- and chapter-breaks for the books of Titus, 1
     John, 2 John, and 3 John (they were missing in 2.5)
   - Updated BETA version to have paragraph- and chapter-breaks (they
     were missing from the BETA encoded version entirely in 2.5)
   - Updated tags of possessive pronouns (e.g., E)MO/S, SO/S,
     H(ME/TEROS, U(ME/TEROS) to provide the number of the possessor as
     well as the number of the possessed.
   - Forms of KREI/TTWN now have a -C (comparative) suffix.
   - Various other fixes to the text and the analyses.

v 2.7 (2011-09-26)
   - Update to latest Westcott-Hort base analysis from 2011-03-15, but
     differing from this in the analysis of *SO/DOMA in three places
     (to harmonize it as neuter plural, not feminine singular).
   - This led to changes to the anlaysis for some 133 words.
   - Luke 19:1 is now a chapter boundary (it was a paragraph boundary
     in Version 2.6).

