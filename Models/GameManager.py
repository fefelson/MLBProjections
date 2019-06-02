# Dirty hack
import os
# #
import json
import datetime
from pprint import pprint

from MLBProjections.MLBProjections.Models.BaseballTeam import BaseballTeam
from MLBProjections.MLBProjections.Models.BaseballDiamond import BaseballDiamond
from MLBProjections.MLBProjections.Models.PA import PlateAppearance
from MLBProjections.MLBProjections.Models.Umpire import Umpire
from MLBProjections.MLBProjections.Models.TicketManager import TicketManager
import MLBProjections.MLBProjections.Environ as ENV
import MLBProjections.MLBProjections.DB.MLB as DB
import MLBProjections.MLBProjections.Models.Ticket as TK

################################################################################
################################################################################





################################################################################
################################################################################


class BaseballGame(TicketManager):

    def __init__(self, db):
        db.openDB()
        self.gameId = db.curs.execute("SELECT game_id FROM games").fetchone()[0]

        super().__init__(db)



    def __del__(self):
        self.db.closeDB()


    def initializeSport(self):

        self.diamond = BaseballDiamond()
        self.homeTeam = BaseballTeam(self.db, True)
        self.awayTeam = BaseballTeam(self.db)
        self.umpire = Umpire(self)


    def runTicketMachine(self):

        self.umpire.setInning()


        while not self.umpire.endGame():
            # pprint(self.umpire.scoreKeeper.scoreBook.info)
            # "home" or "away"



            print("\n\n\n")
            print("{} Inning {}".format(self.umpire.side, self.umpire.inning))
            print("{0[home]} Home - Away {0[away]}".format(self.umpire.scoreKeeper.scoreBook.score))

            self.newInning()

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



    def newInning(self):
        self.diamond.clearBases()
        self.umpire.clearOuts()
        self.umpire.scoreKeeper.flipBook()



        while self.umpire.getOuts() < 3 and not self.umpire.endInning():
            # print("{0[home]} Home - Away {0[away]}".format(self.umpire.scoreKeeper.scoreBook.score))
            # print("{} Outs".format(self.umpire.getOuts()))
            print("firstBase {}    secondBase {}    thirdBase {}".format(self.diamond.firstBase, self.diamond.secondBase, self.diamond.thirdBase))
            # Tickets are generated and recorded until 3 outs are reached
            pitcher = self.umpire.getPitcher()
            batter = self.umpire.nextBatter()
            result = PlateAppearance(pitcher, batter, self.umpire).result
            # Dirty Hack
            result = "Out" if not result else result
            ##
            ticket = {"Out":self.out, "Ground Out":self.groundOut, "Strike Out":self.strikeOut,
                        "Single":self.single, "Fly Out":self.flyOut, "Walk":self.walk,
                        "Line Out":self.lineOut, "Double":self.double, "Pop Out":self.popOut,
                        "Home Run":self.homeRun, "Fielder's Choice":self.fielderChoice,
                        "Double Play":self.doublePlay, "Fouled Out":self.foulOut,
                        "Hit by Pitch":self.hbp, "Reached on Error":self.reachOnError,
                        "Sacrifice":self.sacrifice, "Triple":self.triple, "Triple Play":self.triplePlay
                    }.get(result, self.out)

            ticket.generateTicket(pitcher=pitcher, batter=batter)
            print("\n\n")
        self.umpire.setInning()


    def setTicketTypes(self):
        self.out = TK.Out(self.diamond, self.umpire)
        self.groundOut = TK.GroundOut(self.diamond, self.umpire)
        self.lineOut = TK.LineOut(self.diamond, self.umpire)
        self.flyOut = TK.FlyOut(self.diamond, self.umpire)
        self.popOut = TK.PopOut(self.diamond, self.umpire)
        self.foulOut = TK.FoulOut(self.diamond, self.umpire)
        self.strikeOut = TK.StrikeOut(self.diamond, self.umpire)
        self.doublePlay = TK.DoublePlay(self.diamond, self.umpire)
        self.triplePlay = TK.TriplePlay(self.diamond, self.umpire)
        self.fielderChoice = TK.FielderChoice(self.diamond, self.umpire)
        self.sacrifice = TK.Sacrifice(self.diamond, self.umpire)

        self.single = TK.Single(self.diamond, self.umpire)
        self.double = TK.Double(self.diamond, self.umpire)
        self.triple = TK.Triple(self.diamond, self.umpire)
        self.homeRun = TK.HomeRun(self.diamond, self.umpire)

        self.walk = TK.Walk(self.diamond, self.umpire)
        self.hbp = TK.HitByPitch(self.diamond, self.umpire)

        self.reachOnError = TK.ReachOnError(self.diamond, self.umpire)


    def setTicketHolders(self):
        pass


################################################################################
################################################################################

if __name__ == "__main__":
    today = datetime.date.today()
    with open(ENV.getLineupPath(today)) as fileIn:
        matchups = json.load(fileIn)["matchups"]

        for n in range(20):
            for i, matchup in enumerate(matchups):

                if i not in (10, ):


                    BaseballGame(matchup)
