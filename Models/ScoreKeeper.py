import json
import os
import re
import copy

from collections import Counter
from pprint import pprint

################################################################################
################################################################################

gameCmd = "SELECT game_id FROM game_meta"
teamCmd = "SELECT {0[teamAbrv]}_id FROM game_meta"
startingPitcherCmd = "SELECT bullpen.player_id, first_name, last_name, throws FROM bullpen INNER JOIN pro_players ON bullpen.player_id = pro_players.player_id WHERE bullpen.team_id = ? AND bullpen.starter = 1"
lineupCmd = "SELECT lineups.player_id, first_name, last_name, bats FROM lineups INNER JOIN pro_players ON lineups.player_id = pro_players.player_id WHERE lineups.team_id = ? ORDER BY batt_order"
bullpenCmd = "SELECT bullpen.player_id, first_name, last_name, throws FROM bullpen INNER JOIN pro_players ON bullpen.player_id = pro_players.player_id WHERE bullpen.team_id = ? AND bullpen.starter = 0"
stadiumCmd = "SELECT stadium_id FROM game_meta"

################################################################################
################################################################################


class ScoreKeeper:
    """
    ScoreKeeper is a record keeper of outcomes.
    """

    def __init__(self, db):

        self.scoreBook = ScoreBook(db)


    def getPitchNum(self):
        side = self.scoreBook.fieldingSide
        statBook = self.scoreBook.info[side]["p"].get(self.scoreBook.currentPitcher, ScoreBook.pitcherStats.copy())
        return statBook["NUM"] + 1



    def pitch(self, pitcher=None):
        self.scoreBook.addPlayerStat(self.scoreBook.fieldingSide, "p", "NUM", pitcher)


    def pitcherOut(self, pitcher=None):
        self.scoreBook.addPlayerStat(self.scoreBook.fieldingSide, "p", "OUT", pitcher)


    def pitcherR(self, pitcher=None):
        self.scoreBook.addPlayerStat(self.scoreBook.fieldingSide, "p", "R", pitcher)


    def pitcherH(self, pitcher=None):
        self.scoreBook.addPlayerStat(self.scoreBook.fieldingSide, "p", "H", pitcher)


    def pitcherBB(self, pitcher=None):
        self.scoreBook.addPlayerStat(self.scoreBook.fieldingSide, "p", "BB", pitcher)


    def pitcherK(self, pitcher=None):
        self.scoreBook.addPlayerStat(self.scoreBook.fieldingSide, "p", "K", pitcher)


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
        self.scoreBook.scores[self.scoreBook.scoringSide] += 1


    def flipBook(self):
        side = "away" if self.scoreBook.scoringSide == "home" or not self.scoreBook.scoringSide else "home"
        self.scoreBook.scoringSide = side
        self.scoreBook.fieldingSide = "away" if side == "home" else "home"
        self.scoreBook.currentPitcher = self.scoreBook.activePitchers[self.scoreBook.fieldingSide]
        self.scoreBook.currentLineup = self.scoreBook.battingLineups[side]


    def getPitcher(self):
        return self.scoreBook.currentPitcher


    def newPitcher(self, pitcher):

        self.scoreBook.activePitchers[self.scoreBook.fieldingSide] = pitcher
        bullpen = self.scoreBook.bullpens[self.scoreBook.fieldingSide]
        for i,player in enumerate(bullpen):
            if player == pitcher:
                bullpen.pop(i)
                break
        self.scoreBook.bullpens[self.scoreBook.fieldingSide] = bullpen
        self.setPitcher(pitcher)


    def setPitcher(self, pitcher):
        self.scoreBook.currentPitcher = pitcher


    def getTurn(self, batter, pitcher):
        return self.scoreBook.getTurn(batter, pitcher)


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

    pitcherStats = {"OUT":0,"NUM":0,"HBP":0,"BB":0,"H":0,"R":0,"K":0 }
    batterStats = {"AB":0,"BB":0,"H":0,"2B":0,"3B":0,"HR":0,"R":0,"RBI":0}

    bookTemplate = {"b":{},"p":{}}

    def __init__(self, db):

        self.info = {"home": copy.deepcopy(ScoreBook.bookTemplate), "away": copy.deepcopy(ScoreBook.bookTemplate)}

        self.gameId = db.curs.execute(gameCmd).fetchone()[0]
        self.stadiumId = db.curs.execute(stadiumCmd).fetchone()[0]
        self.teams = {}
        self.scores = {}
        self.scoringSide = None
        self.fieldingSide = None
        self.currentPitcher = None
        self.currentLineup = None
        self.activePitchers = {}
        self.battingLineups = {}
        self.battingOrders = {}
        self.bullpens = {}
        self.benches = {}
        self.turn = {}


        for teamAbrv in ("home", "away"):
            # teamId
            teamId = db.curs.execute(teamCmd.format({"teamAbrv":teamAbrv})).fetchone()[0]
            self.teams[teamAbrv] = teamId
            # playerId, firstName, lastName, throws
            self.activePitchers[teamAbrv] = db.curs.execute(startingPitcherCmd, (teamId, )).fetchone()
            # playerId, firstName, lastName, bats
            self.battingLineups[teamAbrv] = [x for x in db.curs.execute(lineupCmd, (teamId,)).fetchall()]
            # playerId, firstName, lastName, throws
            self.bullpens[teamAbrv] = [x for x in db.curs.execute(bullpenCmd, (teamId,)).fetchall()]
            # initialize battingOrder
            self.battingOrders[teamAbrv] = -1
            # initialize score
            self.scores[teamAbrv] = 0



    def setScoringSide(self, side):
        self.scoringSide = side


    def getTurn(self, batter, pitcher):
        allTurns = self.turn.get(pitcher, {})
        turn = allTurns.get(batter, 0) +1
        allTurns[batter] = turn
        self.turn[pitcher] = allTurns
        return turn




    def addPlayerStat(self, side, role, stat, playerId):
        # Dirty hack
        playerId = int(playerId[0])

        statGroup = ScoreBook.pitcherStats if role == "p" else ScoreBook.batterStats
        statBook = self.info[side][role].get(playerId, statGroup.copy())
        statBook[stat] += 1
        self.info[side][role][playerId] = statBook


    def getBatter(self):

        num = self.battingOrders[self.scoringSide] + 1
        index = num % 9


        batterId = self.currentLineup[index]
        self.battingOrders[self.scoringSide] = num
        return batterId


################################################################################
################################################################################
