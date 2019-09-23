# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 16:35:34 2018

@author: Maël Soulié
"""
from ics import Calendar
from datetime import datetime, timedelta
import dateutil.parser
import log
import logging
import sys
from requestSafe import requestSafe

log.setup_logging()
logger = logging.getLogger(__name__)

ADE_DOWN_MESSAGE = "ADE Down"

SUMMER_HOUR=False


if len(sys.argv)==2 and sys.argv[1]=="testRoom":
    test = True
else:
    test = False


class roomGetter:
    def __init__(self, bot, chat_id, getHelpMessage):
        self._getHelpMessage = getHelpMessage
        self.waitingMessages = [
            "Il y a beaucoup de salles a l'N7 tu sais.",
            "J'ai un peu la flemme auourd'hui alors tu vas attendre un peu",
            "Tout est question de patience tu sais ",
            "Ne bouge pas je reviens bientôt",
            "Nous nous efforçons d’écourter agréablement votre attente, merci de bien vouloir patienter quelques instants ",
            "Merci de bien vouloir patienter quelques instants. ",
            "Sérieux tu veux rester dedans avec ce beau temps dehors ? ",
            "Sinon tu préfères quelle salle ? ",
            "J'ai une information de la plus grande importance pour toi, tu veux savoir ce que c'est ?",
            "Vive le bot Maël Soulié",
            "Je cherche",
            "Trop de salle dans ma base, je vais bientôt bruler !!!",
            "ça eduramme ce réseau, franchement pour une école de réseau ça la fout mal !",
            "L'ENSEEHIT c'est quoi ?",
            "Tu connais l'ENSEEIHT ?"]
        
        splitDay = str(datetime.now().isoformat()).split('T')  # magic
        self.currentDate = splitDay[0]
        url = "https://edt.inp-toulouse.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?resources=343,341,335,330,329,502,319,318,317,316,315,314,313,312,311,310,309,308,307,306,305,304,303,302,300,298,297,296,295,293,292,291,290,288,287,286,285,284,283,282,281,460,280,279,278,277,276,275,274,273,272,266,265,264,261,259,250,249,248,247,243,242,241,239,238,237,211,939,938,942,947&projectId=20&calType=ical&firstDate="\
            +self.currentDate\
            +"&lastDate="\
            +self.currentDate
        if (SUMMER_HOUR):
             #summer hour :
            self.currentTime = int(splitDay[1][0:2] + splitDay[1][3:5]) - 200
        else :
            self.currentTime = int(splitDay[1][0:2] + splitDay[1][3:5]) - 100
            
        self.bot = bot
        self.chat_id = chat_id
        if not test:
            if (self.currentTime > 1800 and self.currentTime < 24000) or \
                    (self.currentTime > 0 and self.currentTime < 500):
                self.bot.sendMessage(self.chat_id,
                                     "l'N7 est fermée à cette heure là.")
 #       self.bot.sendMessage(self.chat_id, random.choice( \
 #                self.waitingMessages))
        
        self.requestUrl = requestSafe(url,"RoomCache")
        data = self.requestUrl.getRequestAnswer()
        if data==False :
            # ADE is down and cache is empty
            logger.error("Ade is down and cache is empty")
            self.adeDown = True
        else :
            self.adeDown = False
            
    #        joke = jokes.jokesContener()
            #cache generation :
    #        if not contentCache:
    #            self.bot.sendMessage(self.chat_id, "Pour patienter, une blague\n" + joke.getJoke())
    #            contentCache = requests.get(url).text
    #            roomCache.write("RoomCache", contentCache)
    #        else :
    #            self.bot.sendMessage(self.chat_id, random.choice( \
    #                 self.waitingMessages))
            self.calendar = Calendar(data)  # create the calendar from URL
            #self.currentDate = '2018-09-25'
            #self.currentTime = '1200'
            
            self.allRooms = set(['A001',
                                 'A002',
                                 'A003',
                                 'A005a',
                                 'A005b',
                                 'A201',
                                 'A202',
                                 'A203',
                                 'A220',
                                 'A301',
                                 'A302',
                                 'A303',
                                 'A304',
                                 'B00',
                                 'B004',
                                 'B005',
                                 'B006',
                                 'B007',
                                 'B101',
                                 'B102',
                                 'B103',
                                 'B104',
                                 'B105',
                                 'B118',
                                 'B122',
                                 'B123',
                                 'B124',
                                 'B201',
                                 'B204',
                                 'B205',
                                 'B206',
                                 'B207',
                                 'B208',
                                 'B209',
                                 'B301',
                                 'B302',
                                 'B303',
                                 'B304',
                                 'B305',
                                 'B306',
                                 'B307',
                                 'B308',
                                 'C002',
                                 'C004',
                                 'C006',
                                 'C008',
                                 'C010',
                                 'C101',
                                 'C102',
                                 'C103',
                                 'C104',
                                 'C106',
                                 'C108',
                                 'C111',
                                 'C112',
                                 'C201',
                                 'C202',
                                 'C203',
                                 'C204',
                                 'C205',
                                 'C206',
                                 'C209',
                                 'C214a',
                                 'C214b',
                                 'C216a',
                                 'C216b',
                                 'C301',
                                 'C302',
                                 'C303',
                                 'C304',
                                 'C305',
                                 'C306',
                                 'C308',
                                 'C309',
                                 'C310'])
            self.ARooms = set(['A001',
                               'A002',
                               'A003',
                               'A005a',
                               'A005b',
                               'A201',
                               'A202',
                               'A203',
                               'A220',
                               'A301',
                               'A302',
                               'A303',
                               'A304'])
            self.BRooms = set(['B00',
                               'B004',
                               'B005',
                               'B006',
                               'B007',
                               'B101',
                               'B102',
                               'B103',
                               'B104',
                               'B105',
                               'B118',
                               'B122',
                               'B123',
                               'B124',
                               'B201',
                               'B204',
                               'B205',
                               'B206',
                               'B207',
                               'B208',
                               'B209',
                               'B301',
                               'B302',
                               'B303',
                               'B304',
                               'B305',
                               'B306',
                               'B307',
                               'B308'])
            self.CRooms = set(['C002',
                               'C004',
                               'C006',
                               'C008',
                               'C010',
                               'C101',
                               'C102',
                               'C103',
                               'C104',
                               'C106',
                               'C108',
                               'C111',
                               'C112',
                               'C201',
                               'C202',
                               'C203',
                               'C204',
                               'C205',
                               'C206',
                               'C209',
                               'C214a',
                               'C214b',
                               'C216a',
                               'C216b',
                               'C301',
                               'C302',
                               'C303',
                               'C304',
                               'C305',
                               'C306',
                               'C308',
                               'C309',
                               'C310'])
            self.linuxRooms = set(['C201',
                                   'C202',
                                   'C203',
                                   'C204',
                                   'C205',
                                   'C206',
                                   'C209',
                                   'C214a',
                                   'C214b',
                                   'C216a',
                                   'C216b',
    							   'C301',
    							   'C302',
                                   'C303',
                                   'C304',
                                   'C305',
                                   'C306'])

        # Parse the fucking horrible format from an event .begin or .end
    # Also, n7 sucks so +2H because they can't handle timezones

    def parseHalfHour(self, eventHour):
        return dateutil.parser.parse(str(eventHour)) + timedelta(hours=2)

    def isEventHappeningOnNextHour(self, event):
        self.deltaCurrentTime = int(self.currentTime) + 60
        eventStartDate = str(event.begin).split('T')[0]
        eventStartTime = int(str(event.begin)[11:13] + str(event.begin)[14:16])
        eventEndTime = int(str(event.end)[11:13] + str(event.end)[14:16])
        return self.currentDate == eventStartDate \
            and ((eventStartTime <= self.currentTime
                  and eventEndTime >= self.currentTime)
                 or (eventStartTime <= self.deltaCurrentTime
                     and eventEndTime >= self.deltaCurrentTime))

    def parseRooms(self):
        roomsOccuped = set()
        for event in self.calendar.events:
            if(self.isEventHappeningOnNextHour(event)):
                for salle in event.location.split(','):
                    if salle in self.allRooms:
                        roomsOccuped.add(salle)
        return roomsOccuped

    def printRooms(self, roomsSet):
        logger.info("printRooms launched")
        ret = ""
        for room in sorted(roomsSet):
            ret += room + " "
        logger.info("printRooms almost finished, before return statement")
        return ret

    def getAnswer(self, message):
        logger.info("Room.getAnswer has started with parameter : " \
                    + message)
        if self.adeDown :
            return ADE_DOWN_MESSAGE
        else :
            if '_' in message:
                notInterogationDot = True
                if '@' in message:
                    splitMessage = message.split('@')[0].split('_')
                else:
                    splitMessage = message.split('_')
            else:
                notInterogationDot = False
                splitMessage = message.split(' ')
    
            hasFirstPara = len(splitMessage)>1
            if hasFirstPara:
                firstPara = splitMessage[1]
            hasSecondPara = len(splitMessage)>2
            if hasSecondPara:
                secondPara = splitMessage[2]
            logger.info("Room.getAnswer() => continuing")
            if hasFirstPara and hasSecondPara and secondPara == "DISPO" :
                if firstPara == "A":
                    ARoomsAvailables = self.ARooms - self.parseRooms()
                    return "Salles A dispo dans la prochaine heure :\n    " \
                        + self.printRooms(ARoomsAvailables)
                elif firstPara == "B":
                    BRoomsAvailables = self.BRooms - self.parseRooms()
                    return "Salles B dispo dans la prochaine heure :\n    " \
                        + self.printRooms(BRoomsAvailables)
                elif firstPara == "C":
                    CRoomsAvailables = self.CRooms - self.parseRooms()
                    return "Salles C dispo dans la prochaine heure :\n    " \
                        + self.printRooms(CRoomsAvailables)
                elif firstPara == "CNOTLINUX":
                    CRoomsAvailables = self.CRooms - self.parseRooms()-self.linuxRooms
                    return "Salles C non Linux dispo dans la prochaine heure :\n    " \
                        + self.printRooms(CRoomsAvailables)
                elif firstPara == "LINUX":
                    linuxRoomsAvailables = self.linuxRooms - self.parseRooms()
                    return "Salles Linux dispo dans la prochaine heure :\n    " \
                        + self.printRooms(linuxRoomsAvailables)
                else : 
                    logger.info("Room.getAnswer() => Help 1 IF")
                    return self._getHelpMessage()
            elif hasFirstPara \
              and (hasSecondPara and secondPara == "?" )\
              or notInterogationDot:
                if firstPara == "DISPO":
                    allRoomsAvailables = self.allRooms - self.parseRooms()
                    return "Salles dispo dans la prochaine heure :\n    " \
                        + self.printRooms(allRoomsAvailables)
                else : 
                    logger.info("Room.getAnswer() => Help 2 ELIF ; firsPara : " \
                                + firstPara)
                    return self._getHelpMessage()
            else : 
                logger.info("Room.getAnswer() => Help 3 ELSE")
                return self._getHelpMessage()

if test:
    room = roomGetter(None, None, None)
    print(room.getAnswer("SALLES DISPO ?"))
    print(room.getAnswer("SALLES A DISPO ?"))
    print(room.getAnswer("SALLES B DISPO ?"))
    print(room.getAnswer("SALLES C DISPO ?"))
    print(room.getAnswer("SALLES linux DISPO ?"))
    print(room.getAnswer("SALLES ?"))
    print(room.getAnswer("SALLES A ?"))
    print(room.getAnswer("SALLES B ?"))
    print(room.getAnswer("SALLES C ?"))
    print(room.getAnswer("SALLES LINUX ?"))
    print(room.getAnswer("SALLES HELP ?"))

