from .Ticket import Ticket, StateTicket

################################################################################
################################################################################





################################################################################
################################################################################


class Double(Ticket):

    def getStateTicket(self, diamondState):
        stateTicket = None
        if diamondState == "firstBase_secondBase_thirdBase":
            stateTicket = BasesLoadedDouble()
        elif diamondState == "secondBase_thirdBase":
            stateTicket = SecondThirdDouble()
        elif diamondState == "firstBase_thirdBase":
            stateTicket = FirstThirdDouble()
        elif diamondState == "firstBase_secondBase":
            stateTicket = FirstSecondDouble()
        elif diamondState == "thirdBase":
            stateTicket = ThirdDouble()
        elif diamondState == "secondBase":
            stateTicket = SecondDouble()
        elif diamondState == "firstBase":
            stateTicket = FirstDouble()
        else: #Bases Empty
            stateTicket = EmptyDouble()
        return stateTicket


################################################################################
################################################################################


class BasesLoadedDouble(StateTicket):

    def recordOuts(self, umpire):
        pass


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordBatter2B(batterId)
        scoreKeeper.recordPitcherH(pitcherId)
        # Runners on second and third score
        for base in ("thirdBase", "secondBase"):
            runnerId, onHook = diamond.popBase(base)
            scoreKeeper.recordTeamRun()
            scoreKeeper.recordBatterRun(runnerId)
            scoreKeeper.recordBatterRbi(batterId)
            scoreKeeper.recordPitcherRun(onHook)
            if scoreKeeper.exOuts() < 3:
                scoreKeeper.recordPitcherER(onHook)


    def moveBases(self, diamond):
        diamond.moveBase("firstBase", "thirdBase")


    def reachedBase(self, pitcherId, batterId, diamond):
        diamond.reachedBase("secondBase", batterId, pitcherId)


################################################################################
################################################################################


class SecondThirdDouble(StateTicket):

    def recordOuts(self, umpire):
        pass


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordBatter2B(batterId)
        scoreKeeper.recordPitcherH(pitcherId)
        # Runners on second and third score
        for base in ("thirdBase", "secondBase"):
            runnerId, onHook = diamond.popBase(base)
            scoreKeeper.recordTeamRun()
            scoreKeeper.recordBatterRun(runnerId)
            scoreKeeper.recordBatterRbi(batterId)
            scoreKeeper.recordPitcherRun(onHook)
            if scoreKeeper.exOuts() < 3:
                scoreKeeper.recordPitcherER(onHook)


    def moveBases(self, diamond):
        pass


    def reachedBase(self, pitcherId, batterId, diamond):
        diamond.reachedBase("secondBase", batterId, pitcherId)


################################################################################
################################################################################


class FirstThirdDouble(StateTicket):

    def recordOuts(self, umpire):
        pass


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordBatter2B(batterId)
        scoreKeeper.recordPitcherH(pitcherId)
        # Runners on second and third score
        runnerId, onHook = diamond.popBase("thirdBase")
        scoreKeeper.recordTeamRun()
        scoreKeeper.recordBatterRun(runnerId)
        scoreKeeper.recordBatterRbi(batterId)
        scoreKeeper.recordPitcherRun(onHook)
        if scoreKeeper.exOuts() < 3:
            scoreKeeper.recordPitcherER(onHook)


    def moveBases(self, diamond):
        diamond.moveBase("firstBase", "thirdBase")


    def reachedBase(self, pitcherId, batterId, diamond):
        diamond.reachedBase("secondBase", batterId, pitcherId)


################################################################################
################################################################################


class FirstSecondDouble(StateTicket):

    def recordOuts(self, umpire):
        pass


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordBatter2B(batterId)
        scoreKeeper.recordPitcherH(pitcherId)
        # Runners on second and third score
        runnerId, onHook = diamond.popBase("secondBase")
        scoreKeeper.recordTeamRun()
        scoreKeeper.recordBatterRun(runnerId)
        scoreKeeper.recordBatterRbi(batterId)
        scoreKeeper.recordPitcherRun(onHook)
        if scoreKeeper.exOuts() < 3:
            scoreKeeper.recordPitcherER(onHook)


    def moveBases(self, diamond):
        diamond.moveBase("firstBase", "thirdBase")


    def reachedBase(self, pitcherId, batterId, diamond):
        diamond.reachedBase("secondBase", batterId, pitcherId)


################################################################################
################################################################################


class ThirdDouble(StateTicket):

    def recordOuts(self, umpire):
        pass


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordBatter2B(batterId)
        scoreKeeper.recordPitcherH(pitcherId)
        # Runners on second and third score
        runnerId, onHook = diamond.popBase("thirdBase")
        scoreKeeper.recordTeamRun()
        scoreKeeper.recordBatterRun(runnerId)
        scoreKeeper.recordBatterRbi(batterId)
        scoreKeeper.recordPitcherRun(onHook)
        if scoreKeeper.exOuts() < 3:
            scoreKeeper.recordPitcherER(onHook)


    def moveBases(self, diamond):
        pass


    def reachedBase(self, pitcherId, batterId, diamond):
        diamond.reachedBase("secondBase", batterId, pitcherId)


################################################################################
################################################################################


class SecondDouble(StateTicket):

    def recordOuts(self, umpire):
        pass


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordBatter2B(batterId)
        scoreKeeper.recordPitcherH(pitcherId)
        # Runners on second and third score
        runnerId, onHook = diamond.popBase("secondBase")
        scoreKeeper.recordTeamRun()
        scoreKeeper.recordBatterRun(runnerId)
        scoreKeeper.recordBatterRbi(batterId)
        scoreKeeper.recordPitcherRun(onHook)
        if scoreKeeper.exOuts() < 3:
            scoreKeeper.recordPitcherER(onHook)


    def moveBases(self, diamond):
        pass


    def reachedBase(self, pitcherId, batterId, diamond):
        diamond.reachedBase("secondBase", batterId, pitcherId)


################################################################################
################################################################################


class FirstDouble(StateTicket):

    def recordOuts(self, umpire):
        pass


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordBatter2B(batterId)
        scoreKeeper.recordPitcherH(pitcherId)


    def moveBases(self, diamond):
        diamond.moveBase("firstBase", "thirdBase")


    def reachedBase(self, pitcherId, batterId, diamond):
        diamond.reachedBase("secondBase", batterId, pitcherId)


################################################################################
################################################################################


class EmptyDouble(StateTicket):

    def recordOuts(self, umpire):
        pass


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordBatter2B(batterId)
        scoreKeeper.recordPitcherH(pitcherId)


    def moveBases(self, diamond):
        pass


    def reachedBase(self, pitcherId, batterId, diamond):
        diamond.reachedBase("secondBase", batterId, pitcherId)


################################################################################
################################################################################
