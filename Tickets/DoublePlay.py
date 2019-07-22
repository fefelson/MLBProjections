from .Ticket import Ticket, StateTicket

################################################################################
################################################################################





################################################################################
################################################################################


class DoublePlay(Ticket):

    def getStateTicket(self, diamondState):
        stateTicket = None
        if diamondState == "firstBase_secondBase_thirdBase":
            stateTicket = BasesLoadedDoublePlay()
        elif diamondState == "secondBase_thirdBase":
            stateTicket = SecondThirdDoublePlay()
        elif diamondState == "firstBase_thirdBase":
            stateTicket = FirstThirdDoublePlay()
        elif diamondState == "firstBase_secondBase":
            stateTicket = FirstSecondDoublePlay()
        elif diamondState == "thirdBase":
            stateTicket = ThirdDoublePlay()
        elif diamondState == "secondBase":
            stateTicket = SecondDoublePlay()
        elif diamondState == "firstBase":
            stateTicket = FirstDoublePlay()
        else: #Bases Empty
            stateTicket = EmptyDoublePlay()
        return stateTicket


################################################################################
################################################################################


class BasesLoadedDoublePlay(StateTicket):

    def recordOuts(self, umpire):
        umpire.recordOut()
        if umpire.getOuts() < 3:
            umpire.recordOut()


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordPitcherOut(pitcherId)
        scoreKeeper.recordBatterAB(batterId)
        if umpire.getOuts() < 3:
            scoreKeeper.recordPitcherOut(pitcherId)


    def moveBases(self, diamond):
        # Runner out advancing Home
        diamond.popBase("thirdBase")
        diamond.moveBase("secondBase", "thirdBase")
        diamond.moveBase("firstBase", "secondBase")


    def reachedBase(self, pitcherId, batterId, diamond):
        pass


################################################################################
################################################################################


class SecondThirdDoublePlay(StateTicket):

    def recordOuts(self, umpire):
        umpire.recordOut()
        if umpire.getOuts() < 3:
            umpire.recordOut()


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordPitcherOut(pitcherId)
        scoreKeeper.recordBatterAB(batterId)
        if umpire.getOuts() < 3:
            scoreKeeper.recordPitcherOut(pitcherId)


    def moveBases(self, diamond):
        # Runner out advancing Home
        diamond.popBase("thirdBase")
        diamond.moveBase("secondBase", "thirdBase")


    def reachedBase(self, pitcherId, batterId, diamond):
        pass


################################################################################
################################################################################


class FirstThirdDoublePlay(StateTicket):

    def recordOuts(self, umpire):
        umpire.recordOut()
        if umpire.getOuts() < 3:
            umpire.recordOut()


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordPitcherOut(pitcherId)
        scoreKeeper.recordBatterAB(batterId)
        if umpire.getOuts() < 3:
            scoreKeeper.recordPitcherOut(pitcherId)


    def moveBases(self, diamond):
        # Runner out advancing Home
        diamond.popBase("thirdBase")
        diamond.moveBase("firstBase", "secondBase")


    def reachedBase(self, pitcherId, batterId, diamond):
        pass


################################################################################
################################################################################


class FirstSecondDoublePlay(StateTicket):

    def recordOuts(self, umpire):
        umpire.recordOut()
        if umpire.getOuts() < 3:
            umpire.recordOut()


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordPitcherOut(pitcherId)
        scoreKeeper.recordBatterAB(batterId)
        if umpire.getOuts() < 3:
            scoreKeeper.recordPitcherOut(pitcherId)


    def moveBases(self, diamond):
        # Runner out advancing Home
        diamond.popBase("secondBase")
        diamond.moveBase("firstBase", "secondBase")


    def reachedBase(self, pitcherId, batterId, diamond):
        pass


################################################################################
################################################################################


class ThirdDoublePlay(StateTicket):

    def recordOuts(self, umpire):
        umpire.recordOut()
        if umpire.getOuts() < 3:
            umpire.recordOut()


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordPitcherOut(pitcherId)
        scoreKeeper.recordBatterAB(batterId)
        if umpire.getOuts() < 3:
            scoreKeeper.recordPitcherOut(pitcherId)


    def moveBases(self, diamond):
        # Runner out advancing Home
        diamond.popBase("thirdBase")


    def reachedBase(self, pitcherId, batterId, diamond):
        pass


################################################################################
################################################################################


class SecondDoublePlay(StateTicket):

    def recordOuts(self, umpire):
        umpire.recordOut()
        if umpire.getOuts() < 3:
            umpire.recordOut()


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordPitcherOut(pitcherId)
        scoreKeeper.recordBatterAB(batterId)
        if umpire.getOuts() < 3:
            scoreKeeper.recordPitcherOut(pitcherId)


    def moveBases(self, diamond):
        # Runner out advancing Home
        diamond.popBase("secondBase")


    def reachedBase(self, pitcherId, batterId, diamond):
        pass


################################################################################
################################################################################


class FirstDoublePlay(StateTicket):

    def recordOuts(self, umpire):
        umpire.recordOut()
        if umpire.getOuts() < 3:
            umpire.recordOut()


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordPitcherOut(pitcherId)
        scoreKeeper.recordBatterAB(batterId)
        if umpire.getOuts() < 3:
            scoreKeeper.recordPitcherOut(pitcherId)


    def moveBases(self, diamond):
        # Runner out advancing Home
        diamond.popBase("firstBase")


    def reachedBase(self, pitcherId, batterId, diamond):
        pass


################################################################################
################################################################################


class EmptyDoublePlay(StateTicket):

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
