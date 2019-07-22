from .Ticket import Ticket, StateTicket

################################################################################
################################################################################





################################################################################
################################################################################


class StrikeOut(Ticket):

    def getStateTicket(self, diamondState):
        return StrikeOutState()


################################################################################
################################################################################


class StrikeOutState(StateTicket):


    def recordOuts(self, umpire):
        umpire.recordOut()


    def moveBases(self, diamond):
        pass


    def reachedBase(self, pitcherId, batterId, diamond, scoreKeeper):
        pass


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        self.scoreKeeper.recordPitcherK(pitcherId)
        self.scoreKeeper.recordBatterK(batterId)


################################################################################
################################################################################
