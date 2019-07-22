import json
import datetime
from pprint import pprint

from MLBProjections.MLBProjections.Models.BaseballDiamond import BaseballDiamond
from MLBProjections.MLBProjections.Managers.DungeonMaster import DungeonMaster
from MLBProjections.MLBProjections.Managers.TicketManager import TicketManager
from MLBProjections.MLBProjections.Models.ScoreKeeper import ScoreKeeper
import MLBProjections.MLBProjections.Environ as ENV
import MLBProjections.MLBProjections.Tickets as TK

################################################################################
################################################################################





################################################################################
################################################################################


class BaseballGame(TicketManager):

    def __init__(self, db, outcome, timeFrame):
        super().__init__(db)
        self.outcome = outcome
        self.timeFrame = timeFrame


    def initializeSport(self):
        self.dungeonMaster = DungeonMaster(self.db, self.outcome)
        self.diamond = BaseballDiamond()
        self.scoreKeeper = ScoreKeeper(self.db)
        self.scoreKeeper.setTimeFrame(self.timeFrame)
        self.scoreKeeper.setScoreBook()
        self.umpire = self.scoreKeeper.getUmpire()


    def runTicketMachine(self):
        self.umpire.setInning()
        while not self.umpire.endGame():
            self.newInning()
        self.recordGame()
        self.writeGameFile()


    def recordGame(self):
        raise AssertionError


    def writeGameFile(self):
        projJson = {"games":[]}
        projPath = ENV.getProjPath(self.scoreKeeper.getGameId())
        try:
            with open(projPath) as fileIn:
                projJson = json.load(fileIn)
        except FileNotFoundError:
            pass

        projJson["games"].append(self.scoreKeeper.getGameResults())
        with open(projPath, "w") as fileOut:
            json.dump(projJson, fileOut)


    def plateAppearance(self, pitcher, batter):
        self.umpire.resetCount()
        self.scoreKeeper.newSequence()
        abResult = None

        while True:
            pitch = self.dungeonMaster.getPitch(pitcher, batter, self.scoreKeeper, self.diamond.getDiamondState())
            swing = self.dungeonMaster.getSwing(pitcher, batter, pitch, self.scoreKeeper, self.diamond.getDiamondState())
            pitchResult = self.dungeonMaster.getPitchResult(pitch[-1], swing)
            self.scoreKeeper.recordPitch(pitcher.getId())

            if pitchResult == 10:
                pitcherContact = self.dungeonMaster.getPitcherContact(pitcher, batter, pitch)
                batterContact = self.dungeonMaster.getBatterContact(pitcher, batter, pitch)
                abResult = self.dungeonMaster.getContactResult(pitcherContact, batterContact, self.scoreKeeper)[0]
            else:
                abResult = self.umpire.recordPitchResult(pitchResult)

            if abResult:
                print(abResult)
                raise AssertionError
                return abResult


    def newInning(self):
        self.diamond.clearBases()
        self.umpire.clearOuts()
        self.scoreKeeper.flipBook()

        # print("\n\n\n")
        print("{} Inning {}".format(self.scoreKeeper.getSide().capitalize(), self.scoreKeeper.getInning()))
        print("{0[home]} Home - Away {0[away]}".format(self.scoreKeeper.getScore()))

        while not self.umpire.endInning():
            # print("{0[home]} Home - Away {0[away]}".format(self.umpire.scoreKeeper.scoreBook.score))
            # print("{} Outs".format(self.umpire.getOuts()))
            # print("firstBase {}    secondBase {}    thirdBase {}".format(self.diamond.firstBase, self.diamond.secondBase, self.diamond.thirdBase))
            # Tickets are generated and recorded until 3 outs are reached

            pitcher = self.scoreKeeper.getPitcher()
            batter = self.scoreKeeper.nextBatter()

            result = self.plateAppearance(pitcher, batter)
            ticket = {"Ground Out":self.groundOut, "Strike Out":self.strikeOut,
                        "Single":self.single, "Fly Out":self.flyOut, "Walk":self.walk,
                        "Double":self.double, "Home Run":self.homeRun, "Fielder's Choice":self.groundOut,
                        "Double Play":self.doublePlay, "Hit by Pitch":self.hbp,
                        "Reached on Error":self.reachOnError, "Sacrifice":self.flyOut,
                        "Triple":self.triple
                    }.get(result, self.out).getStateTicket(self.diamond.getDiamondState())

            ticket.recordOuts(self.umpire)
            ticket.recordEvents(pitcher.getId(), batter.getId(), self.diamond, self.umpire, self.scoreKeeper)
            ticket.moveBases(self.diamond)
            ticket.reachedBase(pitcher.getId(), batter.getId(), self.diamond)

        self.umpire.setInning()


    def setTicketTypes(self):
        self.out = TK.Out()
        self.groundOut = TK.GroundOut()
        self.flyOut = TK.FlyOut()
        self.strikeOut = TK.StrikeOut()
        self.doublePlay = TK.DoublePlay()
        self.single = TK.Single()
        self.double = TK.Double()
        self.triple = TK.Triple()
        self.homeRun = TK.HomeRun()
        self.walk = TK.Walk()
        self.hbp = TK.HitByPitch()

        self.reachOnError = TK.ReachOnError()

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
