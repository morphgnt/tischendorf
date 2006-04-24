import sys

def getfirst(t):
    return t[0]

class StrongsMapping:
    def __init__(self):
        self.strongs2lemma = {}
        self.lemma2strongs = {}
        self.strongs2lemma_single = {}
        self.strongs2lemma_additions = {}

    def writeTXT(self, f):
        keys = self.strongs2lemma.keys()
        keys.sort()
        for strongs in keys:
            print >>f, "%s : %s" % (strongs, str(self.strongs2lemma[strongs]))

    def read(self, filename):
        f = open(filename, "r")
        for line in f.readlines():
            arr = line.split(" : ")
            strongs = arr[0]

            if "&" in strongs:
                strongs_single = strongs.split("&")[0]
                #lemma = arr[1].replace("\n", "").split("!")[0].strip()
                lemma = arr[1].strip()
                try:
                    lemma2 = self.strongs2lemma[strongs_single]
                    if lemma2 != lemma:
                        print "UP100: strongs_single = %s lemma2 = %s lemma = %s" % (strongs_single,lemma2,lemma)
                except:
                    self.strongs2lemma[strongs_single] = lemma

        f.close()

s1 = StrongsMapping()
s1.read("lemmatable_ANLEX.txt")
