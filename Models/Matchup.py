import itertools

from pprint import pprint

################################################################################
################################################################################





################################################################################
################################################################################


class Matchup:

    def __init__(self, info):

        self.gameId = info["gameId"]
        self.season = info["season"]
        self.gameDate = info["gameDate"]
        self.gameTime = info["gameTime"]
        self.league = None
        self.teams = {"home":info["home"], "away":info["away"]}
        self.changeObservers = []
        self.setObservers = []

        for homeAway in ("home", "away"):
            self.teams[homeAway]["teamId"] = info[homeAway]["teamId"]


    def getPlayerIds(self):
        playerIds = []
        for homeAway in ("home", "away"):
            for player in itertools.chain(self.teams[homeAway]["roster"]["batters"], self.teams[homeAway]["roster"]["pitchers"]):
                playerIds.append(player["playerId"])
        return playerIds


    def newLineup(self, info):
        for homeAway in ("home", "away"):
            self.teams[homeAway]["starter"] = info[homeAway]["starter"]
            lineup = []
            for player in info[homeAway]["lineup"]:
                lineup.append((player["playerId"], player["firstName"], player["lastName"], player["pos"]))
            self.teams[homeAway]["lineup"] = lineup
        self.notifyOnChange()


    def setLeague(self, league):
        self.league = league


    def setTeamInfo(self, homeAway, key, info):
        self.teams[homeAway][key] = info


    def notifyOnChange(self):
        for observer in self.changeObservers:
            observer.notify(self.getInfo())


    def notifyOnSet(self):
        for observer in self.setObservers:
            observer.onSet()


    def registerChangeObserver(self, observer):
        self.changeObservers.append(observer)
        observer.notify(self.getInfo())


    def registerOnSetObserver(self, observer):
        self.setObservers.append(observer)


    def getGameId(self):
        return self.gameId


    def getInfo(self):
        info = {"gameId": self.gameId,
                "league": self.league,
                "gameTime": self.gameTime,
                "teams":self.teams}
        return info


################################################################################
################################################################################
