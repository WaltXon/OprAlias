# -*- coding: utf-8 -*-
"""
Created on Tue Aug 12 13:12:38 2014

@author: wnixon
"""

#import cPickle as pkle
#import difflib
#import Levenshtein as lev
from fuzzywuzzy import fuzz
#from fuzzywuzzy import process
import collections
import string
#import pprint

#need to normalize for counts but aslo need to keep
#the original so that I can match back to it later?

#maybe I can clean up a list and then do fuzzy mathcing
#when adding the alias back to the gdb file? 
#

def normalize(s):
    remove = ('incorporated', 'corporation', 'corp', 'inc', 'company', 'co', 'limited', 'partnership', 'partner',
          'llc', 'ltd','llp', 'lp', 'l l c','l p', 'et al', 'et ux')
    if s != None:      
        for p in string.punctuation:
            s = s.replace(p, '')
        s = s.lower()
        for item in remove:
            s = s.replace(item, '')
        return s.strip()
    else: return 'None'

def opr_alias(opr_list):
    RATIO_CUTOFF = 90  
    operators_normal = []
    for opr in opr_list:
        normalized = normalize(opr)
        operators_normal.append(normalized)
   
   #print(operators_normal[:20])

    opr_count = collections.Counter(operators_normal)
    
    #for opr, count in opr_count.most_common(10):
    #    print('{0} {1}'.format(opr, count))
    #    
    
    opr_set = set(operators_normal)
    opr_sort_set = sorted(opr_set)
    
    
    name_group = []
    groups = []
    
    
    for name in opr_sort_set:
        name_group.append(name)
        for name2 in opr_sort_set:
            if fuzz.partial_ratio(name, name2) >= RATIO_CUTOFF and name != name2:
                name_group.append(name2)
        
        name_set = tuple(name_group)
        groups.append(name_set)
        name_group = []
    
    
    sorted_groups = []
    for sub_group in groups:
        sorted_groups.append(tuple(sorted(sub_group)))
    
    
    opr_group_set = set(sorted_groups)
    
    
    opr_count['LOW'] = 0
    opr_lookup = {}
    
    for opr_group in opr_group_set:
        most_common_opr = 'LOW'
        for opr_name in opr_group:
            if opr_count[opr_name] > opr_count[most_common_opr]:
                most_common_opr = opr_name
        opr_lookup.setdefault(most_common_opr, opr_group)
                
    #pp = pprint.PrettyPrinter()
    #pp.pprint(opr_lookup)
    
    ##USE THE REVERSE LOOKUP FOR ADDING ALIAS THROUGH ARCPY
    opr_lookup_reverse = {}
    for key, values in opr_lookup.iteritems():
        for val in values: 
            opr_lookup_reverse.setdefault(val, key)
    return({"opr_lookup":opr_lookup,"opr_lookup_reverse":opr_lookup_reverse})
        
#pp.pprint(opr_lookup_reverse)
        
        
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