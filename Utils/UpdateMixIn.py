from abc import ABCMeta, abstractmethod
import datetime
import json

import MLBProjections.MLBProjections.Environ as ENV

import pprint

################################################################################
################################################################################





################################################################################
################################################################################


class UpdateMixIn(metaclass=ABCMeta):

    def __init__(self):
        self.manager = {}

        try:
            with open(ENV.getManagerFile()) as fileIn:
                self.manager = json.load(fileIn)
        except FileNotFoundError:
            pass



    def getItem(self):
        key = self.getManagerKey()
        item = self.manager.get(key, "2016-04-04 01:01:01.01")
        return datetime.datetime.strptime(item, "%Y-%m-%d %H:%M:%S.%f")


    def clearManagerFile(self):
        key = self.getManagerKey()
        self.manager.pop(key, None)


    def checkUpdate(self):

        update = False
        today = datetime.datetime.today()
        checkDate = self.getItem()
        try:
            checkDate = datetime.datetime.strptime(checkDate, "%Y-%m-%d %H:%M:%S.%f")
            if (datetime.date.fromtimestamp(today.timestamp()) - datetime.date.fromtimestamp(checkDate.timestamp())).days >= 1 and today.hour > 3:
                update = True
        except TypeError:
            update = True
        return update



    def updateManagerFile(self):
        key = self.getManagerKey()
        self.manager[key] = str(datetime.datetime.today())
        self.writeManager()


    def writeManager(self):
        with open(ENV.getManagerFile(), "w") as fileOut:
            json.dump(self.manager, fileOut)


    def checkManager(self, item):
        return self.manager.get(item, None)


    @abstractmethod
    def getManagerKey(self):
        pass


    @abstractmethod
    def update(self):
        pass
