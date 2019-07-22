from abc import ABCMeta, abstractmethod

################################################################################
################################################################################





################################################################################
################################################################################


class Ticket(metaclass=ABCMeta):

    @abstractmethod
    def getStateTicket(self, diamondState):
        pass


################################################################################
################################################################################


class StateTicket(metaclass=ABCMeta):

    @abstractmethod
    def recordOuts(self, umpire):
        pass


    @abstractmethod
    def moveBases(self, diamond):
        pass


    @abstractmethod
    def reachedBase(self, pitcher, batter, diamond):
        pass


    @abstractmethod
    def recordEvents(self, pitcher, batter, diamond, umpire, scoreKeeper):
        pass


################################################################################
################################################################################
