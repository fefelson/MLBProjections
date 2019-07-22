# from pprint import pprint

################################################################################
################################################################################





################################################################################
################################################################################


class Umpire:

    def __init__(self, scoreKeeper):

        self.scoreKeeper = scoreKeeper

        self.winCase = False
        self.inning = 0
        self.side = None
        self.outs = None
        self.balls = None
        self.strikes = None


    def getInning(self):
        return self.inning


    def recordPitchResult(self, result):
        abResult = None
        if result == 0:
            self.addBall()
        elif result in (1,2,3):
            self.addStrike()
        elif result == 3 and self.strikes <2:
            self.addStrike()

        if self.balls == 4:
            abResult = "Walk"
        if self.strikes ==3:
            abResult = "Strike Out"
        return abResult




    def setInning(self):
        self.side = "away" if (self.side == "home" or not self.side) else "home"
        if self.side == "away":
            self.inning += 1
        if self.inning == 9 and self.side == "home":
            self.winCase = True


    def endInning(self):
        return self.outs >= 3 or self.endGame()


    def endGame(self,):
        homeScore = self.scoreKeeper.getScore()["home"]
        awayScore = self.scoreKeeper.getScore()["away"]
        gameOver = False
        if self.winCase and self.side == "home":
                gameOver = True if homeScore > awayScore else False
        return gameOver


    def clearOuts(self):
        self.outs = 0


    def recordOut(self):
        self.outs += 1


    def setSide(self, side):
        self.side = side


    def getCount(self):
        return (self.balls, self.strikes)


    def getOuts(self):
        return self.outs


    def addStrike(self):
        self.strikes += 1


    def addBall(self):
        self.balls += 1


    def resetCount(self):
        """
        resetCount is called by an Umpire to initialize balls and strikes
        """
        self.balls = 0
        self.strikes = 0


################################################################################
################################################################################
