class Chapter:
    def __init__(self, first_monad, last_monad, chapter, bookname):
        self.first_monad = first_monad
        self.last_monad = last_monad
        self.chapter = chapter
        self.bookname = bookname

    def writeMQL(self, f, bUseOldStyle):
        print >>f, "CREATE OBJECT"
        print >>f, "FROM MONADS={" + str(self.first_monad) + "-" + str(self.last_monad) + "}"
        if bUseOldStyle:
            OT = "Chapter"
        else:
            OT = ""
        print >>f, "[%s" % OT
        print >>f, "  book:=" + self.bookname + ";"
        print >>f, "  chapter:=" + str(self.chapter) + ";"
        print >>f, "]" 
        if bUseOldStyle:
            print >>f, "GO"
        print >>f, ""

