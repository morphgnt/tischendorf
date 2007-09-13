# -*- coding: utf-8 -*-
import sys
from morphgnt import convert
import unicodedata

for line in sys.stdin.readlines():
    line = line.decode('utf-8').strip().replace("#2", "$").split("#")[0].strip().replace("$", "#2")
    arr = line.split(u" : ")
    lemma_arr = arr[1].split(u" ! ")
    lemma_arr_utf8 = [convert.beta2unicode(x) for x in lemma_arr]

    s = u"%s : %s" % (arr[0], " ! ".join(lemma_arr_utf8))
    print ("%s" % unicodedata.normalize('NFC', s)).encode('utf-8')
