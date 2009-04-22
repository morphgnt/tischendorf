# -*- coding: utf-8 -*-
import sys

for line in sys.stdin.readlines():
    line = line.decode('utf-8').strip().replace("#2", "$").split("#")[0].strip().replace("$", "#2")
    arr = line.split(u" : ")
    lemma_arr = arr[1].split(u" ! ")
    lemma_arr_beta = [x for x in lemma_arr]

    s = u"%s : %s" % (arr[0], lemma_arr_beta[0])
    print s.encode('utf-8')
