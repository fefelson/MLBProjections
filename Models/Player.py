from abc import ABCMeta, abstractmethod
import datetime
from pprint import pprint

################################################################################
################################################################################

today = datetime.date.today()
threeMonths = today - datetime.timedelta(90)
oneMonth = today - datetime.timedelta(30)

playerStats = ("playerId", "firstName", "lastName", "bats", "throws")

gdSettings = ['All', 'Season', '3Months', '1Month']

timeFrameWhereCmd = {"All": "",
                        "Season": "WHERE season ="+str(today.year),
                        "3Months": "WHERE season="+str(today.year) + " AND game_date >="+"{}.{}".format(*str(threeMonths).split("-")[1:]),
                        "1Month": "WHERE season="+str(today.year) + " AND game_date >="+"{}.{}".format(*str(oneMonth).split("-")[1:])}


playerCmd = "SELECT player_id, first_name, last_name, bats, throws FROM pro_players WHERE player_id = ?"

baseCmd = "SELECT game_id FROM games "

pitchCountCmd = """
                    SELECT COUNT(pitch_contact_id)
                        FROM pitch_contacts
                        INNER JOIN ({0[gdCmd]}) AS gd
                            ON pitch_contacts.game_id = gd.game_id
                        WHERE {0[playerType]}_id = ?
                        GROUP BY {0[playerType]}_id
                """



################################################################################
################################################################################


class Player(metaclass=ABCMeta):

    def __init__(self, playerId, timeFrame, db):

        for key, value in zip(playerStats, db.fetchOne(playerCmd, (playerId,))):
            setattr(self, key, value)
        self.gdCmd = self.setGDCmd(timeFrame, db)


    def getId(self):
        return self.playerId


    @abstractmethod
    def _playerType(self):
        pass


    def getGDCmd(self):
        return self.gdCmd


    def setGDCmd(self, timeFrame, db):
        index = gdSettings.index(timeFrame)
        gdCmd = baseCmd
        while True:
            timeFrame = gdSettings[index]
            gdCmd = baseCmd + timeFrameWhereCmd[timeFrame]
            try:
                pitches = db.fetchOne(pitchCountCmd.format({"gdCmd":gdCmd, "playerType": self._playerType()}), (self.playerId,))[0]
                if pitches > 100:
                    break
            except TypeError:
                pass
            index -= 1
        return gdCmd


################################################################################
################################################################################


class Batter(Player):

    def __init__(self, playerId, timeFrame, db):
        super().__init__(playerId, timeFrame, db)


    def _playerType(self):
        return "batter"


    def getBatSide(self):
        return self.bats


################################################################################
################################################################################


class Pitcher(Player):

    def __init__(self, info, timeFrame, db):
        super().__init__(info, timeFrame, db)


    def _playerType(self):
        return "pitcher"


    def getThrowSide(self):
        return self.throws


################################################################################
################################################################################
