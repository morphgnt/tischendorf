from word import Word
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
            else:
                strongs_single = strongs
            lemma = arr[1].replace("['", "").replace("']", "").replace("\\\\", "\\").replace("\n", "")
            self.strongs2lemma[strongs] = lemma
            self.strongs2lemma_single[strongs_single] = lemma
            self.lemma2strongs[lemma] = strongs
        f.close()
        self.strongs2lemma_keys = self.strongs2lemma.keys()

    def getLemmaFromStrongs(self, strongs):
        try:
            lemma = self.strongs2lemma[strongs]
            return lemma
        except KeyError:
            if "&" in strongs:
                strongs_single = strongs.split("&")[0]
            else:
                strongs_single = strongs
            try:
                lemma = self.strongs2lemma_single[strongs_single]
                self.strongs2lemma_additions[strongs] = lemma
            except KeyError:
                lemma = ""
                print "UP256: strongs missing: %s" % strongs_single
            return lemma

    def getSingleNumberDictionary(self):
        other = {}
        other_lemma2strongs = {}
        for strongs in self.strongs2lemma.keys():
            # Get lemma
            lemma = self.strongs2lemma[strongs]

            # Get single strong's
            if "&" in strongs:
                strongs_single = int(strongs.split("&")[0])
            else:
                strongs_single = int(strongs)

            # Create empty list if not there
            try:
                other[strongs_single]
            except KeyError:
                other[strongs_single] = []

            if lemma in other[strongs_single]:
                pass
            else:
                other[strongs_single].append(lemma)

            try:
                other_lemma2strongs[lemma]
            except KeyError:
                other_lemma2strongs[lemma] = []

            if strongs_single in other_lemma2strongs[lemma]:
                pass
            else:
                other_lemma2strongs[lemma].append(strongs_single)

        other_keys = other.keys()
        other_keys.sort()

        for k in other_keys:
            print "%d : %s" % (k,other[k])

        lemma2strongs_keys = other_lemma2strongs.keys()
        lemma2strongs_keys.sort()

        for k in lemma2strongs_keys:
            if len(other_lemma2strongs[k]) > 1:
                print "%d : %s : %s : UP262" % (int(other_lemma2strongs[k][0]), str(other_lemma2strongs[k]), k)

        #for i in range(1,5624):
        #    try:
        #        self.strongs2lemma[str(i)]
        #    except:
        #        print "UP260: Missing Strong's: %d" %i
