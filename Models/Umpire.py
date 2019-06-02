from MLBProjections.MLBProjections.Models.ScoreKeeper import ScoreKeeper

import random
import sqlite3
from pprint import pprint

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
        self.inning = 0
        self.stadiumId = self.db.curs.execute("SELECT stadium_id FROM pro_teams WHERE team_id = ?", (self.game.homeTeam.teamId,)).fetchone()[0]

        self.winCase = False

        self.side = None
        self.outs = None
        self.balls = None
        self.strikes = None


    def setInning(self):

        self.side = "away" if (self.side == "home" or not self.side) else "home"

        if self.side == "away":
            self.inning += 1
        if self.inning == 9 and self.side == "home":
            self.winCase = True


    def endInning(self):
        homeScore = self.scoreKeeper.scoreBook.score["home"]
        awayScore = self.scoreKeeper.scoreBook.score["away"]
        gameOver = False

        if self.winCase and self.side == "home":
                gameOver = True if homeScore > awayScore else False

        return gameOver


    def endGame(self):
        homeScore = self.scoreKeeper.scoreBook.score["home"]
        awayScore = self.scoreKeeper.scoreBook.score["away"]
        gameOver = False

        if self.winCase:
            if self.side == "home":
                gameOver = True if homeScore > awayScore else False
            else:
                gameOver = True if homeScore != awayScore else False

        return gameOver


    def nextBatter(self):
        return self.scoreKeeper.nextBatter()


    def getPitcher(self):
        side = self.scoreKeeper.scoreBook.fieldingSide
        pitcher = str(self.scoreKeeper.getPitcher())
        stats = self.scoreKeeper.scoreBook.info[side]["p"].get(int(pitcher), None)
        #print(stats)
        if stats:
            total = self.db.curs.execute("SELECT COUNT(pitcher_id) FROM removals WHERE pitcher_id = ?", (pitcher,)).fetchone()[0]
            runRemove = self.db.curs.execute("SELECT COUNT(pitcher_id) FROM removals WHERE pitcher_id = ? AND runs <= ?", (pitcher, stats["R"])).fetchone()[0]
            pitchRemove = self.db.curs.execute("SELECT COUNT(pitcher_id) FROM removals WHERE pitcher_id = ? AND pitch_num <= ?", (pitcher, stats["NUM"])).fetchone()[0]
            #print(total, runRemove, pitchRemove)
            if not total:
                total = 1
                runRemove = 1
                pitchRemove = 1
            if runRemove/total + pitchRemove/total >= 1.15:
                team = self.game.homeTeam if side == "home" else self.game.awayTeam
                bullpen = [x for x in team.bullpen]
                cmd = "SELECT pitcher_id FROM new_pitchers WHERE team_id = ? AND inning <= ? AND pitcher_id in {}".format(str(tuple(bullpen)))
                #pprint(cmd)
                try:
                    results = [x[0] for x in self.db.curs.execute(cmd, (team.teamId, self.inning,)).fetchall()]
                    index = round(random.random() * (len(results)-1))
                    num = results[index]

                except (sqlite3.OperationalError, IndexError):
                    pprint(cmd)
                    num = 0

                newPitcher = None
                for p in team.bullpen:
                    if str(p) == str(num):
                        newPitcher = p
                        break
                if not newPitcher:
                    newPitcher = team.bullpen[0]

                #print(results)
                #print("\n\nLength {}   Index {}".format(len(results), index))
                team.setPitcher(newPitcher)
                self.scoreKeeper.newPitcher(newPitcher)

        return self.scoreKeeper.getPitcher()


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
                tag="Strike Out"
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
