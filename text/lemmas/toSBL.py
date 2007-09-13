# -*- coding: utf-8 -*-
import sys
from morphgnt import convert

for line in sys.stdin.readlines():
    line = line.decode('utf-8').strip().replace("#2", "$").split("#")[0].strip().replace("$", "#2")
    arr = line.split(u" : ")
    lemma_arr = arr[1].split(u" ! ")
    lemma_arr_utf8 = [convert.beta2sbl(x) for x in lemma_arr]

    print (u"%s %s" % (arr[0], lemma_arr_utf8[0])).encode('utf-8')
