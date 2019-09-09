import os
from datetime import datetime
import logging
import log

log.setup_logging()
logger = logging.getLogger(__name__)

class Cache:

    def __init__(self, fileName):
        self.fileName = fileName
        if os.getcwd() == '/':
            os.chdir("/TelegramBot/")
        if not os.path.exists("cache"):
            os.mkdir("cache")

    def write(self, content):
        logger.info("Write : " + self.fileName + " to cache")
        if "cache/" + self.fileName + ".tmp" in os.listdir("cache"):
            os.remove("cache/" + self.fileName + ".tmp")
        file = open("cache/" + self.fileName + ".tmp", "wb")
        file.write(content.encode('utf8'))
        file.close()

    def read(self):
        logger.info("Read : " + self.fileName + " from cache")
        try:
            file = open("cache/" + self.fileName + ".tmp", "rb")
            content = file.read().decode('utf8')
            file.close()
        except BaseException:
            logger.info(self.fileName + " not in cache")
            content = False
        return content

    def getFileAge(self):
        if "cache/" + self.fileName + ".tmp" in os.listdir("cache"):
            creationDate = os.path.getmtime("cache/"+self.fileName)
            age = int(datetime.datetime.now().timestamp() - creationDate)
            return age
        else:
            return None

    def cleanFileCache(self):
        if "cache/" + self.fileName + ".tmp" in os.listdir("cache"):
            os.remove("cache/"+self.fileName)
            logger.info("suppression de "+self.fileName+" du cache")
        else :
            logger.info(self.fileName + " not in cache")