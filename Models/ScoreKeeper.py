import json
import os
import re
import copy

from collections import Counter
from pprint import pprint

################################################################################
################################################################################


pitchTypes = ((1,"Fastball"),
                (2,"Curveball"),
                (3,"Slider"),
                (4,"Changeup"),
                (6,"Knuckleball"),
                (7,"Unknown"),
                (8,"Split-Finger"),
                ("9","Cut Fastball"))


pitchResults = ((1,"Called Strike"),
                (2,"Swinging Strike"),
                (3,"Foul Ball"),
                (0,"Ball"),
                (5,"Bunt Foul"),
                (10,"In Play"))


valuesBase = (0,1667,3333, 5000, 6667, 8333, 10000, 11667, 13333, 15000, 16667)
values = list(valuesBase) + [ x*-1 for x in valuesBase if x ]
pitchLocations = []
for horizontal in values:
    for vertical in values:
        # append a tuple (valA, valB)
        pitchLocations.append((horizontal,vertical))


def sortingHat(horizontal, vertical):
    # find a box for the pitch location
    y = round(vertical/1667) - 11
    x = round(horizontal/1667) + 11

    yValue = _hat(abs(y))
    xValue = _hat(x)+1
    return (yValue *5) + xValue


def _hat(item):
    value = None
    if item <= 3:
        value = 0
    elif item <= 7:
        value = 1
    elif item <=12:
        value = 2
    elif item <= 16:
        value = 3
    else:
        value = 4
    return value


inPlayResults = (
                    ('grounded out', "Out"),
                    ('singled', "Single"),
                    ("fielder's choice", "Out"),
                    ('doubled', "Double"),
                    ('lined out', "Out"),
                    ('flied out', "Out"),
                    ('double play', "Double Play"),
                    ('popped out', "Out"),
                    ('homered', "Home Run"),
                    ('reached on an infield single', "Single"),
                    ("reached on 's throwing error", "Out"),
                    ('fouled out', "Out"),
                    ('sacrifice fly', "Out"),
                    ('tripled', "Triple"),
                    ('grounded bunt out', "Out"),
                    ('ground rule double', "Double"),
                    ("reached on 's fielding error", "Out"),
                    ('sacrificed', "Out"),
                    ('inside the park home run', "Home Run"),
                    ('triple play', "Triple Play")
                )


positions = {"pitcher":1, "catcher":2, "first":3, "second":4, "third":5,
             "shortstop":6, "left":7, "center":8, "right":9}


playerPattern = re.compile("mlb.p.(?P<playerId>\d*)")
batterPattern = re.compile("^\[(?P<playerId>\d*)\]")
parenPattern = re.compile("\(.*?\)")
sacrificePattern = re.compile("sacrificed")
sacFlyPattern = re.compile("sacrifice fly")
fouledPattern = re.compile("fouled out")
grounderPattern = re.compile("grounded out")
poppedPattern = re.compile("popped out")
fliedPattern = re.compile("flied out")
linedPattern = re.compile("lined out")
singledPattern = re.compile("singled")
doubledPattern = re.compile("doubled")
groundDoublePattern = re.compile("ground rule double")
iphrPattern = re.compile("inside the park home run")
triplePlayPattern = re.compile("triple play")
doublePlayPattern = re.compile("double play")
tripledPattern = re.compile("tripled")
homeredPattern = re.compile("homered")
fielderPattern = re.compile("fielder's choice")
groundBuntPattern = re.compile("grounded bunt out")
outToPattern = re.compile("out to (?P<field>\w*)")
groundOutPattern = re.compile("(?P<throw>\w*) to (?P<field>\w*)")


def manageText(text):

    text = parenPattern.sub("", text)
    text = re.sub("\[.*?\]","", text)
    text = text.split(".")[0]
    text = text.split(",")[0]
    text = "double play" if doublePlayPattern.search(text) else text
    text = "triple play" if triplePlayPattern.search(text) else text
    text = "grounded out" if grounderPattern.search(text) else text
    text = "popped out" if poppedPattern.search(text) else text
    text = "flied out" if fliedPattern.search(text) else text
    text = "lined out" if linedPattern.search(text) else text
    text = "singled" if singledPattern.search(text) else text
    text = "doubled" if doubledPattern.search(text) else text
    text = "ground rule double" if groundDoublePattern.search(text) else text
    text = "grounded bunt out" if groundBuntPattern.search(text) else text
    text = "tripled" if tripledPattern.search(text) else text
    text = "inside the park home run" if iphrPattern.search(text) else text
    text = "homered" if homeredPattern.search(text) else text
    text = "fouled out" if fouledPattern.search(text) else text
    text = "sacrifice fly" if sacFlyPattern.search(text) else text
    text = "sacrificed" if sacrificePattern.search(text) else text
    text = "fielder's choice" if fielderPattern.search(text) else text
    return text.strip()


################################################################################
################################################################################


class ScoreKeeper:
    """
    ScoreKeeper is a record keeper of outcomes.
    """

    def __init__(self, game):

        self.game = game
        self.scoreBook = ScoreBook(game)


    def pitcherOut(self, pitcher=None):
        self.scoreBook.addPlayerStat(self.scoreBook.fieldingSide, "p", "OUT", self.scoreBook.currentPitcher)



    def pitcherR(self, pitcher=None):
        self.scoreBook.addPlayerStat(self.scoreBook.fieldingSide, "p", "R", self.scoreBook.currentPitcher)


    def pitcherH(self, pitcher=None):
        self.scoreBook.addPlayerStat(self.scoreBook.fieldingSide, "p", "H", self.scoreBook.currentPitcher)


    def pitcherBB(self, pitcher=None):
        self.scoreBook.addPlayerStat(self.scoreBook.fieldingSide, "p", "BB", self.scoreBook.currentPitcher)


    def pitcherK(self, pitcher=None):
        self.scoreBook.addPlayerStat(self.scoreBook.fieldingSide, "p", "OUT", self.scoreBook.currentPitcher)
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
        self.scoreBook.addPlayerStat(self.scoreBook.scoringSide, "b", "AB", batter)
        self.scoreBook.addPlayerStat(self.scoreBook.scoringSide, "b", "H", batter)


    def batter2B(self, batter=None):
        self.scoreBook.addPlayerStat(self.scoreBook.scoringSide, "b", "AB", batter)
        self.scoreBook.addPlayerStat(self.scoreBook.scoringSide, "b", "H", batter)
        self.scoreBook.addPlayerStat(self.scoreBook.scoringSide, "b", "2B", batter)


    def batter3B(self, batter=None):
        self.scoreBook.addPlayerStat(self.scoreBook.scoringSide, "b", "AB", batter)
        self.scoreBook.addPlayerStat(self.scoreBook.scoringSide, "b", "H", batter)
        self.scoreBook.addPlayerStat(self.scoreBook.scoringSide, "b", "3B", batter)


    def batterHR(self, batter=None):
        self.scoreBook.addPlayerStat(self.scoreBook.scoringSide, "b", "AB", batter)
        self.scoreBook.addPlayerStat(self.scoreBook.scoringSide, "b", "H", batter)
        self.scoreBook.addPlayerStat(self.scoreBook.scoringSide, "b", "HR", batter)
        self.scoreBook.addPlayerStat(self.scoreBook.scoringSide, "b", "R", batter)
        self.scoreBook.addPlayerStat(self.scoreBook.scoringSide, "b", "RBI", batter)


    def addRun(self):
        self.scoreBook.score[self.scoreBook.scoringSide] += 1


    def flipBook(self, side):
        self.scoreBook.scoringSide = side
        self.scoreBook.fieldingSide = "away" if side == "home" else "home"
        self.scoreBook.currentPitcher = self.scoreBook.pitchers[self.scoreBook.fieldingSide]
        self.scoreBook.battingLineup = self.scoreBook.lineups[side]


    def getPitcher(self):
        return self.scoreBook.currentPitcher


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

    pitcherStats = {"OUT":0,"BB":0,"H":0,"R":0,"K":0 }
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
