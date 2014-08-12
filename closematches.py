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

PICKLE_FILE = 'operators2.p'

operators = pkle.load(open(PICKLE_FILE, 'rb'))

print(operators[:10])

#need to lowercase the list
operators_lowercase = []
for opr in operators:
    if opr != None:
        operators_lowercase.append(opr.lower())
    
print(operators_lowercase[:20])

opr_count = collections.Counter(operators_lowercase)

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