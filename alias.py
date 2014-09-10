# -*- coding: utf-8 -*-
"""
Created on Wed Sep 10 16:18:03 2014

@author: waltn
"""

import arcpy
import closematchesV3 as cm


TARGET_FILE = r''
GRANTEE = 'Grantee'

operator_list = []

with arcpy.da.SearchCursor(TARGET_FILE, (GRANTEE)) as scursor:
    for row in scursor:
        operator_list.extend(row)
        
field = "OprAlias"
##Add a column for OperatorAlias if the column does not already exist
if field not in arcpy.ListFields(TARGET_FILE):
    arcpy.AddField_management(TARGET_FILE, field, "TEXT", 50, "", "",
                          "", "NULLABLE") 
                     
                     
OprLookupRev = cm.opr_alias(operator_list)['opr_lookup_reverse']

with arcpy.da.UpdateCursor(TARGET_FILE,[GRANTEE,'OprAlias'] ) as ucursor: 
    for row in ucursor:
        row[1] = OprLookupRev[cm.normalize(row[0])]
        ucursor.updateRow(row)

print("updates complete")