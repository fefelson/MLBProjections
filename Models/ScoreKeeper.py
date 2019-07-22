import copy

from MLBProjections.MLBProjections.Models.Player import Batter, Pitcher
from MLBProjections.MLBProjections.Models.Umpire import Umpire

################################################################################
################################################################################


gameCmd = "SELECT game_id FROM game_meta"
teamCmd = "SELECT {0[homeAway]}_id FROM game_meta"
startingPitcherCmd = "SELECT player_id FROM bullpens WHERE bullpens.team_id = ? AND bullpens.starter = 1"
lineupCmd = "SELECT lineups.player_id, first_name, last_name, bats FROM lineups INNER JOIN pro_players ON lineups.player_id = pro_players.player_id WHERE lineups.team_id = ? ORDER BY batt_order"


bullpenCmd = """
                SELECT player_id
                    FROM bullpens
                    INNER JOIN  (SELECT DISTINCT replace_id FROM pitcher_replace WHERE team_id = ?) AS replace
                        ON bullpens.player_id = replace.replace_id
                    WHERE bullpens.starter = 0
            """

stadiumCmd = "SELECT stadium_id FROM game_meta"


################################################################################
################################################################################


class ScoreKeeper:
    """
    ScoreKeeper keeps a record of player outcomes.
    """

    def __init__(self, db):
        self.scoreBook = ScoreBook(db)
        self.umpire = Umpire(self)
        self.exOuts = 0
        self.sequence = 1
        self.timeFrame = "All"


    def getFieldingTeam(self):
        return self.scoreBook.teams[self.scoreBook.fieldingSide]


    def setTimeFrame(self, timeFrame):
        self.timeFrame = timeFrame


    def setScoreBook(self):
        self.scoreBook.setupBook(self.timeFrame)


    def getBalls(self):
        return self.umpire.getCount()[0]


    def getStrikes(self):
        return self.umpire.getCount()[1]


    def getPitcher(self):
        side = self.scoreBook.fieldingSide
        pitcherId = self.scoreBook.currentPitcher.getId()
        stats = self.scoreBook.info[side]["pitchers"].get(int(pitcherId), None)
        teamId = self.scoreBook.teams[side]
        #print(stats)
        if stats:
            inning = self.inning

            num = stats["NUM"]
            r = stats["R"]


            removeNum = self.db.fetchOne("SELECT COUNT(pitcher_id) FROM pitcher_replace WHERE pitch_num <= ? AND pitcher_id = ?",(num,pitcher))[0]
            removeCount = self.db.fetchOne("SELECT COUNT(pitcher_id) FROM pitcher_replace WHERE pitcher_id = ?",(pitcher,))[0]
            removeRun = self.db.fetchOne("SELECT COUNT(pitcher_id) FROM pitcher_replace WHERE runs <= ? AND pitcher_id = ?",(r,pitcher))[0]


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
                    self.setPitcher(newPitcher)
        return self.scoreBook.currentPitcher


    def nextBatter(self):
        return self.scoreBook.nextBatter()



    def setPitcher(self, pitcher):
        side = self.scoreBook.fieldingSide
        self.scoreBook.activePitchers[side] = pitcher
        self.scoreBook.currentPitcher = pitcher


    def getInning(self):
        return self.umpire.getInning()


    def flipBook(self):
        self.scoreBook.changeSides()
        self.exOuts = 0


    def getSide(self):
        return self.scoreBook.scoringSide


    def addExOut(self):
        self.exOuts += 1


    def getExOuts(self):
        return self.exOuts + self.umpire.getOuts()


    def getUmpire(self):
        return self.umpire


    def recordBatterPA(self, batterId):
        self.scoreBook.addBatterStat("PA", batterId)


    def recordBatterAB(self, batterId):
        self.recordBatterPA(batterId)
        self.scoreBook.addBatterStat("AB", batterId)


    def recordBatterH(self, batterId):
        self.recordBatterAB(batterId)
        self.scoreBook.addBatterStat("H", batterId)


    def recordBatterK(self, batterId):
        self.recordBatterAB(batterId)
        self.scoreBook.addBatterStat("K", batterId)


    def recordBatterBB(self, batterId):
        self.recordBatterPA(batterId)
        self.scoreBook.addBatterStat("BB", batterId)


    def recordBatterHBP(self, batterId):
        self.recordBatterPA(batterId)
        self.scoreBook.addBatterStat("HBP", batterId)


    def recordBatter2B(self, batterId):
        self.recordBatterH(batterId)
        self.scoreBook.addBatterStat("2B", batterId)


    def recordBatter3B(self, batterId):
        self.recordBatterH(batterId)
        self.scoreBook.addBatterStat("3B", batterId)


    def recordBatterHR(self, batterId):
        self.recordBatterH(batterId)
        self.scoreBook.addBatterStat("HR", batterId)


    def recordPitcherH(self, pitcherId):
        self.scoreBook.addPitcherStat("H", pitcherId)


    def recordPitcherK(self, pitcherId):
        self.scoreBook.addPitcherStat("K", pitcherId)


    def recordPitcherBB(self, pitcherId):
        self.scoreBook.addPitcherStat("BB", pitcherId)


    def recordPitcherHBP(self, pitcherId):
        self.scoreBook.addPitcherStat("HBP", pitcherId)


    def recordPitcherOut(self, pitcherId):
        self.scoreBook.addPitcherStat("OUT", pitcherId)


    def recordTeamRun(self):
        self.scoreBook.addRun()


    def recordBatterRun(self, runnerId):
        self.scoreBook.addBatterStat("R", runnerId)


    def recordBatterRbi(self, batterId):
        self.scoreBook.addBatterStat("RBI", batterId)


    def recordPitcherRun(self, pitcherId):
        if pitcherId != -20:
            self.scoreBook.addPitcherStat("R", pitcherId)


    def recordPitcherER(self, pitcherId):
        if pitcherId != -20:
            self.scoreBook.addPitcherStat("ER", pitcherId)


    def recordPitch(self, pitcherId):
        self.sequence += 1
        self.scoreBook.addPitcherStat("NUM", pitcherId)


    def newSequence(self):
        self.sequence = 1


    def getScore(self):
        return self.scoreBook.getScore()


    def getSequence(self):
        return self.sequence


    def getTurn(self, batter):
        return self.scoreBook.getTurn(batter)


################################################################################
################################################################################


class ScoreBook:

    pitcherStats = {"OUT":0,"NUM":0,"HBP":0,"BB":0,"H":0,"R":0,"ER":0, "K":0 }
    batterStats = {"PA":0,"AB":0,"K":0,"HBP":0,"BB":0,"H":0,"2B":0,"3B":0,"HR":0,"R":0,"RBI":0}
    bookTemplate = {"batters":{},"pitchers":{}}

    def __init__(self, db):

        self.db = db

        self.info = {"home": copy.deepcopy(ScoreBook.bookTemplate), "away": copy.deepcopy(ScoreBook.bookTemplate)}

        self.gameId = db.fetchOne(gameCmd)[0]
        self.stadiumId = db.fetchOne(stadiumCmd)[0]
        self.teams = {"home":None, "away":None}
        self.scores = {"home":0, "away":0}
        self.scoringSide = None
        self.fieldingSide = None
        self.currentPitcher = None
        self.currentLineup = None
        self.activePitchers = {"home":None, "away":None}
        self.battingLineups = {"home":[], "away":[]}
        self.battingOrders = {"home":-1, "away":-1}
        self.bullpens = {"home":[], "away":[]}
        self.turn = {}


    def setupBook(self, timeFrame):

        for homeAway in ("home", "away"):
            # teamId
            teamId = self.db.fetchOne(teamCmd.format({"homeAway":homeAway}))[0]
            self.teams[homeAway] = teamId

            starterId = self.db.fetchOne(startingPitcherCmd, (teamId, ))[0]
            self.activePitchers[homeAway] = Pitcher(starterId, timeFrame, self.db)

            for pitcherId in self.db.fetchAll(bullpenCmd, (teamId,)):
                self.bullpens[homeAway].append(Pitcher(pitcherId[0], timeFrame, self.db))

            for batterId in self.db.fetchAll(lineupCmd, (teamId,)):
                self.battingLineups[homeAway].append(Batter(batterId[0], timeFrame, self.db))

            # initialize battingOrder
            self.battingOrders[homeAway] = -1
            # initialize score
            self.scores[homeAway] = 0


    def getScore(self):
        return self.scores


    def changeSides(self):
        side = "away" if self.scoringSide == "home" or not self.scoringSide else "home"
        self.scoringSide = side
        self.fieldingSide = "away" if side == "home" else "home"
        self.currentPitcher = self.activePitchers[self.fieldingSide]
        self.currentLineup = self.battingLineups[side]


    def addRun(self):
        self.scoreBook.scores[self.scoringSide] += 1


    def addBatterStat(self, stat, batterId):
        self.addPlayerStat(self.scoringSide, "batters", stat, batterId)


    def addPitcherStat(self, stat, pitcherId):
        self.addPlayerStat(self.fieldingSide, "pitchers", stat, pitcherId)


    def addPlayerStat(self, side, role, stat, playerId):
        statGroup = ScoreBook.pitcherStats if role == "pitchers" else ScoreBook.batterStats
        statBook = self.info[side][role].get(playerId, statGroup.copy())
        statBook[stat] += 1
        self.info[side][role][playerId] = statBook


    def nextBatter(self):
        num = self.battingOrders[self.scoringSide] + 1
        index = num % 9
        batter = self.currentLineup[index]
        self.battingOrders[self.scoringSide] = num

        allTurns = self.turn.get(self.currentPitcher.getId(), {})
        turn = allTurns.get(batter.getId(), 0) +1
        allTurns[batter.getId()] = turn
        self.turn[self.currentPitcher.getId()] = allTurns

        return batter


    def getTurn(self, batter):
        allTurns = self.turn.get(self.currentPitcher.getId(), {})
        turn = allTurns.get(batter.getId(), 1)
        return turn


################################################################################
################################################################################
