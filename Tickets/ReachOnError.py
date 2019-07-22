from .Ticket import Ticket, StateTicket

################################################################################
################################################################################


unEarn = -20


################################################################################
################################################################################


class ReachOnError(Ticket):

    def getStateTicket(self, diamondState):
        stateTicket = None
        if diamondState == "firstBase_secondBase_thirdBase":
            stateTicket = BasesLoadedReachOnError()
        elif diamondState == "secondBase_thirdBase":
            stateTicket = SecondThirdReachOnError()
        elif diamondState == "firstBase_thirdBase":
            stateTicket = FirstThirdReachOnError()
        elif diamondState == "firstBase_secondBase":
            stateTicket = FirstSecondReachOnError()
        elif diamondState == "thirdBase":
            stateTicket = ThirdReachOnError()
        elif diamondState == "secondBase":
            stateTicket = SecondReachOnError()
        elif diamondState == "firstBase":
            stateTicket = FirstReachOnError()
        else: #Bases Empty
            stateTicket = EmptyReachOnError()
        return stateTicket


################################################################################
################################################################################


class BasesLoadedReachOnError(StateTicket):

    def recordOuts(self, umpire):
        pass


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordBatterAB(batterId)
        scoreKeeper.addExOut()
        # Runners on second and third score
        for base in ("thirdBase", ):
            runnerId, _ = diamond.popBase(base)
            scoreKeeper.recordTeamRun()
            scoreKeeper.recordBatterRun(runnerId)
            scoreKeeper.recordBatterRbi(batterId)
            scoreKeeper.recordPitcherRun(unEarn)


    def moveBases(self, diamond):
        diamond.moveBase("secondBase", "thirdBase")
        diamond.moveBase("firstBase", "secondBase")


    def reachedBase(self, pitcherId, batterId, diamond):
        diamond.reachedBase("firstBase", batterId, unEarn)


################################################################################
################################################################################


class SecondThirdReachOnError(StateTicket):

    def recordOuts(self, umpire):
        pass


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordBatterAB(batterId)
        scoreKeeper.addExOut()
        # Runners on second and third score
        for base in ("thirdBase", ):
            runnerId, _ = diamond.popBase(base)
            scoreKeeper.recordTeamRun()
            scoreKeeper.recordBatterRun(runnerId)
            scoreKeeper.recordBatterRbi(batterId)
            scoreKeeper.recordPitcherRun(unEarn)


    def moveBases(self, diamond):
        diamond.moveBase("secondBase", "thirdBase")


    def reachedBase(self, pitcherId, batterId, diamond):
        diamond.reachedBase("firstBase", batterId, unEarn)


################################################################################
################################################################################


class FirstThirdReachOnError(StateTicket):

    def recordOuts(self, umpire):
        pass


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordBatterAB(batterId)
        scoreKeeper.addExOut()
        # Runners on second and third score
        for base in ("thirdBase", ):
            runnerId, _ = diamond.popBase(base)
            scoreKeeper.recordTeamRun()
            scoreKeeper.recordBatterRun(runnerId)
            scoreKeeper.recordBatterRbi(batterId)
            scoreKeeper.recordPitcherRun(unEarn)


    def moveBases(self, diamond):
        diamond.moveBase("firstBase", "secondBase")


    def reachedBase(self, pitcherId, batterId, diamond):
        diamond.reachedBase("firstBase", batterId, unEarn)


################################################################################
################################################################################


class FirstSecondReachOnError(StateTicket):

    def recordOuts(self, umpire):
        pass


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordBatterAB(batterId)
        scoreKeeper.addExOut()


    def moveBases(self, diamond):
        diamond.moveBase("secondBase", "thirdBase")
        diamond.moveBase("firstBase", "secondBase")


    def reachedBase(self, pitcherId, batterId, diamond):
        diamond.reachedBase("firstBase", batterId, unEarn)


################################################################################
################################################################################


class ThirdReachOnError(StateTicket):

    def recordOuts(self, umpire):
        pass


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordBatterAB(batterId)
        scoreKeeper.addExOut()
        # Runners on second and third score
        for base in ("thirdBase", ):
            runnerId, _ = diamond.popBase(base)
            scoreKeeper.recordTeamRun()
            scoreKeeper.recordBatterRun(runnerId)
            scoreKeeper.recordBatterRbi(batterId)
            scoreKeeper.recordPitcherRun(unEarn)


    def moveBases(self, diamond):
        pass


    def reachedBase(self, pitcherId, batterId, diamond):
        diamond.reachedBase("firstBase", batterId, unEarn)


################################################################################
################################################################################


class SecondReachOnError(StateTicket):

    def recordOuts(self, umpire):
        pass


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordBatterAB(batterId)
        scoreKeeper.addExOut()


    def moveBases(self, diamond):
        diamond.moveBase("secondBase", "thirdBase")


    def reachedBase(self, pitcherId, batterId, diamond):
        diamond.reachedBase("firstBase", batterId, unEarn)


################################################################################
################################################################################


class FirstReachOnError(StateTicket):

    def recordOuts(self, umpire):
        pass


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordBatterAB(batterId)
        scoreKeeper.addExOut()


    def moveBases(self, diamond):
        diamond.moveBase("firstBase", "secondBase")


    def reachedBase(self, pitcherId, batterId, diamond):
        diamond.reachedBase("firstBase", batterId, unEarn)


################################################################################
################################################################################


class EmptyReachOnError(StateTicket):

    def recordOuts(self, umpire):
        pass


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordBatterAB(batterId)
        scoreKeeper.addExOut()


    def moveBases(self, diamond):
        pass


    def reachedBase(self, pitcherId, batterId, diamond):
        diamond.reachedBase("firstBase", batterId, unEarn)


################################################################################
################################################################################
