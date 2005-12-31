import sys
import string
import re

REHasAsper = re.compile(r'([AEHIOUW]\()|(\*\([/\\=]?[AEHIOUW])')

dict = {}

def getStrongs(strongs):
    if "&" in strongs:
        strongsarr = strongs.split("&")
        return "%05d" % int(strongsarr[0])
    else:
        return "%05d" % int(strongs)

letterdict = {
    "a" : "a",
    "b" : "b",
    "g" : "g",
    "d" : "d",
    "e" : "e",
    "z" : "z",
    "h" : "e",
    "q" : "th",
    "i" : "i",
    "k" : "k",
    "l" : "l",
    "m" : "m",
    "n" : "n",
    "c" : "x",
    "o" : "o",
    "p" : "p",
    "r" : "r",
    "s" : "s",
    "t" : "t",
    "u" : "u",
    "f" : "ph",
    "x" : "ch",
    "y" : "ps",
    "w" : "o",
    "|" : "i",
    " " : " ",
    "-" : "-",
    "j" : "rh"
    }

def transformLemma(lemma):
    hasAsper = not re.search(REHasAsper,lemma) is None
    hasStar = "*" in lemma
    lowercaselemma = string.lower(lemma)
    strippedlemma = lowercaselemma.replace("r(","j").replace("(", "").replace(")", "").replace("/", "").replace("\\", "").replace("=", "").replace("+", "").replace("*", "").replace("[1","").replace("]1","")
    lettertransformedlemma = ""
    for l in strippedlemma:
        try:
            replacement = letterdict[l]
            lettertransformedlemma = lettertransformedlemma + replacement
        except:
            print "UP102: in lemma '%s', letter '%s' unknown." % (lemma, l)

    # Take care of spiritus asper
    if hasAsper:
        lemmapenultimate = "h" + lettertransformedlemma
    else:
        lemmapenultimate = lettertransformedlemma

    # Take care of capital letter
    if hasStar:
        lemmaultimate = string.upper(lemmapenultimate[0]) + lemmapenultimate[1:]
    else:
        lemmaultimate = lemmapenultimate
    return lemmaultimate

for line in sys.stdin.readlines():
    line = line.replace("\n", "")
    arr = line.split()
    strongs = getStrongs(arr[0])
    lemma = " ".join(arr[2:])
    transformedlemma = transformLemma(lemma)
    try:
        alreadythere = dict[strongs]
        if alreadythere != transformedlemma:
            print "UP100: line '%s' already there: %s" % (line, alreadythere)
    except:
        dict[strongs] = transformedlemma

keys = dict.keys()
keys.sort()
for k in keys:
    print "%s %s" % (k, dict[k])
                     
