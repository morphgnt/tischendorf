import sys
from book import Book
from verse import Verse
from word import Word
from variant import *
from kind import *

tisch_book_list_OLB = ["mt", "mr", "lu", "joh", "ac", "ro", "1co", "2co",
                 "ga", "eph", "php", "col", "1th", "2th", "1ti", "2ti",
                 "tit", "phm", "heb", "jas", "1pe", "2pe", "1jo", "2jo", "3jo",
                 "jude", "re"]

book_list_OLB = ["MT", "MR", "LU", "JOH", "AC", "RO", "1CO", "2CO",
                 "GA", "EPH", "PHP", "COL", "1TH", "2TH", "1TI", "2TI",
                 "TIT", "PHM", "HEB", "JAS", "1PE", "2PE", "1JO", "2JO", "3JO",
                 "JUDE", "RE"]


impnames = { "Matthew" : "MT",
             "Mark" : "MR",
             "Luke" : "LU",
             "John" : "JOH",
             "Acts" : "AC",
             "Romans" : "RO",
             "I Corinthians" : "1CO",
             "II Corinthians" : "2CO",
             "Galatians" : "GA",
             "Ephesians" : "EPH",
             "Philippians" : "PHP",
             "Colossians" : "COL",
             "I Thessalonians" : "1TH",
             "II Thessalonians" : "2TH",
             "I Timothy" : "1TI",
             "II Timothy" : "2TI",
             "Titus" : "TIT",
             "Philemon" : "PHM",
             "Hebrews" : "HEB",
             "James" : "JAS",
             "I Peter" : "1PE",
             "II Peter" : "2PE",
             "I John" : "1JO",
             "II John" : "2JO",
             "III John" : "3JO",
             "Jude" : "JUDE",
             "Revelation of John" : "RE"
             }



class TischReader:
    def __init__(self):
        self.current_monad = 1
        self.books = []
        self.curBook = ""
        self.verse = None


    def read_BETA_file(self, fname):
        f = open(fname, "r")
        for line in f.readlines():
            self.parseLine(line)

        f.close()

    def parseLine(self, line):
        line = line.replace("\r", "").replace("\n", "")
        if line[0:3] == "$$$":
            self.parseDollarLine(line)
        else:
            self.parseVerseTextLine(line)

    def parseDollarLine(self, line):
        myline = line[3:]
        mylist = myline.split(":")
        myindex = mylist[0].rfind(" ")
        mybook = mylist[0][0:myindex]
        mychapter = mylist[0][myindex+1:]
        myverse = mylist[1]
        #print "'%s' chapter '%s' verse '%s'" % (mybook,mychapter,myverse)
        bookname = impnames[mybook]
        if self.curBook != mybook:
            self.curBook = mybook
            newbook = Book("./" + bookname + ".TBA")
            print "UP2: newbook.bookname = %s, newbook.booknumber = %d" % (newbook.bookname, newbook.booknumber)
            self.books.append(newbook)
        book = self.books[-1]
        self.verse = Verse([], book.bookname, book.booknumber)
        self.verse.chapter = int(mychapter)
        self.verse.verse = int(myverse)

    def parseVerseTextLine(self, line):
        # Must also add it to current book
        if line == "":
            pass
        else:
            words = line.split(" ")
            words_list = []
            for w in words:
                w2 = Word(0,variant_none)
                w2.surface = w
                words_list.append(w2)
            self.verse.words = words_list
            self.books[-1].verses.append(self.verse)

    def writeAsMORPH(self, output_dir, output_suffix, encodingStyle):
        for index in range(0,27):
            olb_bookname = book_list_OLB[index]
            self.write_book_MORPH_style(index, olb_bookname, output_dir, output_suffix, encodingStyle)

    def addVersesToVerseDicts(self):
        for index in range(0, len(self.books)):
            whbook = self.books[index]
            whbook.addVersesToVerseDict()

    def write_book_MORPH_style(self, index, bookname, output_dir, output_suffix, encodingStyle):
        if output_suffix == "":
            print bookname
            filename = output_dir + "/" + bookname
        else:
            print bookname + "." + output_suffix
            filename = output_dir + "/" + bookname + "." + output_suffix
        book = self.books[index]
        book.write_MORPH_style(filename, encodingStyle)
        
    
        
        



ddd = 0
txt = 1
begin = 2

curbook = ""
curchapverse = ""
state = begin


