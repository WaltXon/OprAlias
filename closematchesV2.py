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
RATIO_CUTOFF = 90

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
    



opr_set = set(operators_normal)
opr_sort_set = sorted(opr_set)

#pp = pprint.PrettyPrinter()
#pp.pprint(opr_sort_set)

i= 'INIT'
alias_dict = {}
alias_dict['DEFAULT'] = 0
#for opr_name in opr_sort_set:
#    #print('* {0}'.format(opr_name))
#    if i == 'INIT':
#        #ON THE FIRST ITERATION SETUP VARIABLES
#        prev_name = opr_name
#        opr_most_common = 'DEFAULT'
#        opr_similar = []
#        
#    if fuzz.ratio(prev_name, opr_name) >= RATIO_CUTOFF:   
#        #IF THE PREV_NAME AND OPR_NAME ARE SIMILAR AND SHOULD BE GROUPED
#        opr_similar.append(prev_name)
#        
#        if opr_count[opr_name] > opr_count[opr_most_common]:
#            #IF THE CURRENT OPR_NAME HAS MORE COUNTS THAN THE OPR_MOST_COMMON                
#            #OPR_MOST_COMMON SOULD IS SET TO CURRENT VALUE OF OPR_NAME                 
#            opr_most_common = opr_name
#            
#        prev_name = opr_name
#    else:
#        opr_most_common = prev_name
#        alias_dict.setdefault(opr_most_common, opr_similar)
#        opr_most_common = 'DEFAULT'
#        opr_similar = []

similar = []
groups = {}


for name in opr_sort_set:
    for name2 in opr_sort_set:
        if fuzz.ratio(name, name2) >= RATIO_CUTOFF and name != name2:
            similar.append((name2, fuzz.ratio(name, name2)))
    groups.setdefault(name, similar)
    similar = []
        
        
alias_dict.pop('DEFAULT')
pp = pprint.PrettyPrinter()
pp.pprint(groups)
    
    

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