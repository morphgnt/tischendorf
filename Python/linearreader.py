from book import Book
from strongsmapping import StrongsMapping
from lexicon import Lexicon
from reader import *

class LinearReader(Reader):
    def __init__(self, dir, suffix):
        Reader.__init__(self,dir,suffix)

    def read_book(self, bookname, read_what=None):
        if self.suffix == "":
            print bookname
            filename = self.dir + "/" + bookname
        else:
            print bookname + "." + self.suffix
            filename = self.dir + "/" + bookname + "." + self.suffix
        book = Book(filename)
        self.books.append(book)
        self.current_monad = book.read_linear(self.current_monad) + 1

