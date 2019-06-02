import json
import os
import re
import copy

from collections import Counter
from pprint import pprint

################################################################################
################################################################################


playerPattern = re.compile("mlb.p.(?P<playerId>\d*)")
batterPattern = re.compile("^\[(?P<playerId>\d*)\]")
parenPattern = re.compile("\(.*?\)")

outToPattern = re.compile("out to (?P<field>\w*)")
groundOutPattern = re.compile("(?P<throw>\w*) to (?P<field>\w*)")

# In order of most common
batterPatterns = (("Ground Out", re.compile("grounded (bunt |\s?)out")),
                  ("Strike Out", re.compile("struck out")),
                  ("Single", re.compile("singled|reached on an infield single")),
                  ("Fly Out", re.compile("flied out")),
                  ("Walk", re.compile("walked")),
                  ("Line Out", re.compile("lined out")),
                  ("Double", re.compile("doubled|ground rule double")),
                  ("Pop Out", re.compile("popped out")),
                  ("Home Run", re.compile("homered|inside the park home run")),
                  ("Fielder's Choice", re.compile("fielder's choice")),
                  ("Double Play", re.compile("double play")),
                  ("Fouled Out", re.compile("fouled out")),
                  ("Hit by Pitch", re.compile("hit by pitch")),
                  ("Reached on Error", re.compile("reached on 's (fielding|throwing) error")),
                  ("Sacrifice", re.compile("sacrificed|sacrifice fly")),
                  ("Triple", re.compile("tripled")),
                  ("Reached on Interference", re.compile("reached on catcher's interference")),
                  ("Triple Play", re.compile("triple play")),
                  ("Out on Interference", re.compile("out on batter's interference")),
                  ("Out of Order", re.compile("batted out of order")))


runnerPatterns = (("Stolen Base", re.compile("stole")),
                  ("Wild Pitch", re.compile("wild pitch")),
                  ("Caught Stealing", re.compile("caught stealing")),
                  ("Passed Ball", re.compile("passed ball")),
                  ("Fielder's Indifference", re.compile("fielder's indifference")),
                  ("Picked Off", re.compile("picked off")),
                  ("Advanced on Error", re.compile("(fielding|throwing) error")),
                  ("Balk", re.compile("balk")),
                  ("Out Advancing", re.compile("out advancing on throw")))


managerPatterns = (("Pitching Change", re.compile("pitching")),
                   ("Fielding Change", re.compile("(catching|first|second|third|shortstop|left|right|center|designated)")),
                   ("Pinch Hitter", re.compile("pinch hitter")),
                   ("Pinch Runner", re.compile("pinch runner")))


positions = {"pitcher":1, "catcher":2, "first":3, "second":4, "third":5,
             "shortstop":6, "left":7, "center":8, "right":9}



def searchAction(text, patterns):
    # Default if no matches
    resultLabel = "Label Error"
    for label, pattern in patterns:
        if pattern.search(text):
            resultLabel = label
            break
    return resultLabel



def runnerAction(text):
    text = re.sub("\[.*?\]","", text)
    return searchAction(text, runnerPatterns)


def batterAction(text):

    text = parenPattern.sub("", text)
    text = re.sub("\[.*?\]","", text)
    text = text.split(",")[0]

    return searchAction(text, batterPatterns)


def managerAction(text):
    text = re.sub("\[.*?\]","", text)
    return searchAction(text, managerPatterns)


def cleanPlayerIds(text):
    for playerId in playerPattern.findall(text):
        text = playerPattern.sub(playerId, text, count=1)
    return text


################################################################################
################################################################################


class ScoreKeeper:
    """
    ScoreKeeper is a record keeper of outcomes.
    """

    def __init__(self, game):

        self.game = game
        self.scoreBook = ScoreBook(game)


    def pitch(self, pitcher=None):
        self.scoreBook.addPlayerStat(self.scoreBook.fieldingSide, "p", "NUM", self.scoreBook.currentPitcher)


    def pitcherOut(self, pitcher=None):
        self.scoreBook.addPlayerStat(self.scoreBook.fieldingSide, "p", "OUT", self.scoreBook.currentPitcher)


    def pitcherR(self, pitcher=None):
        self.scoreBook.addPlayerStat(self.scoreBook.fieldingSide, "p", "R", self.scoreBook.currentPitcher)


    def pitcherH(self, pitcher=None):
        self.scoreBook.addPlayerStat(self.scoreBook.fieldingSide, "p", "H", self.scoreBook.currentPitcher)


    def pitcherBB(self, pitcher=None):
        self.scoreBook.addPlayerStat(self.scoreBook.fieldingSide, "p", "BB", self.scoreBook.currentPitcher)


    def pitcherK(self, pitcher=None):
        self.scoreBook.addPlayerStat(self.scoreBook.fieldingSide, "p", "K", self.scoreBook.currentPitcher)


    def batterAB(self, batter=None):
        self.scoreBook.addPlayerStat(self.scoreBook.scoringSide, "b", "AB", batter)


    def batterBB(self, batter=None):
        self.scoreBook.addPlayerStat(self.scoreBook.scoringSide, "b", "BB", batter)


    def batterR(self, batter=None):
        self.scoreBook.addPlayerStat(self.scoreBook.scoringSide, "b", "R", batter)


    def batterRBI(self, batter=None):
        self.scoreBook.addPlayerStat(self.scoreBook.scoringSide, "b", "RBI", batter)


    def batterH(self, batter=None):
        self.scoreBook.addPlayerStat(self.scoreBook.scoringSide, "b", "H", batter)


    def batter2B(self, batter=None):
        self.scoreBook.addPlayerStat(self.scoreBook.scoringSide, "b", "2B", batter)


    def batter3B(self, batter=None):
        self.scoreBook.addPlayerStat(self.scoreBook.scoringSide, "b", "3B", batter)


    def batterHR(self, batter=None):
        self.scoreBook.addPlayerStat(self.scoreBook.scoringSide, "b", "HR", batter)
        self.scoreBook.addPlayerStat(self.scoreBook.scoringSide, "b", "R", batter)
        self.scoreBook.addPlayerStat(self.scoreBook.scoringSide, "b", "RBI", batter)


    def addRun(self):
        self.scoreBook.score[self.scoreBook.scoringSide] += 1


    def flipBook(self):
        side = "away" if self.scoreBook.scoringSide == "home" or not self.scoreBook.scoringSide else "home"
        self.scoreBook.scoringSide = side
        self.scoreBook.fieldingSide = "away" if side == "home" else "home"
        self.scoreBook.currentPitcher = self.scoreBook.pitchers[self.scoreBook.fieldingSide]
        self.scoreBook.battingLineup = self.scoreBook.lineups[side]


    def getPitcher(self):
        return self.scoreBook.currentPitcher


    def newPitcher(self, pitcher):
        self.scoreBook.pitchers[self.scoreBook.fieldingSide] = pitcher


    def setPitcher(self, pitcher):
        self.scoreBook.currentPitcher = pitcher


    def setLineup(self, lineup):
        self.scoreBook.battingLineup = lineup


    def setLineupOrder(self, num):
        self.scoreBook.lineupOrder = num


    def nextBatter(self):
        return self.scoreBook.getBatter()


    def getLineupOrder(self):
        return self.scoreBook.lineupOrder


################################################################################
################################################################################


class ScoreBook:

    pitcherStats = {"OUT":0,"NUM":0,"BB":0,"H":0,"R":0,"K":0 }
    batterStats = {"AB":0,"BB":0,"H":0,"2B":0,"3B":0,"HR":0,"R":0,"RBI":0}

    bookTemplate = {"b":{},"p":{}}

    def __init__(self, game):

        self.info = {"home": copy.deepcopy(ScoreBook.bookTemplate), "away": copy.deepcopy(ScoreBook.bookTemplate)}

        self.scoringSide = None
        self.fieldingSide = None
        self.currentPitcher = None
        self.battingLineup = None

        self.score = {"home":0, "away": 0}

        self.pitchers = {"home":game.homeTeam.currentPitcher, "away":game.awayTeam.currentPitcher}
        self.lineups = {"home":game.homeTeam.lineup, "away":game.awayTeam.lineup}
        self.battingOrder = {"home":-1, "away":-1}


    def setScoringSide(self, side):
        self.scoringSide = side



    def addPlayerStat(self, side, role, stat, playerId):

        statGroup = ScoreBook.pitcherStats if role == "p" else ScoreBook.batterStats
        statBook = self.info[side][role].get(playerId, statGroup.copy())
        statBook[stat] += 1
        self.info[side][role][playerId] = statBook


    def getBatter(self):

        num = self.battingOrder[self.scoringSide] + 1
        index = num % 9

        batterId = self.battingLineup[index]
        self.battingOrder[self.scoringSide] = num
        return batterId


################################################################################
################################################################################
