# Dirty hack
import os
# #
import json
import datetime
from pprint import pprint

from MLBProjections.MLBProjections.Models.PA import PlateAppearance
from MLBProjections.MLBProjections.Models.Umpire import Umpire
from MLBProjections.MLBProjections.Models.TicketManager import TicketManager
import MLBProjections.MLBProjections.Environ as ENV
import MLBProjections.MLBProjections.DB.MLB as DB
from MLBProjections.MLBProjections.Models.Ticket import Out, Single, Double, Triple, HomeRun, Walk, StrikeOut, DoublePlay

################################################################################
################################################################################





################################################################################
################################################################################


class BaseballTeam:

    def __init__(self, db, teamId, startingPitcher, lineup, isHome=False):

        self.teamId = teamId
        self.currentPitcher = startingPitcher
        self.isHome = isHome

        self.lineup = lineup


    def getPitcher(self):
        return self.currentPitcher


################################################################################
################################################################################


class BaseballDiamond:

    def __init__(self):

        self.firstBase = None
        self.secondBase = None
        self.thirdBase = None


    def getBase(self, base):
        return {"first":self.firstBase, "second":self.secondBase, "third":self.thirdBase}[base]


    def getBasesLoaded(self):
        return True if self.firstBase and self.secondBase and self.thirdBase else False


    def setBase(self, base, playerId):
        if base == "first":
            self.firstBase = playerId
        elif base == "second":
            self.secondBase = playerId
        else:
            self.thirdBase = playerId


    def clearBase(self, base):
        if base == "first":
            self.firstBase = None
        elif base == "second":
            self.secondBase = None
        else:
            self.thirdBase = None



    def moveBase(self, base1, base2=None):
        startBase = {"first":self.firstBase, "second":self.secondBase, "third":self.thirdBase}[base1]
        playerId = startBase
        self.clearBase(base1)

        if base2:
            self.setBase(base2, playerId)


    def clearBases(self):
        self.firstBase = None
        self.secondBase = None
        self.thirdBase = None



################################################################################
################################################################################


class BaseballGame(TicketManager):

    def __init__(self, gameJson):

        self.gameId = gameJson["gameId"]
        self.db = DB.MLBDatabase()
        self.db.openDB()
        super().__init__(gameJson)





    def __del__(self):
        self.db.closeDB()


    def initializeSport(self):

        self.diamond = BaseballDiamond()
        self.homeTeam = BaseballTeam(self.db, self.gameJson["homeTeam"]["teamId"], self.gameJson["homeTeam"]["starter"][0], self.gameJson["homeTeam"]["lineup"], True)
        self.awayTeam = BaseballTeam(self.db, self.gameJson["awayTeam"]["teamId"], self.gameJson["awayTeam"]["starter"][0], self.gameJson["awayTeam"]["lineup"])
        self.umpire = Umpire(self)



    def runTicketMachine(self):
        side = "away"
        winCase = False
        num = 1

        while not self.umpire.endGame(winCase, side):
            print("{} Inning {}".format(side, num))
            print("{0[home]} Home - Away {0[away]}".format(self.umpire.scoreKeeper.scoreBook.score))


            self.umpire.setSide(side)
            self.newInning(side, winCase=winCase)
            # Change side
            side = "home" if side == "away" else "away"
            num = num + 1 if side == "away" else num
            if num == 9 and side == "home":
                winCase = True

        projJson = {"games":[]}
        projPath = ENV.getProjPath(self.gameId)
        try:
            with open(projPath) as fileIn:
                projJson = json.load(fileIn)
        except FileNotFoundError:
            pass

        projJson["games"].append(self.umpire.scoreKeeper.scoreBook.info)

        with open(projPath, "w") as fileOut:
            json.dump(projJson, fileOut)



    def newInning(self, side, winCase):
        self.diamond.clearBases()
        self.umpire.clearOuts()
        self.umpire.scoreKeeper.flipBook(side)

        pitcher = self.umpire.scoreKeeper.getPitcher()


        while self.umpire.getOuts() < 3 and not self.umpire.endInning(winCase, side):
            # print("{0[home]} Home - Away {0[away]}".format(self.umpire.scoreKeeper.scoreBook.score))
            # print("{} Outs".format(self.umpire.getOuts()))
            # print("firstBase {}    secondBase {}    thirdBase {}".format(self.diamond.firstBase, self.diamond.secondBase, self.diamond.thirdBase))
            # Tickets are generated and recorded until 3 outs are reached
            batter = self.umpire.scoreKeeper.nextBatter()
            result = PlateAppearance(pitcher, batter, self.umpire).result

            ticket = {"Out":self.out, "Single":self.single, "Double":self.double, "Triple":self.triple,
                        "Home Run":self.homeRun, "Walk":self.walk, "Strikeout":self.strikeOut,
                        "Double Play":self.doublePlay}[result]

            ticket.generateTicket(pitcher=pitcher, batter=batter)
            print("\n\n")



    def setTicketTypes(self):
        self.out = Out(self.diamond, self.umpire)
        self.single = Single(self.diamond, self.umpire)
        self.double = Double(self.diamond, self.umpire)
        self.triple = Triple(self.diamond, self.umpire)
        self.homeRun = HomeRun(self.diamond, self.umpire)
        self.doublePlay = DoublePlay(self.diamond, self.umpire)
        self.walk = Walk(self.diamond, self.umpire)
        self.strikeOut = StrikeOut(self.diamond, self.umpire)


    def setTicketHolders(self):
        pass


################################################################################
################################################################################

if __name__ == "__main__":
    today = datetime.date.today()
    with open(ENV.getLineupPath(today)) as fileIn:
        matchups = json.load(fileIn)["matchups"]

    for i, matchup in enumerate(matchups):
        for n in range(15):
            BaseballGame(matchup)
