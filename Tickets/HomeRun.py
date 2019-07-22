from .Ticket import Ticket, StateTicket

################################################################################
################################################################################





################################################################################
################################################################################


class HomeRun(Ticket):

    def getStateTicket(self, diamondState):
        stateTicket = None
        if diamondState == "firstBase_secondBase_thirdBase":
            stateTicket = BasesLoadedHomeRun()
        elif diamondState == "secondBase_thirdBase":
            stateTicket = SecondThirdHomeRun()
        elif diamondState == "firstBase_thirdBase":
            stateTicket = FirstThirdHomeRun()
        elif diamondState == "firstBase_secondBase":
            stateTicket = FirstSecondHomeRun()
        elif diamondState == "thirdBase":
            stateTicket = ThirdHomeRun()
        elif diamondState == "secondBase":
            stateTicket = SecondHomeRun()
        elif diamondState == "firstBase":
            stateTicket = FirstHomeRun()
        else: #Bases Empty
            stateTicket = EmptyHomeRun()
        return stateTicket


################################################################################
################################################################################


class BasesLoadedHomeRun(StateTicket):

    def recordOuts(self, umpire):
        pass


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordTeamRun()
        scoreKeeper.recordBatterHR(batterId)
        scoreKeeper.recordPitcherH(pitcherId)
        scoreKeeper.recordBatterRun(runnerId)
        scoreKeeper.recordBatterRbi(batterId)
        scoreKeeper.recordPitcherRun(pitcherId)
        if scoreKeeper.exOuts() < 3:
            scoreKeeper.recordPitcherER(pitcherId)
        # Runners on second and third score
        for base in ("thirdBase", "secondBase", "firstBase"):
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
        pass


################################################################################
################################################################################


class SecondThirdHomeRun(StateTicket):

    def recordOuts(self, umpire):
        pass


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordTeamRun()
        scoreKeeper.recordBatterHR(batterId)
        scoreKeeper.recordPitcherH(pitcherId)
        scoreKeeper.recordBatterRun(runnerId)
        scoreKeeper.recordBatterRbi(batterId)
        scoreKeeper.recordPitcherRun(pitcherId)
        if scoreKeeper.exOuts() < 3:
            scoreKeeper.recordPitcherER(pitcherId)
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
        pass


################################################################################
################################################################################


class FirstThirdHomeRun(StateTicket):

    def recordOuts(self, umpire):
        pass


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordTeamRun()
        scoreKeeper.recordBatterHR(batterId)
        scoreKeeper.recordPitcherH(pitcherId)
        scoreKeeper.recordBatterRun(runnerId)
        scoreKeeper.recordBatterRbi(batterId)
        scoreKeeper.recordPitcherRun(pitcherId)
        if scoreKeeper.exOuts() < 3:
            scoreKeeper.recordPitcherER(pitcherId)
        # Runners on second and third score
        for base in ("thirdBase", "firstBase"):
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
        pass


################################################################################
################################################################################


class FirstSecondHomeRun(StateTicket):

    def recordOuts(self, umpire):
        pass


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordTeamRun()
        scoreKeeper.recordBatterHR(batterId)
        scoreKeeper.recordPitcherH(pitcherId)
        scoreKeeper.recordBatterRun(runnerId)
        scoreKeeper.recordBatterRbi(batterId)
        scoreKeeper.recordPitcherRun(pitcherId)
        if scoreKeeper.exOuts() < 3:
            scoreKeeper.recordPitcherER(pitcherId)
        # Runners on second and third score
        for base in ("secondBase", "firstBase"):
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
        pass


################################################################################
################################################################################


class ThirdHomeRun(StateTicket):

    def recordOuts(self, umpire):
        pass


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordTeamRun()
        scoreKeeper.recordBatterHR(batterId)
        scoreKeeper.recordPitcherH(pitcherId)
        scoreKeeper.recordBatterRun(runnerId)
        scoreKeeper.recordBatterRbi(batterId)
        scoreKeeper.recordPitcherRun(pitcherId)
        if scoreKeeper.exOuts() < 3:
            scoreKeeper.recordPitcherER(pitcherId)
        # Runners on second and third score
        for base in ("thirdBase",):
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
        pass


################################################################################
################################################################################


class SecondHomeRun(StateTicket):

    def recordOuts(self, umpire):
        pass


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordTeamRun()
        scoreKeeper.recordBatterHR(batterId)
        scoreKeeper.recordPitcherH(pitcherId)
        scoreKeeper.recordBatterRun(runnerId)
        scoreKeeper.recordBatterRbi(batterId)
        scoreKeeper.recordPitcherRun(pitcherId)
        if scoreKeeper.exOuts() < 3:
            scoreKeeper.recordPitcherER(pitcherId)
        # Runners on second and third score
        for base in ("secondBase", ):
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
        pass


################################################################################
################################################################################


class FirstHomeRun(StateTicket):

    def recordOuts(self, umpire):
        pass


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordTeamRun()
        scoreKeeper.recordBatterHR(batterId)
        scoreKeeper.recordPitcherH(pitcherId)
        scoreKeeper.recordBatterRun(runnerId)
        scoreKeeper.recordBatterRbi(batterId)
        scoreKeeper.recordPitcherRun(pitcherId)
        if scoreKeeper.exOuts() < 3:
            scoreKeeper.recordPitcherER(pitcherId)
        # Runners on second and third score
        for base in ("firstBase", ):
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
        pass


################################################################################
################################################################################


class EmptyHomeRun(StateTicket):

    def recordOuts(self, umpire):
        pass


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordTeamRun()
        scoreKeeper.recordBatterHR(batterId)
        scoreKeeper.recordPitcherH(pitcherId)
        scoreKeeper.recordBatterRun(runnerId)
        scoreKeeper.recordBatterRbi(batterId)
        scoreKeeper.recordPitcherRun(pitcherId)
        if scoreKeeper.exOuts() < 3:
            scoreKeeper.recordPitcherER(pitcherId)


    def moveBases(self, diamond):
        pass


    def reachedBase(self, pitcherId, batterId, diamond):
        pass

################################################################################
################################################################################
