from abc import ABCMeta, abstractmethod
from pprint import pprint

################################################################################
################################################################################





################################################################################
################################################################################


class TicketManager(metaclass=ABCMeta):

    def __init__(self, gameJson):

        self.gameJson = gameJson
        self.homeTeam = None
        self.awayTeam = None

        self.initializeSport()
        self.setTicketTypes()

        self.runTicketMachine()


    @abstractmethod
    def setTicketTypes(self):
        pass


    @abstractmethod
    def initializeSport(self):
        pass


    @abstractmethod
    def runTicketMachine(self):
        pass