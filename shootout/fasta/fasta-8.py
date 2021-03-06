# The Computer Language Benchmarks Game
# http://shootout.alioth.debian.org/
#
# modified by Ian Osgood
# modified again by Heinrich Acker
# modified by Justin Peel
# modified by Mariano Chouza

import sys, bisect, array

alu = (
   'GGCCGGGCGCGGTGGCTCACGCCTGTAATCCCAGCACTTTGG'
   'GAGGCCGAGGCGGGCGGATCACCTGAGGTCAGGAGTTCGAGA'
   'CCAGCCTGGCCAACATGGTGAAACCCCGTCTCTACTAAAAAT'
   'ACAAAAATTAGCCGGGCGTGGTGGCGCGCGCCTGTAATCCCA'
   'GCTACTCGGGAGGCTGAGGCAGGAGAATCGCTTGAACCCGGG'
   'AGGCGGAGGTTGCAGTGAGCCGAGATCGCGCCACTGCACTCC'
   'AGCCTGGGCGACAGAGCGAGACTCCGTCTCAAAAA')

iub = zip('acgtBDHKMNRSVWY', [0.27, 0.12, 0.12, 0.27] + [0.02]*11)

homosapiens = [
    ('a', 0.3029549426680),
    ('c', 0.1979883004921),
    ('g', 0.1975473066391),
    ('t', 0.3015094502008),
]

IM = 139968
INITIAL_STATE = 42

def makeCumulative(table):
    P = []
    C = []
    prob = 0.
    for char, p in table:
        prob += p
        P += [prob]
        C += [char]
    return (P, C)

randomSeq = None
j = 0
def makeRandomSeq():
    global randomSeq
    ia = 3877; ic = 29573
    randomSeq = []
    s = INITIAL_STATE
    while True:
        s = (s * ia + ic) % IM
        randomSeq.append(s)
        if s == INITIAL_STATE:
            break

def makeLookupTable(table):
    bb = bisect.bisect
    probs, chars = makeCumulative(table)
    imf = float(IM)
    return [chars[bb(probs, i / imf)] for i in xrange(IM)]

def repeatFasta(src, n):
    width = 60
    r = len(src)
    s = src + src + src[:n % r]
    for j in xrange(n // width):
        i = j*width % r
        print s[i:i+width]
    if n % width:
        print s[-(n % width):]

def randomFasta(table, n):
    global randomSeq, j
    width = 60
    
    lut = makeLookupTable(table)
    luStr = ''.join(lut[randomSeq[j]] for j in xrange(IM))
    luStr += luStr[:width]

    lj = j
    sow = sys.stdout.write
    for i in xrange(n // width):
        sow(luStr[lj:lj+width] + '\n')
        lj = (lj + width) % IM
    j = lj
    if n % width:
        k = (j + (n % width)) % IM
        sow((luStr[j:k] if j < k else luStr[j:] + luStr[:k]) + '\n')
        j = k

def main():
    n = int(sys.argv[1])

    makeRandomSeq()

    print '>ONE Homo sapiens alu'
    repeatFasta(alu, n*2)

    print '>TWO IUB ambiguity codes'
    randomFasta(iub, n*3)

    print '>THREE Homo sapiens frequency'
    randomFasta(homosapiens, n*5)
    
main()
