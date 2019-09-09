from cache import *
from ics import Calendar, Event
from datetime import datetime, timedelta
import dateutil.parser
import log
from requestSafe import requestSafe

log.setup_logging()
logger = logging.getLogger(__name__)

ADE_DOWN_MESSAGE = "ADE Down"
SUMMER_HOUR=False

class adeGetter:
    def __init__(self):
        splitDay = str(datetime.now().isoformat()).split('T')  # magic
        self.day = splitDay[0]
        url1 = "https://edt.inp-toulouse.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?resources=1876&projectId=42&calType=ical&firstDate=" \
            +self.day\
            +"&lastDate="\
            +self.day
        url2 = "https://edt.inp-toulouse.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?resources=1879&projectId=42&calType=ical&firstDate=" \
            +self.day\
            +"&lastDate="\
            +self.day
            
        self.requestUrl1 = requestSafe(url1,"dataurl1")
        self.requestUrl2 = requestSafe(url2,"dataurl2")
        logger.info("url GR1 : "+url1)
        logger.info("url GR2 : "+url2)
        
        data1 = self.requestUrl1.getRequestAnswer()
        if data1==False :
            # ADE is down and cache is empty
            logger.error("Ade is down and cache is empty")
            self.adeDown = True
        else :
            self.adeDown = False
            data2 = self.requestUrl2.getRequestAnswer()
            
            self.c = Calendar(data1)  # create the calendar from URL
            self.c2 = Calendar(data2)
            
            splitNextDay = str(
                dateutil.parser.parse(
                    self.day) +
                timedelta(
                    days=1)).split(' ')
            self.nextDay = splitNextDay[0]
            self.classes = {}
            self.classes2 = {}
            self.classesND = {}
            self.classes2ND = {}
            self.defaultEvent = Event()
            self.defaultEvent.description = 'Personne'
            self.defaultEvent.location = 'Maison'
            self.defaultEvent.name = 'Pas cours'

    # Parse the fucking horrible format from an event .begin or .end
    # Also, n7 sucks so +2H because they can't handle timezones
    def parseHour(self, eventHour):
        return dateutil.parser.parse(str(eventHour)) + timedelta(hours=2)

    # Suboptimal way to store all the classes of current day
    def storeClassesDay(self):
        for i in ['08', '10', '14', '16', '18']:
            self.classes[i] = self.defaultEvent
            self.classes2[i] = self.defaultEvent
        for e in self.c.events:
            if(self.day in str(e.begin)):
                self.classes[self.parseHour(e.begin).strftime('%H')] = e
        for e in self.c2.events:
            if(self.day in str(e.begin)):
                self.classes2[self.parseHour(e.begin).strftime('%H')] = e

    def storeClassesNextDay(self):
        for i in ['08', '10', '14', '16', '18']:
            self.classesND[i] = self.defaultEvent
            self.classes2ND[i] = self.defaultEvent
        for e in self.c.events:
            if(self.nextDay in str(e.begin)):
                self.classesND[self.parseHour(e.begin).strftime('%H')] = e
                self.classes2ND[self.parseHour(e.begin).strftime('%H')] = e

    # More format bullshit, returns 8, 10, 14, 16 or 18 (keys to the classes
    # dictionnary)
    def hourToKey(self):
        hLims = ['945', '1545']
        hCur = datetime.now().hour
        hStr = datetime.now().strftime('%H%M')
        #hCur = 12
        #hStr = "1203"
        if(hCur == 9 and int(hStr) > int(hLims[0])):
            hCur = 10
        elif(hCur == 9):
            hCur = 8

        if(hCur == 15 and int(hStr) > int(hLims[1])):
            hCur = 16
        elif(hCur == 15):
            hCur = 14
        if(hCur == 17):
            hCur = 16
        if(hCur < 8):  # De 00h à 08h
            hCur = 8
        if(12 <= hCur <= 14):
            hCur = 14
        if(hCur >= 18):
            hCur = 18
        if(hCur == 11):
            hCur = 10
        if(hCur == 8):
            return ('0' + str(hCur))if SUMMER_HOUR else ('0' + str(hCur+1))
        return str(hCur) if SUMMER_HOUR else str(hCur+1) 

    def InfoGroups(self):
        groups = []
        if (self.classes[self.hourToKey()] != self.classes2[self.hourToKey()]):
            groups.append(self.classes[self.hourToKey()])
            groups.append(self.classes2[self.hourToKey()])
            return groups
        return None

    # following crap returns the fucking current thingies
    def CurrentRoom(self):
        if self.adeDown :
            return ADE_DOWN_MESSAGE
        self.storeClassesDay()
        if (self.InfoGroups()):
            return "Groupe 1 : " + \
                self.InfoGroups()[0].location + " | Groupe 2 : " + self.InfoGroups()[1].location
        return self.classes[self.hourToKey()].location

    def CurrentTeacher(self):
        if self.adeDown :
            return ADE_DOWN_MESSAGE
        self.storeClassesDay()
        desc = self.classes[self.hourToKey()].description.split('\n')
        if(self.InfoGroups()):
            return "Groupe 1 :  " + self.InfoGroups()[0].description.split('\n')[2] + \
                " | Groupe 2 : " + self.InfoGroups()[1].description.split('\n')[2]
        return desc[2] if len(desc) > 1 else self.defaultEvent.description

    def CurrentClass(self):
        if self.adeDown :
            return ADE_DOWN_MESSAGE
        self.storeClassesDay()
        cours = self.classes[self.hourToKey()].name.split('-')
        if(self.InfoGroups()):
            return "Groupe 1 : " + self.InfoGroups()[0].name.split('-')[2] + \
                " | Groupe 2 : " + self.InfoGroups()[1].name.split('-')[2]
        return cours[3] if len(cours) > 1 else self.defaultEvent.name

    # and following crap return the next thingies
    # + 2H because a class is approx 2h long, and I'm using integer keys like a dumbass
    def NextKey(self):
        if(int(self.hourToKey()) == 10):
            return 14
        return int(self.hourToKey()) + 2

    def nextRoom(self):
        self.storeClassesDay()
        return self.classes[str(self.NextKey())].location

    def NextTeacher(self):
        self.storeClassesDay()
        desc = self.classes[str(nextKey())].description.split('\n')
        return desc[2] if len(desc) > 1 else self.defaultEvent.description

    def NextClass(self):
        self.storeClassesDay()
        cours = self.classes[str(NextKey())].name.split('-')
        return cours[3] if len(cours) > 1 else self.defaultEvent.name
    # TODO

    def printClassesDay(self, classes):
        timetable = ""
        for key, val in classes.items():
            timetable += "\n"
            timetable += val.name.split('-')[3] if len(
                val.name.split('-')) > 2 else val.name
            timetable += "\n"
            timetable += val.description.split('\n')[2] if len(
                val.description.split('\n')) > 1 else val.description
            timetable += "\n"
            timetable += val.location
            timetable += "\n"
            # print(val.description.split('\n'))
        return timetable
#a = adeGetter()
#message = a.CurrentRoom()
# print(message)
#ade = adeGetter()
# ade.storeClassesDay()
# print(ade.CurrentRoom())
# print(ade.nextRoom())
# ade.storeClassesNextDay()
# print("today")
# print(ade.printClassesDay(ade.classes))
# print("tomo")
# print(ade.printClassesDay(ade.classesND))
# print(ade.CurrentRoom())
# print(ade.nextRoom())
# print(ade.CurrentTeacher())
# print(ade.NextTeacher())
# print(ade.CurrentClass())
# print(ade.NextClass())
# print(ade.getClassesDay())
# print(ade.classes)
