class FormTagLemmaDict:
    def __init__(self, filename):
        self.mydict = {}
        self.read(filename)

    def read(self, filename):
        f = open(filename, "r")
        for line in f.readlines():
            self.parseLine(line)
        f.close()

    def parseLine(self, line):
        line = line.replace("\r", "").replace("\n", "")
        myarr = line.split(" ")
        myform = myarr[0]
        mytag = myarr[1]
        myanlex_lemma = " ".join(myarr[2:])

        self.mydict.setdefault(myform, {})
        self.mydict[myform].setdefault(mytag, myanlex_lemma)


    def getLemma(self, form, tag):
        try:
            return self.mydict[form][tag]
        except KeyError:
            return None
