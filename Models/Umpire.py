from MLBProjections.MLBProjections.Models.ScoreKeeper import ScoreKeeper

################################################################################
################################################################################





################################################################################
################################################################################


class Umpire:
    """
    Umpire is the DungeonMaster.  It assesses variables and rolls the dice to determine
    outcomes.
    """

    def __init__(self, game):

        self.game = game
        self.db = game.db
        self.scoreKeeper = ScoreKeeper(game)

        self.side = None
        self.outs = None
        self.balls = None
        self.strikes = None


    def endInning(self, winCase, side):
        homeScore = self.scoreKeeper.scoreBook.score["home"]
        awayScore = self.scoreKeeper.scoreBook.score["away"]
        gameOver = False

        if winCase and side == "home":
                gameOver = True if homeScore > awayScore else False

        return gameOver


    def endGame(self, winCase, side):
        homeScore = self.scoreKeeper.scoreBook.score["home"]
        awayScore = self.scoreKeeper.scoreBook.score["away"]
        gameOver = False

        if winCase:
            if side == "home":
                gameOver = True if homeScore > awayScore else False
            else:
                gameOver = True if homeScore != awayScore else False

        return gameOver


    def clearOuts(self):
        self.outs = 0


    def recordOut(self):
        self.outs += 1


    def recordRun(self):
        self.scoreKeeper.addRun()


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


    def pitchRuling(self, pitchResult, hitResult=None):
        outcome = False
        tag = hitResult
        # In Play
        if pitchResult == 10:
            outcome = True
        # Ball
        elif pitchResult == 0:
            self.addBall()
            if self.balls == 4:
                outcome = True
                tag="Walk"
        # Called Strike, Swinging Strike
        elif pitchResult in (1,2):
            self.addStrike()
            if self.strikes == 3:
                outcome = True
                tag="Strikeout"
        # Foul Ball
        elif pitchResult == 3:
            if self.strikes <2:
                self.addStrike()
        # Foul Bunt
        elif pitchResult == 5:
            if self.strikes <2:
                self.addStrike()
            else:
                outcome = True
                #Bunt Out
                tag="Out"
        return outcome, tag


################################################################################
################################################################################
