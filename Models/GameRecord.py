import datetime
import json
from itertools import chain

import MLBProjections.MLBProjections.Environ as ENV
from MLBProjections.MLBProjections.Models.TicketManager import TicketManager
from MLBProjections.MLBProjections.Models.BaseballDiamond import BaseballDiamond
from MLBProjections.MLBProjections.Models.BaseballTeam import BaseballTeam

from pprint import pprint

################################################################################
################################################################################





################################################################################
################################################################################


class GameRecord(TicketManager):

    def __init__(self, db, gameJson):
        super().__init__(db, gameJson)


    def selectTicket(self, sql, args):
        return self.db.execute()


    def initializeSport(self):
        self.diamond = BaseballDiamond()
        self.homeTeam = BaseballTeam(self.gameJson["home_id"], True)
        self.awayTeam = BaseballTeam(self.gameJson["away_id"])
        #self.umpire = Umpire(self)





    def runTicketMachine(self):



        pbp = self.gameJson["play_by_play"].values()
        pitches = self.gameJson["pitches"].values()

        for play in sorted(chain(pbp,pitches), key=lambda x: int(x["play_num"])):

            if play["play_type"] =="RESULT":
                pprint(play)
                print("\n\n\n")


    def setTicketTypes(self):
        pass


################################################################################
################################################################################

if __name__ == "__main__":
    today = datetime.date.today()
    gameJson = None
    with open("/home/ededub/FEFelson/MLBProjections/PlayByPlay/2019/05/20/390520121.json") as fileIn:
        gameJson = json.load(fileIn)
    GameReplay(gameJson)
