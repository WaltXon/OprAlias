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

PICKLE_FILE = 'operators2.p'

operators = pkle.load(open(PICKLE_FILE, 'rb'))

print(operators[:10])

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
for opr in operators:
    if opr != None:
    
        operators_normal.append(normalize(opr))
    
print(operators_normal[:20])

opr_count = collections.Counter(operators_normal)

for opr, count in opr_count.most_common(10):
    print('{0} {1}'.format(opr, count))
    



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