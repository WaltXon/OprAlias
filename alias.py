# -*- coding: utf-8 -*-
"""
Created on Wed Sep 10 16:18:03 2014

@author: waltn
"""

import arcpy
import closematchesV3 as cm

arcpy.env.workspace = 'Z:\GIS\HENDRICK_RANCH\HENDRICK_RANCH.gdb'
TARGET_FILE = 'di_production_HR_20140910'
TARGET_FIELD = 'operatorName'

operator_list = []

with arcpy.da.SearchCursor(TARGET_FILE, (TARGET_FIELD)) as scursor:
    for row in scursor:
        operator_list.extend(row)

print("Operator List Complete, [:10] = {0}".format(operator_list[:10]))

field = "OprAlias"
##Add a column for OperatorAlias if the column does not already exist
if field not in arcpy.ListFields(TARGET_FILE):
    arcpy.AddField_management(TARGET_FILE, field, "TEXT", 50, "", "","", "NULLABLE") 
    print("Added Field Complete")
else:
    print("Field Already In File")
                     
OprLookupRev = cm.opr_alias(operator_list)['opr_lookup_reverse']

print("OprLookupRev complete, [:10] = {0}".format(OprLookupRev))

with arcpy.da.UpdateCursor(TARGET_FILE,[TARGET_FIELD,'OprAlias'] ) as ucursor: 
    for row in ucursor:
        row[1] = OprLookupRev[cm.normalize(row[0])]
        print("row[1] ({0}) == row[0] ({1})".format(row[1], row[0]))
        ucursor.updateRow(row)

print("updates complete")