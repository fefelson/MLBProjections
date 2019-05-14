import os

mainPath = os.environ["HOME"]+"{0[sep]}FEFelson{0[sep]}"


def getManagerFile():
    managerPath = (mainPath + ".proj_manager.json").format({"sep":os.sep})
    print("ManagerPath - "+managerPath+"\n")
    return managerPath


def getPath(item, *, fileName=None, gameDate=None):
    #items = "player", "scoreboard", "boxscore", "database", "team", "matchup"
    newPath = mainPath + "MLBProjections{0[sep]}"
    folder = {"database": None, "player":"Players", "team":"Teams"}.get(item, "BoxScores")
    filePath = {"matchup": "{0[fileName]}.json",
                "scoreboard": "scoreboard.json",
                "database": "{0[fileName]}.db"}.get(item, "{0[fileName]}.json")
    if folder:
        newPath += "{0[folder]}{0[sep]}"
    if gameDate:
        newPath += "{0[sep]}".join([x for x in gameDate])+"{0[sep]}"
    newPath = (newPath+filePath).format({"sep":os.sep, "fileName": fileName, "folder": folder})
    print("File Path- "+newPath+"\n")
    return newPath


def getMatchupPath(gameDate):
    gd = str(gameDate).split("-")
    return mainPath.format({"sep": os.sep})+"/MLBProjections/Matchups/{}.json".format("".join(gd))


def getLineupPath(gameDate):
    gd = str(gameDate).split("-")
    return mainPath.format({"sep": os.sep})+"/MLBProjections/Lineups/{}.json".format("".join(gd))



def getProjPath(gameId):
    return mainPath.format({"sep": os.sep})+"/MLBProjections/Projections/{}.json".format(gameId)


def getGamePaths():
    gamePaths = []
    for gamePath in os.listdir(filePath):
        gamePaths.append(filePath+gamePath)
    return gamePaths
