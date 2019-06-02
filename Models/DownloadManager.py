import json
import os
import urllib.error as error

from abc import ABCMeta, abstractmethod
from bs4 import BeautifulSoup
from http.client import IncompleteRead
from time import sleep
from urllib.request import urlopen, Request
from datetime import date, datetime, timedelta

import MLBProjections.MLBProjections.Environ as ENV

# For debugging
from pprint import pprint

################################################################################
################################################################################


headers = {"Host": "sports.yahoo.com",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0",
            "Connection": "close",
            "Cache-Control": "max-age=0"}


def downloadItem(url, attempts = 5, sleepTime = 3):
    """
    Recursive function to download yahoo url and isolate json
    Or write to errorFile
    """
    item = None
    try:
        #sleep(sleepTime)
        req = Request(url, headers=headers)
        html = urlopen(req)
        parser = BeautifulSoup(html,"lxml")

        for line in parser.text.split("\n"):
            if "root.App.main" in line:
                item = json.loads(";".join(line.split("root.App.main = ")[1].split(";")[:-1]))

    except (error.URLError, error.HTTPError, IncompleteRead) as e:
        msg = ""
        if hasattr(e,'code'):
            print (e.code)
            msg+= str(e.code)
        if hasattr(e,'reason'):
            print (e.reason)
            msg+=" "+str(e.reason)
        writeErrorMsg("downloads", url, msg)
    return item


def writeErrorMsg(fileName, url, msg):
    """
    Writes error message to error file
    """
    formating = {"timestamp":datetime.datetime.today().timestamp(),
                    "msg":msg, "url":url}
    errorPath = ENV.getErrorPath(fileName)
    print("Writing to Error File")
    with open(errorPath, "a+") as errorFile:
        print("{0[timestamp]}   {0[url]}   {0[msg]}\n".format(formating))
        errorFile.write("{0[timestamp]}\t{0[url]}\t{0[msg]}\n".format(formating))


################################################################################
################################################################################


class DownloadManager:

    def __init__(self):
        self.manager = {}

        try:
            with open(ENV.getManagerFile()) as fileIn:
                self.manager = json.load(fileIn)
        except FileNotFoundError:
            pass


    def update(self):
        update = False
        today = datetime.today()
        checkDate = self.checkManager("gameResults")

        try:
            checkDate = datetime.strptime(checkDate, "%Y-%m-%d %H:%M:%S.%f")
            if (date.fromtimestamp(today.timestamp()) - date.fromtimestamp(checkDate.timestamp())).days >= 1 and today.hour > 5:
                update = True
        except TypeError:
            update = True
            # Change to largest date in file system
            checkDate = datetime(2019,3,20)

        if update:
            self.getGameDates(date.fromtimestamp(checkDate.timestamp()), date.fromtimestamp(today.timestamp()))
            self.getMatchups(date.fromtimestamp(today.timestamp()))
            self.updateManager("gameResults", str(today))
            self.writeManager()



    def updateManager(self, item, value):
        self.manager[item] = value


    def writeManager(self):
        with open(ENV.getManagerFile(), "w") as fileOut:
            json.dump(self.manager, fileOut)


    def checkManager(self, item):
        return self.manager.get(item, None)



    def _getGameData(self, gameDate, endDate, scoreFunc=None, itemType=None):
        while gameDate < endDate:
            scoreboard = ScoreBoard(gameDate)
            if scoreFunc:
                for data in scoreFunc(scoreboard):
                    itemType(gameDate, data)
            gameDate += timedelta(1)


    # Change Method name to gare result
    def getGameDates(self, startDate, endDate):
        self._getGameData(startDate, endDate, ScoreBoard.getGameUrls, BoxScore)



    def getMatchups(self, startDate):
        gameDate = startDate
        endDate = startDate + timedelta(3)
        self._getGameData(startDate, endDate)


    def getPlayer(self, playerId):
        player = Player(playerId)
        player.downloadHeadshot()


################################################################################
################################################################################


class RecordableItem(metaclass=ABCMeta):
    """
    This is an abstract class that handles download, parsing, saving
    Borrows from p270  of Python Cookbook
    """

    _fields = []

    def __init__(self, *args):
        if len(args) != len(self._fields):
            raise TypeError("Expected {} arguments".format(len(self._fields)))

        for name, value in zip(self._fields, args):
            setattr(self, name, value)

        self.filePath = None
        self.info = {}

        self.setFilePath()
        if self.downloadCondition():
            self.parseData()
        if self.writeCondition():
            self.saveToFile()


    @abstractmethod
    def downloadCondition(self):
        return not os.path.exists(self.filePath)


    def getInfo(self):
        return self.info


    @abstractmethod
    def parseData(self):
        pass


    def saveToFile(self):
        fileBase = os.sep.join(self.filePath.split(os.sep)[:-1])
        if not os.path.exists(fileBase):
            ENV.createFilePath(fileBase)
        if self.info == {}:
            writeErrorMsg("download", self.url, self.gameDate)
        else:
            with open(self.filePath, "w") as fileOut:
                json.dump(self.info, fileOut)


    @abstractmethod
    def setFilePath(self):
        pass


    @abstractmethod
    def writeCondition(self):
        return True


################################################################################
################################################################################


class ScoreBoard(RecordableItem):

    _fields = ["gameDate", "url"]

    newGame = {"away_id":-1,
                "home_id":-1,
                "game_id":-1,
                "odds":None,
                "starters":None,
                "game_time":None,
                "status":None,
                "url":None}

    def __init__(self, gameDate):
        super().__init__(gameDate, ENV.getScoreBoardUrl(gameDate))


    def downloadCondition(self):
        return True


    def getGameUrls(self):
        return [game["url"] for game in self.info["games"]]


    def parseData(self):
        data = downloadItem(self.url)
        self.info["games"] = []
        for game in [game for key, game in data["context"]["dispatcher"]["stores"]["GamesStore"]["games"].items() if "mlb" in key and game["game_type"] != "Preseason" and game["status_type"] == "final" ]:
            gameData = ScoreBoard.newGame.copy()
            gameData["away_id"] = game["away_team_id"].split(".")[-1]
            gameData["home_id"] = game["home_team_id"].split(".")[-1]
            gameData["game_id"] = game["gameid"].split(".")[-1]
            gameData["odds"] = game.get("odds", {})
            gameData["starters"] = {"home":None, "away":None}
            if game.get("starting_pitchers", None):
                for homeAway in ("home", "away"):
                    if game["starting_pitchers"].get("{}_pitcher".format(homeAway), None):
                        gameData["starters"][homeAway] = game["starting_pitchers"]["{}_pitcher".format(homeAway)]["player_id"].split(".")[-1]
            gameData["game_time"] = game["start_time"].split()[-2:]
            gameData["status"] = game["status_type"]
            gameData["url"] = game["navigation_links"]["boxscore"]["url"]

            self.info["games"].append(gameData)



    def setFilePath(self):
        self.filePath = ENV.getPath("scoreboard", gameDate=self.gameDate)


    def writeCondition(self):
        return self.info.get("games", None)


################################################################################
################################################################################


class BoxScore(RecordableItem):

    _fields = ["gameDate", "gameId", "url"]

    newLineup = {"player_type":"N/A",
                    "order": -1,
                    "player_id":-1,
                    "position": [],
                    "sub_order":-1}

    def __init__(self, gameDate, url):
        gameId = url.split("-")[-1].strip("/")
        super().__init__(gameDate, gameId, ENV.mainUrl + url)


    def downloadCondition(self):
        return super().downloadCondition()


    def parseData(self):
        data = downloadItem(self.url)
        pageData = data["context"]["dispatcher"]["stores"]["PageStore"]["pageData"]
        # used as key in GamesStore
        dataIndex = pageData["entityId"]
        gameData = data["context"]["dispatcher"]["stores"]["GamesStore"]["games"][dataIndex]

        self.info["game_id"] = self.gameId
        self.info["season"] = self.gameDate.year
        self.info["game_date"] = float("{}.{}".format(*str(self.gameDate).split("-")[1:]))
        self.info["title"] = pageData["title"]
        self.info["away_id"] = pageData["entityData"]["awayTeamId"].split(".")[-1]
        self.info["home_id"] = pageData["entityData"]["homeTeamId"].split(".")[-1]
        self.info["away_stat_line"] = gameData["away_team_stats"]
        self.info["home_stat_line"] = gameData["home_team_stats"]

        ####### lineups
        self.info["lineups"] = {"home":{}, "away":{}}
        for homeAway in ("home", "away"):
            self.info["lineups"][homeAway] = {"B":[], "P":[]}
            for playerType in ("B", "P"):
                try:
                    for playerValue in gameData["lineups"]["{}_lineup".format(homeAway)][playerType].values():
                        newLineup = BoxScore.newLineup.copy()
                        newLineup["player_type"] = playerType
                        newLineup["order"] = playerValue["order"]
                        newLineup["player_id"] = playerValue["player_id"].split(".")[-1]
                        newLineup["sub_order"] = playerValue["suborder"]
                        newLineup["position"] = playerValue["position"].split("-")
                        self.info["lineups"][homeAway][playerType].append(newLineup)
                except (TypeError, KeyError):
                    pass
        ################

        try:
            self.info["umpires"] = gameData["game_details"]["g.umpires"]["text"]
            self.info["weather"] = gameData["game_details"]["g.weather"]["text"]
            self.info["wind"] = gameData["game_details"]["g.wind"]["text"]
        except KeyError:
            pass

        self.info["url"] = pageData["url"]
        try:
            self.info["winner_id"] = gameData["winning_team_id"].split(".")[-1]
            self.info["loser_id"] = self.info["away_id"] if self.info["winner_id"] == self.info["home_id"] else self.info["home_id"]
        except AttributeError:
            pass

        try:
            self.info["season_type"] = gameData["series_type"]
        except KeyError:
            pass

        self.info["stadium_id"] = gameData["stadium_id"]

        try:
            self.info["pitches"] = gameData["pitches"]
            self.info["play_by_play"] = gameData["play_by_play"]
        except KeyError:
            pass


    def setFilePath(self):
        self.filePath = ENV.getPath("boxscore", fileName=self.gameId, gameDate=self.gameDate)




    def writeCondition(self):
        return self.info != {}


################################################################################
################################################################################


class Player(RecordableItem):

    _fields = ["playerId", "url"]

    newPlayer = {"player_id":-1,
                "first_name":"N/A",
                "last_name":"N/A",
                "pos":-1,
                "height": -1,
                "weight": -1,
                "bats":None,
                "throws":None,
                "rookie_season":-1,
                "birth_year":-1,
                "birth_day":0.0}

    def __init__(self, playerId):
        super().__init__(playerId, ENV.getPlayerUrl(playerId))


    def downloadCondition(self):
        return super().downloadCondition()


    def downloadHeadshot(self):
        imagePath = self.info["image"]
        headShotPath = ENV.getPath("headshot", fileName=self.playerId)
        if not os.path.exists(headShotPath):
           req = Request(imagePath, headers=headers)
           html = urlopen(req)
           with open(headShotPath, "wb") as fileOut:
               fileOut.write(html.read())



    def parseData(self):
        data = downloadItem(self.url)["context"]["dispatcher"]["stores"]["PlayersStore"]["players"]["mlb.p.{}".format(self.playerId)]

        self.info = Player.newPlayer.copy()
        self.info["player_id"] = self.playerId
        self.info["first_name"] = data["first_name"]
        self.info["last_name"] = data["last_name"]
        self.info["pos"] = data["primary_position_id"].split(".")[-1]
        self.info["height"] = data["bio"]["height"]
        self.info["weight"] = data["bio"]["weight"]
        self.info["bats"] = data["bat"]
        self.info["throws"] = data ["throw"]
        self.info["rookie_season"] = data["bio"]["rookie_season"]
        birthday = data["bio"]["birth_date"]
        self.info["birth_year"] = int(birthday.split("-")[0])
        self.info["birth_day"] = float("{}.{}".format(*birthday.split("-")[1:]))



    def setFilePath(self):
        self.filePath = ENV.getPath("player", fileName=self.playerId)


    def writeCondition(self):
        return self.info != {}


################################################################################
################################################################################


class Roster(RecordableItem):

    _fields = ["teamId", "url"]


    def __init__(self, teamId):
        super().__init__(teamId, ENV.getRosterUrl(teamId))


    def downloadCondition(self):
        return True


    def parseData(self):
        data = downloadItem(self.url)["context"]["dispatcher"]["stores"]["PlayersStore"]
        self.info["pitchers"] = []
        self.info["batters"] = []
        for player in [player for player in data["players"].values() if player["team_id"] == "mlb.t.{}".format(self.teamId) and not player.get("injury", None)]:
            if "mlb.pos.1" in player["positions"].values():
                self.info["pitchers"].append(player["player_id"].split(".")[-1])
            else:
                self.info["batters"].append(player["player_id"].split(".")[-1])


    def setFilePath(self):
        pass


    def writeCondition(self):
        return False


################################################################################
################################################################################
