# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 17:45:09 2018

@author: n7
"""
import random
import log
import logging

log.setup_logging()
logger = logging.getLogger(__name__)

class jokes:
    def __init__(self,getHelpMessage):
        self._getHelpMessage = getHelpMessage
        self.jokes_file = "jokes_content.txt"
        return 
    
    def getJoke(self):
        try:
            file = open(self.jokes_file, "rb")
            content = file.read().decode('utf8')
            jokes = content.split("\n")
            #print(jokes)
            file.close()
        except BaseException:
            logger.info("jokes file content not found")
            jokes = []
        return random.choice(jokes).replace("\\n","\n")
 
    def getAllJokes(self):
        try:
            file = open(self.jokes_file, "rb")
            content = file.read().decode('utf8')
            jokes = content.split("\n")
            #print(jokes)
            file.close()
        except BaseException:
            logger.info("jokes file content not found")
            jokes = []
        return jokes 
    
    def addJoke(self,joke):
        if (joke in self.getAllJokes()):
            return "la blague \""+joke+"\" est déjà dans ma base"
        else :
            try:
                file = open(self.jokes_file, "a")
                file.write("\n"+joke)
                file.close()
                return "la blague \""+joke+"\" a bien été ajouté à ma base"
            except BaseException:
                logger.info("jokes file write error")
                return "erreur d'écriture dans ma base, recommencez"
            
    def removeJoke(self,joke):
        if (joke not in self.getAllJokes()):
            return "la blague \""+joke+"\" n'est pas dans ma base"
        else :
            try:
                file = open(self.jokes_file, "rb")
                content = file.read().decode('utf8')
                file.close          
                
                content = content.replace(joke+"\n", '')  
                
                file = open(self.jokes_file, "wb")
                file.write(content.encode('utf8'))
                file.close()
                return "la blague \""+joke+"\" a bien retirée de ma base"
            except BaseException:
                logger.info("jokes file write error")
                return "erreur de modification de ma base, recommencez"
            
    def getAnswer(self, message):
        logger.info("jokes.getAnswer has started with parameter : " \
                    + message)
        if '_' in message or '/' in message :
            #notInterogationDot = True
            if '@' in message:
                splitMessage = message.split('@')[0].split('_')
            else:
                splitMessage = message.split('_')
        else:
            #notInterogationDot = False
            splitMessage = message.split(' ')

        hasFirstPara = len(splitMessage)>0
        if hasFirstPara:
            firstPara = str.upper(splitMessage[0])
        hasSecondPara = len(splitMessage)>1
        if hasSecondPara:
            secondPara = splitMessage[1]
            #print("2 : "+secondPara)
        
        #print("1 :"+firstPara)
        
        if firstPara == "BLAGUE" or firstPara == "/BLAGUE":
            return self.getJoke()
        elif hasSecondPara:
            if firstPara == "ADD" or firstPara == "/ADD":
                content = secondPara[7:]
                if content != "" :
                    print(content)
                    return self.addJoke(content)
                else:
                    return ("impossible d'ajouter une blague vide mettez votre \
                            blague après l'eapace")
            elif firstPara == "REMOVE" or firstPara == "/REMOVE":
                content = secondPara[7:]
                if content != "":
                    return self.removeJoke(content)
                else:
                    return ("impossible d'enlever une blague vide mettez votre \
                            blague après l'eapace")
        else : 
            logger.info("Room.getAnswer() => Help 1 IF")
            return self._getHelpMessage()
    
#joke = jokes(None)
#print("\n\n"+joke.getJoke())
#print("\n\n"+joke.addJoke("toto joke"))