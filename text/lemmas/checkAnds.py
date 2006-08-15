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

            lemma = arr[1].strip()
            try:
                lemma2 = self.strongs2lemma[strongs]
                print "UP101: lemma already exists for strong's %s: original = '%s', new = '%s'." % (strongs, lemma2, lemma)
            except:
                self.strongs2lemma[strongs] = lemma

        f.close()

        keys = self.strongs2lemma.keys()
        keys.sort()
        for strongs in keys:
            lemma = self.strongs2lemma[strongs]
            if "&" in strongs:
                strongs_single = strongs.split("&")[0]
                try:
                    lemma_single = self.strongs2lemma[strongs_single]
                    if lemma_single != lemma:
                        print "UP100: lemma '%s' for %s != %s for : %s" % (lemma, strongs, lemma_single, strongs_single)
                except:
                    print "UP102: strong's single %s does not exist, but strong's %s does, with lemma %s" % (strongs_single, strongs, lemma)
                    self.strongs2lemma[strongs_single] = lemma

s1 = StrongsMapping()
s1.read("lemmatable_ANLEX.txt")
