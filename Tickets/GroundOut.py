from .Ticket import Ticket, StateTicket

################################################################################
################################################################################





################################################################################
################################################################################


class GroundOut(Ticket):

    def getStateTicket(self, diamondState):
        stateTicket = None
        if diamondState == "firstBase_secondBase_thirdBase":
            stateTicket = BasesLoadedGroundOut()
        elif diamondState == "secondBase_thirdBase":
            stateTicket = SecondThirdGroundOut()
        elif diamondState == "firstBase_thirdBase":
            stateTicket = FirstThirdGroundOut()
        elif diamondState == "firstBase_secondBase":
            stateTicket = FirstSecondGroundOut()
        elif diamondState == "thirdBase":
            stateTicket = ThirdGroundOut()
        elif diamondState == "secondBase":
            stateTicket = SecondGroundOut()
        elif diamondState == "firstBase":
            stateTicket = FirstGroundOut()
        else: #Bases Empty
            stateTicket = EmptyGroundOut()
        return stateTicket


################################################################################
################################################################################


class BasesLoadedGroundOut(StateTicket):

    def recordOuts(self, umpire):
        umpire.recordOut()


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordPitcherOut(pitcherId)
        scoreKeeper.recordBatterAB(batterId)


    def moveBases(self, diamond):
        # Runner out advancing Home
        diamond.popBase("thirdBase")
        diamond.moveBase("secondBase", "thirdBase")
        diamond.moveBase("firstBase", "secondBase")


    def reachedBase(self, pitcherId, batterId, diamond):
        diamond.reachedBase("firstBase", batterId, pitcherId)


################################################################################
################################################################################


class SecondThirdGroundOut(StateTicket):

    def recordOuts(self, umpire):
        umpire.recordOut()


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordPitcherOut(pitcherId)
        scoreKeeper.recordBatterAB(batterId)
        runnerId, onHook = diamond.popBase("thirdBase")
        if umpire.getOuts() < 3:
            scoreKeeper.recordTeamRun()
            scoreKeeper.recordBatterRun(runnerId)
            scoreKeeper.recordBatterRbi(batterId)
            scoreKeeper.recordRun(pitcherId)
        if scoreKeeper.exOuts() < 3:
            scoreKeeper.recordPitcherER(pitcherId)


    def moveBases(self, diamond):
        diamond.moveBase("secondBase", "thirdBase")


    def reachedBase(self, pitcherId, batterId, diamond):
        pass


################################################################################
################################################################################


class FirstThirdGroundOut(StateTicket):

    def recordOuts(self, umpire):
        umpire.recordOut()


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordPitcherOut(pitcherId)
        scoreKeeper.recordBatterAB(batterId)
        runnerId, onHook = diamond.popBase("thirdBase")
        if umpire.getOuts() < 3:
            scoreKeeper.recordTeamRun()
            scoreKeeper.recordBatterRun(runnerId)
            scoreKeeper.recordBatterRbi(batterId)
            scoreKeeper.recordRun(pitcherId)
        if scoreKeeper.exOuts() < 3:
            scoreKeeper.recordPitcherER(pitcherId)


    def moveBases(self, diamond):
        # PlayerOut from first to second
        diamond.popBase("firstBase")


    def reachedBase(self, pitcherId, batterId, diamond):
        diamond.reachedBase("firstBase", batterId, pitcherId)


################################################################################
################################################################################


class FirstSecondGroundOut(StateTicket):

    def recordOuts(self, umpire):
        umpire.recordOut()


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordPitcherOut(pitcherId)
        scoreKeeper.recordBatterAB(batterId)


    def moveBases(self, diamond):
        # PlayerOut from second to third
        diamond.popBase("secondBase")
        diamond.moveBase("firstBase", "secondBase")


    def reachedBase(self, pitcherId, batterId, diamond):
        diamond.reachedBase("firstBase", batterId, pitcherId)


################################################################################
################################################################################


class ThirdGroundOut(StateTicket):

    def recordOuts(self, umpire):
        umpire.recordOut()


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordPitcherOut(pitcherId)
        scoreKeeper.recordBatterAB(batterId)
        runnerId, onHook = diamond.popBase("thirdBase")
        if umpire.getOuts() < 3:
            scoreKeeper.recordTeamRun()
            scoreKeeper.recordBatterRun(runnerId)
            scoreKeeper.recordBatterRbi(batterId)
            scoreKeeper.recordRun(onHook)
        if scoreKeeper.exOuts() < 3:
            scoreKeeper.recordPitcherER(onHook)


    def moveBases(self, diamond):
        pass


    def reachedBase(self, pitcherId, batterId, diamond):
        pass


################################################################################
################################################################################


class SecondGroundOut(StateTicket):

    def recordOuts(self, umpire):
        umpire.recordOut()


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordPitcherOut(pitcherId)
        scoreKeeper.recordBatterAB(batterId)


    def moveBases(self, diamond):
        diamond.moveBase("secondBase", "thirdBase")


    def reachedBase(self, pitcherId, batterId, diamond):
        pass


################################################################################
################################################################################


class FirstGroundOut(StateTicket):

    def recordOuts(self, umpire):
        umpire.recordOut()


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordPitcherOut(pitcherId)
        scoreKeeper.recordBatterAB(batterId)


    def moveBases(self, diamond):
        # Out going from first to second
        diamond.popBase("firstBase")


    def reachedBase(self, pitcherId, batterId, diamond):
        diamond.reachedBase("firstBase", batterId, pitcherId)


################################################################################
################################################################################


class EmptyGroundOut(StateTicket):

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
