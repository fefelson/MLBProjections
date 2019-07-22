from abc import ABCMeta, abstractmethod
from pprint import pprint

################################################################################
################################################################################





################################################################################
################################################################################


class TicketManager(metaclass=ABCMeta):

    def __init__(self, db):

        self.db = db
        self.db.openDB()
        self.homeTeam = None
        self.awayTeam = None


    def __del__(self):
        self.db.closeDB()


    @abstractmethod
    def setTicketTypes(self):
        pass


    @abstractmethod
    def initializeSport(self):
        pass


    @abstractmethod
    def runTicketMachine(self):
        pass
