import random

from MLBProjections.MLBProjections.Models.BaseballGame import BaseballGame

import MLBProjections.MLBProjections.Environ as ENV
import MLBProjections.MLBProjections.DB.MLB as MLB

################################################################################
################################################################################





################################################################################
################################################################################


class GameManager:

    def __init__(self, model):
        self.model = model


    def newGameBundle(self, gameDB, settings):
        return GameBundle(self, gameDB, settings)


################################################################################
################################################################################


class GameBundle:

    def __init__(self, gameManager, gameDB, settings):

        self.gameManager = gameManager
        self.gameDB = gameDB
        self.totalSim = settings["total"]
        self.outcomeValues = self.setValues(settings["outcomeValues"])
        self.dateValues = self.setValues(settings["dateValues"])


    def setValues(self, info):
        values = []
        for key, value in info:
            for _ in range(value):
                values.append(key)
        random.shuffle(values)
        return values


    def run(self):


        while self.totalSim:
            outcome = self.outcomeValues.pop()
            timeFrame = self.dateValues.pop()
            baseballGame = BaseballGame(self.gameDB, outcome, timeFrame)
            baseballGame.initializeSport()
            baseballGame.setTicketTypes()
            baseballGame.runTicketMachine()

            self.totalSim -= 1


################################################################################
################################################################################


if __name__ == "__main__":
    manager = GameManager(None)
    settings = {'dateValues': [('All', 19), ('Season', 19), ('3Months', 19), ('1Month', 18)],
                'outcomeValues': [('Random', 0), ('Probable', 38)],
                'total': 75}
    gameDB = MLB.MLBGame(390721115)
    bundle = manager.newGameBundle(gameDB, settings)
    bundle.run()
