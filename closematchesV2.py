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
RATIO_CUTOFF = 70

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
    
        operators_normal.append(normalize(opr))
    
#print(operators_normal[:20])

opr_count = collections.Counter(operators_normal)

for opr, count in opr_count.most_common(10):
    print('{0} {1}'.format(opr, count))
    


i=0
alias_dict = {}

opr_set = set(operators_normal)

for opr_name in opr_set:
    #print('* {0}'.format(opr_name))
    opr_most_common = ''
    opr_similar = []    
    if i == 0:
        prev_name = opr_name
        opr_most_common = opr_name
        i += 1
        continue
    else:
        #print('--PREV = {0}, OPR = {1}, FUZZ RATIO = {2}'.format(prev_name, opr_name, fuzz.ratio(opr_name, prev_name)))
        if fuzz.ratio(opr_name, prev_name) >= RATIO_CUTOFF:        
            if opr_count[opr_name] > opr_count[opr_most_common]:
                print('---OPR_CT = {0}, MOST_COMMON = {1}'.format(opr_count[opr_name], opr_count[opr_most_common]))
                opr_similar.append(prev_name)                    
                opr_most_common = opr_name
                
            else:
                opr_similar.append(prev_name)
        else:
            alias_dict.setdefault(opr_most_common, opr_similar)  
        
        #print('--! prev_name = {0}, opr_name = {1}, most_common = {2}, opr_similar = {3}'.format(prev_name, opr_name, opr_most_common, opr_similar))
    prev_name = opr_name
        
        
print(alias_dict)
    
    

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