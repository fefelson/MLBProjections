import os
import json

mainPath = os.environ["HOME"]+"{0[sep]}FEFelson{0[sep]}MLBProjections{0[sep]}"
mainUrl = "https://sports.yahoo.com"
scoreBoardUrl = "/mlb/scoreboard/?confId=&schedState=2&dateRange={}-{}-{}"
playerUrl = "/mlb/players/{}/"
rosterUrl = "/mlb/teams/{}/roster/"


def getRosterUrl(teamId):
    slugId = None
    with open(mainPath.format({"sep":os.sep})+"/Teams/{}.json".format(teamId)) as fileIn:
        slugId = json.load(fileIn)["slugId"]
    return mainUrl + rosterUrl.format(slugId)


def yearMonthDay():
    pbpPath = getPath("boxscore").strip("None.json")
    for year in [year for year in os.listdir(pbpPath) if os.path.isdir(pbpPath+year)]:
        for month in [month for month in os.listdir(pbpPath+year) if os.path.isdir(pbpPath+year+"/"+month)]:
            for day in [day for day in os.listdir(pbpPath+year+"/"+month) if os.path.isdir(pbpPath+year+"/"+month+"/"+day)]:
                yield pbpPath+year+"/"+month+"/"+day+"/"


def getErrorPath(fileName):
    return mainPath.format({"sep":os.sep})+fileName+".err"


def getManagerFile():
    return mainPath.format({"sep":os.sep})+".manager.json"


def createFilePath(filePath):
    print("Creating path - {}".format(filePath))
    os.makedirs(filePath)

def getPlayerUrl(playerId):
    return mainUrl+playerUrl.format(playerId)


def getScoreBoardUrl( gameDate):
    gameDate = str(gameDate).split("-")
    return mainUrl+scoreBoardUrl.format(*gameDate)



def getPath(item, *, fileName=None, gameDate=None):
    newPath = mainPath
    folderPath = {"scoreboard":"PlayByPlay",
                    "headshot":"Players{0[sep]}Headshots",
                    "player":"Players",
                    "team":"Teams",
                    "stadium":"Stadiums",
                    "boxscore":"PlayByPlay",
                    "roster":"Teams/Rosters",
                    "game":"Games"}.get(item, None)


    if folderPath:
        newPath += folderPath+"{0[sep]}"

    filePath = {"scoreboard": "scoreboard.json",
                "headshot": "{0[fileName]}.png",
                "database": "{0[fileName]}.db",
                "game": "{0[fileName]}.db"}.get(item, "{0[fileName]}.json")

    if gameDate:
        gameDate = str(gameDate).split("-")
        newPath += "{0[sep]}".join([x for x in gameDate])+"{0[sep]}"

    newPath = (newPath+filePath).format({"sep":os.sep, "fileName": fileName})

    print("File Path- "+newPath+"\n")
    return newPath


def getMatchupPath(gameDate):
    gd = str(gameDate).split("-")
    return mainPath.format({"sep": os.sep})+"/MLBProjections/Matchups/{}.json".format("".join(gd))


def getLineupPath(gameDate):
    gd = str(gameDate).split("-")
    return mainPath.format({"sep": os.sep})+"Lineups/{}.json".format("".join(gd))



def getProjPath(gameId):
    return mainPath.format({"sep": os.sep})+"Projections/{}.json".format(gameId)


def getGamePaths():
    gamePaths = []
    for gamePath in os.listdir(filePath):
        gamePaths.append(filePath+gamePath)
    return gamePaths
