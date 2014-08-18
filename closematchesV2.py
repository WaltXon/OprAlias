# -*- coding: utf-8 -*-
"""
Created on Tue Aug 12 13:12:38 2014

@author: wnixon
"""

import cPickle as pkle
import difflib
import Levenshtein as lev
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import collections
import string
import pprint

PICKLE_FILE = 'operators2.p'
RATIO_CUTOFF = 87

operators = pkle.load(open(PICKLE_FILE, 'rb'))

operators_deque = collections.deque(operators[:100])

operator_test  = operators[:2000]
#need to normalize for counts but aslo need to keep
#the original so that I can match back to it later?

#maybe I can clean up a list and then do fuzzy mathcing
#when adding the alias back to the gdb file? 
#

def normalize(s):
    for p in string.punctuation:
        s = s.replace(p, '')
    return s.lower().strip()

operators_normal = []
for opr in operator_test:
    if opr != None:
        normalized = normalize(opr)
        trunc = normalized.split(' ')
        if len(trunc) >= 3:
            take3 = ' '.join(trunc[0:3])
        else:
            take3 = normalized
            
        operators_normal.append(take3)
    
#print(operators_normal[:20])

opr_count = collections.Counter(operators_normal)

for opr, count in opr_count.most_common(10):
    print('{0} {1}'.format(opr, count))
    



opr_set = set(operators_normal)
opr_sort_set = sorted(opr_set)

#pp = pprint.PrettyPrinter()
#pp.pprint(opr_sort_set)



similar = []
groups = []
similar_tup = None

for name in opr_sort_set:
    for name2 in opr_sort_set:
        if fuzz.ratio(name, name2) >= RATIO_CUTOFF and name != name2:
            similar.append(name2)
            similar_tup = tuple(similar)
    groups.append(similar_tup)
    similar = []
    similar_tup = None

opr_group_set = set(groups)

pp = pprint.PrettyPrinter()
pp.pprint(opr_group_set)
    
    

#using difflib
#difflib.get_close_matches(operator, operators)
#difflib.SequenceMather().ratio() --Not reallly 

#using Levenshtein
#lev.ratio(string1, string2)

##using Fuzzywuzzy
#fuzz.partial_ratio(s1, s2) 
#fuzz.ratio()
#>>> choices = ["Atlanta Falcons", "New York Jets", "New York Giants", "Dallas Cowboys"]
#>>> process.extract("new york jets", choices, limit=2)
#    [('New York Jets', 100), ('New York Giants', 78)]
#>>> process.extractOne("cowboys", choices)
#    ("Dallas Cowboys", 90)