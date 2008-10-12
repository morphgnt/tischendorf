import sys

for line in sys.stdin.readlines():
    arr = line.strip().split()
    print "%s %s" % (" ".join(arr[0:3]), " ".join(arr[4:]))
