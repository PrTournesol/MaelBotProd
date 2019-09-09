#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 13:08:32 2018

@author: n7
"""

import requests
from datetime import datetime, timedelta
import dateutil.parser

splitDay = str(datetime.now().isoformat()).split('T')  # magic
day = splitDay[0]
url = "https://edt.inp-toulouse.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?resources=1876&projectId=42&calType=ical&firstDate=" \
            +day\
            +"&lastDate="\
            +day
#url='https://api.github.com/events'

print(url)
adeError = False

try :
    r = requests.get(url,timeout=2)
    if (("Le projet est invalide") in str(r.text)):
        adeError= True
    
except Exception as e :
    print("\nGeneral error : \n\t"+str(e))
    adeError= True
    
print("\n\nAde Down " if adeError else "Ade works")

    