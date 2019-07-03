from MLBProjections.MLBProjections.Models.ScoreKeeper import ScoreKeeper
from itertools import chain
from sklearn.naive_bayes import MultinomialNB as MultiReg

import random
import sqlite3
import numpy
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

    def __init__(self, db):

        self.db = db
        self.scoreKeeper = ScoreKeeper(db)
        self.inning = 0
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
        homeScore = self.scoreKeeper.scoreBook.scores["home"]
        awayScore = self.scoreKeeper.scoreBook.scores["away"]
        gameOver = False

        if self.winCase and self.side == "home":
                gameOver = True if homeScore > awayScore else False

        return gameOver


    def endGame(self):
        homeScore = self.scoreKeeper.scoreBook.scores["home"]
        awayScore = self.scoreKeeper.scoreBook.scores["away"]
        gameOver = False

        if self.winCase:
            if self.side == "home":
                gameOver = True if homeScore > awayScore else False
            else:
                gameOver = True if homeScore != awayScore else False

        return gameOver


    def nextBatter(self):
        return self.scoreKeeper.nextBatter()


    def inningCheck(self, teamId, inning):
        return self.db.fetchAll("SELECT pitcher_id, COUNT(pitcher_id) AS appearance FROM new_pitchers WHERE team_id = ? and inning = ? GROUP BY pitcher_id ORDER BY appearance DESC", (teamId, inning))



    def getPitcher(self):
        side = self.scoreKeeper.scoreBook.fieldingSide
        pitcher = self.scoreKeeper.getPitcher()[0]
        stats = self.scoreKeeper.scoreBook.info[side]["p"].get(int(pitcher), None)
        teamId = self.scoreKeeper.scoreBook.teams[side]
        #print(stats)
        if stats:
            inning = self.inning

            num = stats["NUM"]
            r = stats["R"]


            removeNum = self.db.fetchOne("SELECT COUNT(pitcher_id) FROM removals WHERE pitch_num <= ? AND pitcher_id = ?",(num,pitcher))[0]
            removeCount = self.db.fetchOne("SELECT COUNT(pitcher_id) FROM removals WHERE pitcher_id = ?",(pitcher,))[0]
            removeRun = self.db.fetchOne("SELECT COUNT(pitcher_id) FROM removals WHERE runs <= ? AND pitcher_id = ?",(r,pitcher))[0]


            rn = (1+removeNum)/(2+removeCount)
            rr = (1+removeRun)/(2+removeCount)


            if rn*rr > .5:
                newPitcher = None
                if len(self.scoreKeeper.scoreBook.bullpens[side]) > 1:
                    while not newPitcher and inning >1:
                        for playerId in [x[0] for x in self.inningCheck(teamId, inning)]:
                            bullpen = [int(player[0]) for player in self.scoreKeeper.scoreBook.bullpens[side]]
                            if int(playerId) in bullpen:
                                index = bullpen.index(int(playerId))
                                newPitcher = self.scoreKeeper.scoreBook.bullpens[side][index]
                                print(newPitcher)
                                break
                        inning -= 1
                        # if not newPitcher:
                        #     newPitcher = team.bullpen[0]

                        #print(results)
                        #print("\n\nLength {}   Index {}".format(len(results), index))
                    if not newPitcher:
                        newPitcher = self.scoreKeeper.scoreBook.bullpens[side][0]

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
