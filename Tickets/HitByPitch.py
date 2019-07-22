from .Ticket import Ticket, StateTicket

################################################################################
################################################################################





################################################################################
################################################################################


class HitByPitch(Ticket):

    def getStateTicket(self, diamondState):
        stateTicket = None
        if diamondState == "firstBase_secondBase_thirdBase":
            stateTicket = BasesLoadedHitByPitch()
        elif diamondState == "firstBase_thirdBase":
            stateTicket = FirstThirdHitByPitch()
        elif diamondState == "firstBase_secondBase":
            stateTicket = FirstSecondHitByPitch()
        elif diamondState == "firstBase":
            stateTicket = FirstHitByPitch()
        else: #Bases Empty
            stateTicket = HitByPitchState()
        return stateTicket


################################################################################
################################################################################


class BasesLoadedHitByPitch(StateTicket):

    def recordOuts(self, umpire):
        pass


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordBatterHBP(batterId)
        scoreKeeper.recordPitcherHBP(pitcherId)
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


class FirstThirdHitByPitch(StateTicket):

    def recordOuts(self, umpire):
        pass


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordBatterHBP(batterId)
        scoreKeeper.recordPitcherHBP(pitcherId)


    def moveBases(self, diamond):
        diamond.moveBase("firstBase", "secondBase")


    def reachedBase(self, pitcherId, batterId, diamond):
        diamond.reachedBase("firstBase", batterId, pitcherId)


################################################################################
################################################################################


class FirstSecondHitByPitch(StateTicket):

    def recordOuts(self, umpire):
        pass


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordBatterHBP(batterId)
        scoreKeeper.recordPitcherHBP(pitcherId)


    def moveBases(self, diamond):
        diamond.moveBase("secondBase", "thirdBase")
        diamond.moveBase("firstBase", "secondBase")


    def reachedBase(self, pitcherId, batterId, diamond):
        diamond.reachedBase("firstBase", batterId, pitcherId)

################################################################################
################################################################################


class FirstHitByPitch(StateTicket):

    def recordOuts(self, umpire):
        pass


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordBatterHBP(batterId)
        scoreKeeper.recordPitcherHBP(pitcherId)


    def moveBases(self, diamond):
        diamond.moveBase("firstBase", "secondBase")


    def reachedBase(self, pitcherId, batterId, diamond):
        diamond.reachedBase("firstBase", batterId, pitcherId)


################################################################################
################################################################################


class HitByPitchState(StateTicket):

    def recordOuts(self, umpire):
        pass


    def recordEvents(self, pitcherId, batterId, diamond, umpire, scoreKeeper):
        scoreKeeper.recordBatterHBP(batterId)
        scoreKeeper.recordPitcherHBP(pitcherId)



    def moveBases(self, diamond):
        pass


    def reachedBase(self, pitcherId, batterId, diamond):
        diamond.reachedBase("firstBase", batterId, pitcherId)


################################################################################
################################################################################
