from book import Book
from strongsmapping import StrongsMapping
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

    def read_MT(self):
        self.read_book("MT",0)

    def read_MT(self, read_what):
        self.read_book("MT",read_what)

    def read_MT_Tisch(self):
        self.read_book("mt",read_tischendorf)

    def read_MT_NA27(self):
        self.read_book("MT",1)

    def read_GA(self):
        self.read_book("GA",0)

    def read_NT(self, read_what):
        for bkname in book_list_OLB:
            if read_what == read_tischendorf:
                self.read_book(bkname.lower(), read_what)
            else:
                self.read_book(bkname, read_what)
            

    def read_NT_write_SFM(self):
        mapping = StrongsMapping()
        mapping.read("./lemmatable.txt")
        cur_monad = 1
        for index in range(0,27):
            olb_bookname = book_list_OLB[index]
            self.read_book(olb_bookname, read_wh_only)
            self.books[-1].applyLemma(mapping, kStrongs)
            gdb_bookname = book_list_UBS[index]
            cur_monad = self.writeSFM(gdb_bookname + ".TD2", self.books[-1], cur_monad)

    def write_SFM(self):
        cur_monad = 1
        for index in range(0,27):
            gdb_bookname = book_list_UBS[index]
            cur_monad = self.writeSFM(gdb_bookname + ".TD2", self.books[index], cur_monad)

    def write_TUP(self):
        for index in range(0,27):
            olb_bookname = book_list_OLB[index]
            cur_monad = self.write_book_MORPH_style(index, olb_bookname, "./", "TUP", kUnicode)


    def read_NT_AccentedTischendorf_write_SFM(self):
        mapping = StrongsMapping()
        mapping.read("./lemmatable.txt")
        cur_monad = 1
        for index in range(0,27):
            olb_bookname = book_list_OLB[index]
            self.read_book(olb_bookname, read_AccentedTischendorf)
            self.books[-1].applyLemma(mapping, kStrongs)
            gdb_bookname = book_list_UBS[index]
            cur_monad = self.writeSFM(gdb_bookname + ".TD2", self.books[-1], cur_monad)

    def read_NT_AccentedTischendorf_write_stripped_linear(self):
        cur_monad = 1
        for index in range(0,27):
            olb_bookname = book_list_OLB[index]
            self.read_book(olb_bookname, read_AccentedTischendorf)
            self.books[-1].write_StrippedLinear(olb_bookname + ".SLN")

    def read_NT_AccentedTischendorf_write_linear(self):
        cur_monad = 1
        for index in range(0,27):
            olb_bookname = book_list_OLB[index]
            self.read_book(olb_bookname, read_AccentedTischendorf)
            self.books[-1].write_Linear(olb_bookname + ".SLN")

    def read_NT_AccentedTischendorf(self):
        cur_monad = 1
        for index in range(0,27):
            olb_bookname = book_list_OLB[index]
            self.read_book(olb_bookname, read_AccentedTischendorf)

    def read_NT_write_MQL(self, mqlfilename, read_what, bUseOldStyle):
        mapping = StrongsMapping()
        mapping.read("./lemmatable.txt")
        fout = open(mqlfilename, "w")
        cur_monad = 1
        for index in range(0,27):
            olb_bookname = book_list_OLB[index]
            self.read_book(olb_bookname, read_what)
            self.books[index].applyLemma(mapping, kStrongs)
            gdb_bookname = book_list_UBS[index]
            self.books[index].writeMQL(fout, bUseOldStyle)
        fout.close()

        

    def applyLemma(self, lemmaType):
        mapping = StrongsMapping()
        if lemmaType == kStrongs:
            mapping.read("./lemmatable.txt")
        else:
            mapping.read("./lemmatable_ANLEX.txt")
        for index in range(0,27):
            self.books[index].applyLemma(mapping, lemmaType)
        

    def read_NA27_ApplyMapping(self):
        mapping = StrongsMapping()
        mapping.read("./lemmatable.txt")
        cur_monad = 1
        for index in range(0,27):
            olb_bookname = book_list_OLB[index]
            self.read_book(olb_bookname, read_na27_only)
            self.books[-1].applyLemma(mapping, kANLEX)

    def read_NA27_ApplyMapping_MT(self):
        mapping = StrongsMapping()
        mapping.read("./lemmatable.txt")
        cur_monad = 1
        for index in range(0,1):
            olb_bookname = book_list_OLB[index]
            self.read_book(olb_bookname, read_na27_only)
            self.books[-1].applyLemma(mapping, kANLEX)

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

    def applyMappingStrongs(self):
        strongsmapping = StrongsMapping()
        strongsmapping.read("./lemmatable.txt")
        for index in range(0,len(self.books)):
            self.books[index].applyLemma(strongsmapping, kStrongs)

    def applyMappingANLEX(self):
        ANLEXmapping = StrongsMapping()
        ANLEXmapping.read("./lemmatable_ANLEX.txt")
        for index in range(0,len(self.books)):
            self.books[index].applyLemma(ANLEXmapping, kANLEX)

    def applyMappings(self):
        self.applyMappingStrongs()
        self.applyMappingANLEX()

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

    def write_MQL(self, filename, bUseOldStyle):
        f = open(filename, "w")
        for b in self.books:
            b.writeMQL(f, bUseOldStyle)
        f.close()

    def writeSFM(self, filename, book, cur_monad):
        f = open(filename, "w")
        cur_monad = book.writeSFM(f, cur_monad)
        f.close()
        return cur_monad

    def compareTischendorf(self, tischrd, lexicon, manualanalyses):
        mapping = StrongsMapping()
        mapping.read("./lemmatable.txt")
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

