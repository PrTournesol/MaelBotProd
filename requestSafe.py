#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 14:14:25 2018

@author: Pr Tournesol

make the request URL, handle the cache. If the request doen't succeed,
 return the content already in cache
"""

from cache import *
import requests
import log

log.setup_logging()
logger = logging.getLogger(__name__)

MAXAGE = 30 * 60

class requestSafe:
    def __init__(self, pUrl, pCacheName):
        self.url= pUrl
        self.cacheName = pCacheName
        self.cache = Cache(self.cacheName)
#        logger.info(" Making requestSafe object with url : "+self.url+" and cacheName File : "+self.cacheName)
        
    def getRequestAnswer(self):
    # get cache file age
        age = self.cache.getFileAge()
        if age == None or age > MAXAGE:
            # cache file is obsolete, try to update with new request :
            result = self.makeRequest()
            if not result:
                # don't clear cache, read it instead
                result = self.cache.read()
            else:
                # clear cache and replace it
                self.cache.cleanFileCache()
                self.cache.write(result)
        else :
            # read cache simply
            result = self.cache.read()
        return result
    
    def makeRequest(self):
        adeError = False
        try :
            answer = requests.get(self.url,timeout=2)
            answerText = str(answer.text)
            print("answerText : "+answerText)
            if (("Le projet est invalide") in answerText):
                logger.info("Le projet est invalide")
                adeError= True
        except Exception as e :
            logger.info("Request error : \n\t"+str(e))
            adeError= True
        if adeError:
            logger.info("Ade Down on url : "+ self.url)
            return False
        else:
#            logger.info("Ade works on url : "+ self.url)
            return answerText
    
#requestTest= requestSafe("https://edt.inp-toulouse.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?resources=1876&projectId=42&calType=ical&firstDate=2018-10-26&lastDate=2018-10-26","TEST")
#requestTest= requestSafe("https://api.github.com/events","Github")

#print("\n---RESULT : \n\t"+str(requestTest.getRequestAnswer()))

