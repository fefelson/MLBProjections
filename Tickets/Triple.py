from .Ticket import Ticket, StateTicket

################################################################################
################################################################################





################################################################################
################################################################################


class Triple(Ticket):

    def getStateTicket(self, diamondState):
        stateTicket = None
        if diamondState == "firstBase_secondBase_thirdBase":
            stateTicket = BasesLoadedTriple()
        elif diamondState == "secondBase_thirdBase":
            stateTicket = SecondThirdTriple()
        elif diamondState == "firstBase_thirdBase":
            stateTicket = FirstThirdTriple()
        elif diamondState == "firstBase_secondBase":
            stateTicket = FirstSecondTriple()
        elif diamondState == "thirdBase":
            stateTicket = ThirdTriple()
        elif diamondState == "secondBase":
            stateTicket = SecondTriple()
        elif diamondState == "firstBase":
            stateTicket = FirstTriple()
        else: #Bases Empty
            stateTicket = EmptyTriple()
        return stateTicket


################################################################################
################################################################################


class BasesLoadedTriple(StateTicket):

    def recordOuts(self, umpire):
        pass


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordBatter3B(batterId)
        scoreKeeper.recordPitcherH(pitcherId)
        # Runners on second and third score
        for base in ("thirdBase", "secondBase", "firstBase"):
            runnerId, onHook = diamond.popBase(base)
            scoreKeeper.recordTeamRun()
            scoreKeeper.recordBatterRun(runnerId)
            scoreKeeper.recordBatterRbi(batterId)
            scoreKeeper.recordRun(onHook)
            if scoreKeeper.exOuts() < 3:
                scoreKeeper.recordPitcherER(onHook)


    def moveBases(self, diamond):
        pass


    def reachedBase(self, pitcherId, batterId, diamond):
        diamond.reachedBase("thirdBase", batterId, pitcherId)


################################################################################
################################################################################


class SecondThirdTriple(StateTicket):

    def recordOuts(self, umpire):
        pass


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordBatter3B(batterId)
        scoreKeeper.recordPitcherH(pitcherId)
        # Runners on second and third score
        for base in ("thirdBase", "secondBase"):
            runnerId, onHook = diamond.popBase(base)
            scoreKeeper.recordTeamRun()
            scoreKeeper.recordBatterRun(runnerId)
            scoreKeeper.recordBatterRbi(batterId)
            scoreKeeper.recordRun(onHook)
            if scoreKeeper.exOuts() < 3:
                scoreKeeper.recordPitcherER(onHook)


    def moveBases(self, diamond):
        pass


    def reachedBase(self, pitcherId, batterId, diamond):
        diamond.reachedBase("thirdBase", batterId, pitcherId)


################################################################################
################################################################################


class FirstThirdTriple(StateTicket):

    def recordOuts(self, umpire):
        pass


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordBatter3B(batterId)
        scoreKeeper.recordPitcherH(pitcherId)
        # Runners on second and third score
        for base in ("thirdBase", "firstBase"):
            runnerId, onHook = diamond.popBase(base)
            scoreKeeper.recordTeamRun()
            scoreKeeper.recordBatterRun(runnerId)
            scoreKeeper.recordBatterRbi(batterId)
            scoreKeeper.recordRun(onHook)
            if scoreKeeper.exOuts() < 3:
                scoreKeeper.recordPitcherER(onHook)

    def moveBases(self, diamond):
        pass


    def reachedBase(self, pitcherId, batterId, diamond):
        diamond.reachedBase("thirdBase", batterId, pitcherId)


################################################################################
################################################################################


class FirstSecondTriple(StateTicket):

    def recordOuts(self, umpire):
        pass


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordBatter3B(batterId)
        scoreKeeper.recordPitcherH(pitcherId)
        # Runners on second and third score
        for base in ("secondBase", "firstBase"):
            runnerId, onHook = diamond.popBase(base)
            scoreKeeper.recordTeamRun()
            scoreKeeper.recordBatterRun(runnerId)
            scoreKeeper.recordBatterRbi(batterId)
            scoreKeeper.recordRun(onHook)
            if scoreKeeper.exOuts() < 3:
                scoreKeeper.recordPitcherER(onHook)


    def moveBases(self, diamond):
        pass


    def reachedBase(self, pitcherId, batterId, diamond):
        diamond.reachedBase("thirdBase", batterId, pitcherId)


################################################################################
################################################################################


class ThirdTriple(StateTicket):

    def recordOuts(self, umpire):
        pass


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordBatter3B(batterId)
        scoreKeeper.recordPitcherH(pitcherId)
        # Runners on second and third score
        runnerId, onHook = diamond.popBase("thirdBase")
        scoreKeeper.recordTeamRun()
        scoreKeeper.recordBatterRun(runnerId)
        scoreKeeper.recordBatterRbi(batterId)
        scoreKeeper.recordRun(onHook)
        if scoreKeeper.exOuts() < 3:
            scoreKeeper.recordPitcherER(onHook)


    def moveBases(self, diamond):
        pass


    def reachedBase(self, pitcherId, batterId, diamond):
        diamond.reachedBase("thirdBase", batterId, pitcherId)


################################################################################
################################################################################


class SecondTriple(StateTicket):

    def recordOuts(self, umpire):
        pass


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordBatter3B(batterId)
        scoreKeeper.recordPitcherH(pitcherId)
        # Runners on second and third score
        runnerId, onHook = diamond.popBase("secondBase")
        scoreKeeper.recordTeamRun()
        scoreKeeper.recordBatterRun(runnerId)
        scoreKeeper.recordBatterRbi(batterId)
        scoreKeeper.recordRun(onHook)
        if scoreKeeper.exOuts() < 3:
            scoreKeeper.recordPitcherER(onHook)


    def moveBases(self, diamond):
        pass


    def reachedBase(self, pitcherId, batterId, diamond):
        diamond.reachedBase("thirdBase", batterId, pitcherId)


################################################################################
################################################################################


class FirstTriple(StateTicket):

    def recordOuts(self, umpire):
        pass


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordBatter2B(batterId)
        scoreKeeper.recordPitcherH(pitcherId)

        runnerId, onHook = diamond.popBase("firstBase")
        scoreKeeper.recordTeamRun()
        scoreKeeper.recordBatterRun(runnerId)
        scoreKeeper.recordBatterRbi(batterId)
        scoreKeeper.recordPitcherRun(onHook)
        if scoreKeeper.exOuts() < 3:
            scoreKeeper.recordPitcherER(onHook)


    def moveBases(self, diamond):
        pass


    def reachedBase(self, pitcherId, batterId, diamond):
        diamond.reachedBase("thirdBase", batterId, pitcherId)


################################################################################
################################################################################


class EmptyTriple(StateTicket):

    def recordOuts(self, umpire):
        pass


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordBatter3B(batterId)
        scoreKeeper.recordPitcherH(pitcherId)


    def moveBases(self, diamond):
        pass


    def reachedBase(self, pitcherId, batterId, diamond):
        diamond.reachedBase("thirdBase", batterId, pitcherId)


################################################################################
################################################################################
