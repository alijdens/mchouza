# The Computer Language Benchmarks Game
# http://shootout.alioth.debian.org/
#
# modified by Ian Osgood
# modified again by Heinrich Acker
# modified by Justin Peel
# modified by Mariano Chouza

import sys, bisect

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

def genRandom(ia = 3877, ic = 29573, im = IM):
    seed = 42
    lut = [(s * ia + ic) % im for s in xrange(IM)]
    while 1:
        seed = lut[seed]
        yield seed

Random = genRandom()

def makeCumulative(table):
    P = []
    C = []
    prob = 0.
    for char, p in table:
        prob += p
        P += [prob]
        C += [char]
    return (P, C)

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
    width = 60
    r = xrange(width)
    gR = Random.next
    jn = ''.join
    lut = makeLookupTable(table)
    lines = [jn([lut[gR()] for i in r]) for j in xrange(n // width)]
    if n % width:
        lines.append(jn([lut[gR()] for i in xrange(n % width)]))
    print '\n'.join(lines)

def main():
    n = int(sys.argv[1])

    print '>ONE Homo sapiens alu'
    repeatFasta(alu, n*2)

    print '>TWO IUB ambiguity codes'
    randomFasta(iub, n*3)

    print '>THREE Homo sapiens frequency'
    randomFasta(homosapiens, n*5)
main()
