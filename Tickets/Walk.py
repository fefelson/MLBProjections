from .Ticket import Ticket, StateTicket

################################################################################
################################################################################





################################################################################
################################################################################


class Walk(Ticket):

    def getStateTicket(self, diamondState):
        stateTicket = None
        if diamondState == "firstBase_secondBase_thirdBase":
            stateTicket = BasesLoadedWalk()
        elif diamondState == "firstBase_thirdBase":
            stateTicket = FirstThirdWalk()
        elif diamondState == "firstBase_secondBase":
            stateTicket = FirstSecondWalk()
        elif diamondState == "firstBase":
            stateTicket = FirstWalk()
        else: #Bases Empty
            stateTicket = WalkState()
        return stateTicket


################################################################################
################################################################################


class BasesLoadedWalk(StateTicket):

    def recordOuts(self, umpire):
        pass


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordBatterBB(batterId)
        scoreKeeper.recordPitcherBB(pitcherId)
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
        diamond.moveBase("secondBase", "thirdBase")
        diamond.moveBase("firstBase", "secondBase")


    def reachedBase(self, pitcherId, batterId, diamond):
        diamond.reachedBase("firstBase", batterId, pitcherId)


################################################################################
################################################################################


class FirstThirdWalk(StateTicket):

    def recordOuts(self, umpire):
        pass


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordBatterBB(batterId)
        scoreKeeper.recordPitcherBB(pitcherId)


    def moveBases(self, diamond):
        diamond.moveBase("firstBase", "secondBase")


    def reachedBase(self, pitcherId, batterId, diamond):
        diamond.reachedBase("firstBase", batterId, pitcherId)


################################################################################
################################################################################


class FirstSecondWalk(StateTicket):

    def recordOuts(self, umpire):
        pass


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordBatterBB(batterId)
        scoreKeeper.recordPitcherBB(pitcherId)


    def moveBases(self, diamond):
        diamond.moveBase("secondBase", "thirdBase")
        diamond.moveBase("firstBase", "secondBase")


    def reachedBase(self, pitcherId, batterId, diamond):
        diamond.reachedBase("firstBase", batterId, pitcherId)

################################################################################
################################################################################


class FirstWalk(StateTicket):

    def recordOuts(self, umpire):
        pass


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordBatterBB(batterId)
        scoreKeeper.recordPitcherBB(pitcherId)


    def moveBases(self, diamond):
        diamond.moveBase("firstBase", "secondBase")


    def reachedBase(self, pitcherId, batterId, diamond):
        diamond.reachedBase("firstBase", batterId, pitcherId)


################################################################################
################################################################################


class WalkState(StateTicket):

    def recordOuts(self, umpire):
        pass


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordBatterBB(batterId)
        scoreKeeper.recordPitcherBB(pitcherId)



    def moveBases(self, diamond):
        pass


    def reachedBase(self, pitcherId, batterId, diamond):
        diamond.reachedBase("firstBase", batterId, pitcherId)


################################################################################
################################################################################
