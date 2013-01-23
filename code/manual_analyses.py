class ManualAnalyses:
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
        mybook = myarr[0]
        mychapterverse = myarr[1]
        myref = "%s %s" % (mybook, mychapterverse)
        mysurface = myarr[2]
        mytag = myarr[3]
        mystrongs = myarr[4]
        if len(myarr) > 5:
            myanlex_lemma = " ".join(myarr[5:])
            mytuple = tuple((mysurface, mytag, mystrongs, myanlex_lemma))
        else:
            mytuple = tuple((mysurface, mytag, mystrongs))

        try:
            self.mydict[myref]
            raise Exception("Error: myref already exists for line:\n%s\n" % line)
        except KeyError:
            self.mydict[myref] = mytuple

    def getTuple(self, ref):
        try:
            return self.mydict[ref]
        except KeyError:
            return None
