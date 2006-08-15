import sys
for line in sys.stdin.readlines():
    arr1 = line.strip().split(" ! ")
    arr2 = arr1[0].split()
    lemma1 = arr2[-1]
    lemma2 = arr1[1]
    if lemma1 != lemma2:
        print "UP100: %s %s %s ... %s %s %s" % (arr2[0], arr2[1], arr2[2], arr2[4], lemma1, lemma2)
