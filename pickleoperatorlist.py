# -*- coding: utf-8 -*-
"""
Created on Tue Aug 12 10:29:14 2014

@author: wnixon
"""

#Pickle a list of operators to use in running the script

import cPickle as pkle
import sys



import arcpy

GDB = r'K:\DRILLING_INFO\DI14gdb_31abc_FULL\DI14gdb_31a.gdb'
GDB_FILE = 'DI_Landtracs' 
PICKLE_FILE = 'operators2.p'

arcpy.env.workspace = GDB

operator_list = []

with arcpy.da.SearchCursor(GDB_FILE, ('Grantee')) as cursor:
    for row in cursor:
        operator_list.extend(row)

pkle.dump(operator_list, open(PICKLE_FILE, 'wb'))
