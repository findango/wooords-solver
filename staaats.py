#!/usr/bin/env python
# encoding: utf-8
"""
Calculate which words are most common in a 9-letter Wooords game.
"""

import sys
from collections import defaultdict

ANAGRAMS = defaultdict(list)

def load_dictionary(fname):
    f = open(fname)
    for word in f.readlines():
        word = word.rstrip("\n")
        key = "".join(sorted(word))
        ANAGRAMS[key].append(word)
    f.close()

def find_words(letters):
    BITMASKS = [0x1, 0x2, 0x4, 0x8, 0x10, 0x20, 0x40, 0x80, 0x100]
    bits = range(9)
    all_combos = range(512) # 2^9
    words = []
    for combo in all_combos:
        subset = ""
        for i in bits:
            if combo & BITMASKS[i]:
                subset += letters[i]
        if len(subset) > 3 and subset in ANAGRAMS:
            # don't need to normalize subset because we preserved the order of letters
            words.append(subset)
    return clean(words)

def clean(words):
    words = list(set(words)) # de-dupe
    return words

def main():
    load_dictionary("./dictionary.txt")
    bingos = filter(lambda w: len(w) == 9, ANAGRAMS.keys())

    word_counts = defaultdict(int)
    for letters in bingos:
        for word in find_words(letters):
            key = "".join(sorted(word))
            word_counts[key] += 1

    top = sorted(word_counts, key=word_counts.get, reverse=True)[:100]

    rk = 1
    for w in top:
        print str(rk) + ".",
        print ", ".join(sorted(ANAGRAMS["".join(sorted(w))])),
        print "(" + str(word_counts[w]) + " words)"
        rk += 1

if __name__ == '__main__':
    main()
