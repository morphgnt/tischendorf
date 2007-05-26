import sys
from morphgnt import convert

for line in sys.stdin.readlines():
    line = line.decode('utf-8').strip()
    arr = line.split(u" : ")
    lemma_arr = arr[1].split(u" ! ")
    lemma_arr_utf8 = [convert.beta2unicode(x) for x in lemma_arr]
    print (u"%s : %s" % (arr[0], u" ! ".join(lemma_arr_utf8))).encode('utf-8')
