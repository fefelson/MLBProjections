from .Ticket import Ticket, StateTicket

################################################################################
################################################################################





################################################################################
################################################################################


class FlyOut(Ticket):

    def getStateTicket(self, diamondState):
        stateTicket = None
        if diamondState in ("firstBase_secondBase_thirdBase",
                            "secondBase_thirdBase",
                            "thirdBase"):
            stateTicket = ThirdBaseFlyOut()
        else:
            stateTicket = FlyOutState()
        return stateTicket


################################################################################
################################################################################


class ThirdBaseFlyOut(StateTicket):

    def recordOuts(self, umpire):
        umpire.recordOut()


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordPitcherOut(pitcherId)
        scoreKeeper.recordBatterPA(batterId)
        runnerId, onHook = diamond.popBase("thirdBase")
        if umpire.getOuts() < 3:
            scoreKeeper.recordTeamRun()
            scoreKeeper.recordBatterRun(runnerId)
            scoreKeeper.recordBatterRbi(batterId)
            scoreKeeper.recordRun(pitcherId)
        if scoreKeeper.exOuts() < 3:
            scoreKeeper.recordPitcherER(pitcherId)


    def moveBases(self, diamond):
        pass


    def reachedBase(self, pitcherId, batterId, diamond):
        pass


################################################################################
################################################################################


class FlyOutState(StateTicket):

    def recordOuts(self, umpire):
        umpire.recordOut()


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordPitcherOut(pitcherId)
        scoreKeeper.recordBatterAB(batterId)


    def moveBases(self, diamond):
        pass


    def reachedBase(self, pitcherId, batterId, diamond):
        pass


################################################################################
################################################################################
