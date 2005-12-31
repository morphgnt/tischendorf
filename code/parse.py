class GNTParse:
    def __init__(self, starting_monad, bIsParsed, bHasVariants):
        self.starting_monad = starting_monad
        self.monad = starting_monad
        self.bIsParsed = bIsParsed
        self.bHasVariants = bHasVariants
        self.words = []
        self.verses = []

    def parseBook(self, filename, bookname):
        self.bookname = bookname
        self.f = open(filename)
        self.readLines(self.f)
        self.f.close()
        del self.f

    def readLines(self):
        for line in self.f:
            self.parseLine(line)

    def parseLine(self, line):
        words = line.split()
        for w in words:
            print "'%s'" % w
        
        
        
