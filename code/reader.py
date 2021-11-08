from book import Book
from strongsmapping import StrongsMapping
from form_tag_lemma_dict import FormTagLemmaDict
from lexicon import Lexicon
from kind import *
from word import *

read_wh_only = 0
read_wh_and_na27 = 1
read_na27_only = 2
read_tischendorf = 3
read_stephens = 4
read_AccentedTischendorf = 5

def read_WH(read_what):
    if read_what == read_na27_only:
        return False
    else:
        return True

def read_NA27(read_what):
    if read_what == read_wh_only:
        return False
    else:
        return True

def read_StrongsLemmas():
    mapping = StrongsMapping()
    mapping.read("../text/lemmas/lemmatable.txt")
    return mapping

def read_ANLEXLemmas():
    mapping = StrongsMapping()
    mapping.read("../text/lemmas/lemmatable_ANLEX.txt")
    return mapping


book_list_OLB = ["MT", "MR", "LU", "JOH", "AC", "RO", "1CO", "2CO",
                 "GA", "EPH", "PHP", "COL", "1TH", "2TH", "1TI", "2TI",
                 "TIT", "PHM", "HEB", "JAS", "1PE", "2PE", "1JO", "2JO", "3JO",
                 "JUDE", "RE"]

book_list_UBS = ["mat", "mrk", "luk", "jhn", "act", "rom", "1co", "2co",
                 "gal", "eph", "php", "col", "1th", "2th", "1ti", "2ti",
                 "tit", "phm", "heb", "jas", "1pe", "2pe", "1jn", "2jn", "3jn",
                 "jud", "rev"]

class Reader:
    def __init__(self, dir, suffix):
        self.current_monad = 1
        self.suffix = suffix
        self.dir = dir
        self.books = []
        self.lexicon = None

    def read_NT(self, read_what):
        for bkname in book_list_OLB:
            self.read_book(bkname, read_what)

    def read_MT(self, read_what):
        self.read_book("MT", read_what)

    def write_SFM(self):
        cur_monad = 1
        for index in range(0,27):
            gdb_bookname = book_list_UBS[index]
            cur_monad = self.writeBookAsSFM(gdb_bookname + ".TIS", self.books[index], cur_monad)

    def writeBookAsSFM(self, filename, book, cur_monad):
        f = open(filename, "w")
        cur_monad = book.writeSFM(f, cur_monad)
        f.close()
        return cur_monad

    def write_TUP(self):
        for index in range(0,27):
            olb_bookname = book_list_OLB[index]
            cur_monad = self.write_book_MORPH_style(index, olb_bookname, "./", "TUP", kUnicode)

    def write_StrippedLinear(self):
        cur_monad = 1
        for index in range(0,27):
            olb_bookname = book_list_OLB[index]
            self.books[index].write_StrippedLinear(olb_bookname + ".SLN")

    def write_WHLinear(self):
        cur_monad = 1
        f = open("WH-BETA.txt", "w")
        for index in range(0,27):
            self.books[index].write_WHLinear(f)
        f.close()

    def parse_sentences_and_clauses(self):
        for index in range(0,27):
            self.books[index].parse_sentences()
            self.books[index].parse_clauses()

    def write_Linear(self):
        cur_monad = 1
        for index in range(0,27):
            olb_bookname = book_list_OLB[index]
            self.books[index].write_Linear(olb_bookname + ".SLN")

    def write_MQL(self, mqlfilename, bUseOldStyle):
        fout = open(mqlfilename, "w")
        for index in range(0,27):
            self.books[index].writeMQL(fout, bUseOldStyle)
        fout.close()


    def write_OSIS(self, osisfilename):
        fout = open(osisfilename, "w")
        fout.write("""<?xml version='1.0' encoding='utf-8' ?>
<osis xmlns="http://www.bibletechnologies.net/2003/OSIS/namespace"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:schemaLocation="http://www.bibletechnologies.net/osisCore.2.1.1.xsd">
<osisText osisIDWork="GK.TischNT" osisRefWork="NA" xml:lang="gk">
<header>
<work osisWork="GK.TischNT">
    <title>Tischendorf's 8th Greek New Testament</title>
    <date event="original" type="Gregorian">1868</date>
    <date event="eversion" type="Gregorian">2019</date>
    <type type="x-bible">Bible</type>
    <language type="ISO-639-2">GK</language>
    <rights>Public Domain. Copy freely.</rights>
</work>
</header>
<div type="bookGroup">
<title>Tischendorf's 8th Greek New Testament</title>
""")

        for index in range(0,27):
            self.books[index].writeOSIS(fout)

        fout.write("""</div></osisText></osis>""")
        fout.close()

    def write_JSON(self, osisfilename):
        fout = open(osisfilename, "w")
        fout.write("""{"version": "TISCH", "versionName": "Tischendorf", "meta": {"description": "Tischendorf's 8th Greek New Testament", "source": "https://github.com/morphgnt/tischendorf", "encoding": null, "language": "gk", "license": "Public Domain. Copy freely", "copyright": null}, "books":{""")

        for index in range(0,27):
            self.books[index].writeJSON(fout)

        fout.write("""} }""")
        fout.close()


    def applyLemma(self, lemmaType):
        if lemmaType == kStrongs:
            mapping = read_StrongsLemmas()
        else:
            mapping = read_ANLEXLemmas()
        for index in range(0,len(self.books)):
            self.books[index].applyLemma(mapping, lemmaType)
        
    def applyMappingStrongs(self):
        self.applyLemma(kStrongs)

    def applyMappingANLEX(self):
        self.applyLemma(kANLEX)

    def applyMappings(self):
        self.applyMappingStrongs()
        self.applyMappingANLEX()

    def applyANLEXLemmaDictionary(self, form_tag_lemma_filename):
        ftl_dict = FormTagLemmaDict(form_tag_lemma_filename)
        self.applyFormTagLemmaDict(ftl_dict)

    def applyFormTagLemmaDict(self, ftl_dict):
        for index in range(0,len(self.books)):
            self.books[index].applyFormTagLemmaDict(ftl_dict)

    def read_book(self, bookname, read_what):
        if self.suffix == "":
            print bookname
            filename = self.dir + "/" + bookname
        else:
            print bookname + "." + self.suffix
            filename = self.dir + "/" + bookname + "." + self.suffix
        book = Book(filename)
        self.books.append(book)
        self.current_monad = book.read(self.current_monad, read_what) + 1

    def writeBooks_MORPH_style(self, output_dir, output_suffix, encodingStyle):
        for index in range(0,27):
            olb_bookname = book_list_OLB[index]
            self.write_book_MORPH_style(index, olb_bookname, output_dir, output_suffix, encodingStyle)

    def writeSubset_MORPH_style(self, filename, word_predicate, manualanalyses, encodingStyle):
        f = open(filename, "w")
        for index in range(0,27):
            olb_bookname = book_list_OLB[index]
            self.write_subset_MORPH_style(f, index, word_predicate, manualanalyses, encodingStyle)
        f.close()

    def write_book_MORPH_style(self, index, bookname, output_dir, output_suffix, encodingStyle):
        if index < len(self.books):
            if output_suffix == "":
                print bookname
                filename = output_dir + "/" + bookname
            else:
                print bookname + "." + output_suffix
                filename = output_dir + "/" + bookname + "." + output_suffix
            book = self.books[index]
            book.write_MORPH_style(filename, encodingStyle)
        
    def write_subset_MORPH_style(self, f, index, word_predicate, manualanalyses, encodingStyle):
        book = self.books[index]
        book.write_subset_MORPH_style(f, word_predicate, manualanalyses, encodingStyle)

    def compareTischendorf(self, tischrd, lexicon, manualanalyses):
        mapping = read_StrongsLemmas()
        self.produceLexicon(lexicon)
        tischrd.addVersesToVerseDicts()
        for index in range(0, len(self.books)):
            whbook = self.books[index]
            tischbook = tischrd.getBook(index)
            whbook.compareTischendorf(tischbook, self.lexicon, manualanalyses)
            #tischbook.applyLemma(mapping)

    def produceLexicon(self, lexicon):
        self.lexicon = lexicon
        for index in range(0, len(self.books)):
            whbook = self.books[index]
            whbook.addToLexicon(self.lexicon)
        return self.lexicon

    def getBook(self, index):
        return self.books[index]

    def addVersesToVerseDicts(self):
        for index in range(0, len(self.books)):
            whbook = self.books[index]
            whbook.addVersesToVerseDict()

