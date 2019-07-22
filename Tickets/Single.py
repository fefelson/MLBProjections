from .Ticket import Ticket, StateTicket

################################################################################
################################################################################





################################################################################
################################################################################


class Single(Ticket):

    def getStateTicket(self, diamondState):
        stateTicket = None
        if diamondState == "firstBase_secondBase_thirdBase":
            stateTicket = BasesLoadedSingle()
        elif diamondState == "secondBase_thirdBase":
            stateTicket = SecondThirdSingle()
        elif diamondState == "firstBase_thirdBase":
            stateTicket = FirstThirdSingle()
        elif diamondState == "firstBase_secondBase":
            stateTicket = FirstSecondSingle()
        elif diamondState == "thirdBase":
            stateTicket = ThirdSingle()
        elif diamondState == "secondBase":
            stateTicket = SecondSingle()
        elif diamondState == "firstBase":
            stateTicket = FirstSingle()
        else: #Bases Empty
            stateTicket = EmptySingle()
        return stateTicket


################################################################################
################################################################################


class BasesLoadedSingle(StateTicket):

    def recordOuts(self, umpire):
        pass


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordBatterH(batterId)
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
        diamond.moveBase("firstBase", "secondBase")


    def reachedBase(self, pitcherId, batterId, diamond):
        diamond.reachedBase("firstBase", batterId, pitcherId)


################################################################################
################################################################################


class SecondThirdSingle(StateTicket):

    def recordOuts(self, umpire):
        pass


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordBatterH(batterId)
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
        diamond.reachedBase("firstBase", batterId, pitcherId)


################################################################################
################################################################################


class FirstThirdSingle(StateTicket):

    def recordOuts(self, umpire):
        pass


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordBatterH(batterId)
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
        diamond.moveBase("firstBase", "secondBase")


    def reachedBase(self, pitcherId, batterId, diamond):
        diamond.reachedBase("firstBase", batterId, pitcherId)


################################################################################
################################################################################


class FirstSecondSingle(StateTicket):

    def recordOuts(self, umpire):
        pass


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordBatterH(batterId)
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
        diamond.reachedBase("firstBase", batterId, pitcherId)


################################################################################
################################################################################


class ThirdSingle(StateTicket):

    def recordOuts(self, umpire):
        pass


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordBatterH(batterId)
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
        diamond.reachedBase("firstBase", batterId, pitcherId)


################################################################################
################################################################################


class SecondSingle(StateTicket):

    def recordOuts(self, umpire):
        pass


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordBatterH(batterId)
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
        diamond.reachedBase("firstBase", batterId, pitcherId)


################################################################################
################################################################################


class FirstSingle(StateTicket):

    def recordOuts(self, umpire):
        pass


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordBatterH(batterId)
        scoreKeeper.recordPitcherH(pitcherId)


    def moveBases(self, diamond):
        diamond.moveBase("firstBase", "secondBase")


    def reachedBase(self, pitcherId, batterId, diamond):
        diamond.reachedBase("firstBase", batterId, pitcherId)


################################################################################
################################################################################


class EmptySingle(StateTicket):

    def recordOuts(self, umpire):
        pass


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordBatterH(batterId)
        scoreKeeper.recordPitcherH(pitcherId)


    def moveBases(self, diamond):
        pass


    def reachedBase(self, pitcherId, batterId, diamond):
        diamond.reachedBase("firstBase", batterId, pitcherId)


################################################################################
################################################################################
