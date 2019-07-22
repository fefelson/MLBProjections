from .Ticket import Ticket, StateTicket

################################################################################
################################################################################





################################################################################
################################################################################


class Out(Ticket):

    def getStateTicket(self, diamondState):
        return OutState()


################################################################################
################################################################################


class OutState(StateTicket):


    def recordOuts(self, umpire):
        umpire.recordOut()


    def moveBases(self, diamond):
        pass


    def reachedBase(self, pitcherId, batterId, diamond, scoreKeeper):
        pass


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        self.scoreKeeper.recordPitcherOut(pitcherId)
        self.scoreKeeper.recordBatterAB(batterId)


################################################################################
################################################################################
