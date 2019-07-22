import os
import json
import datetime

mainPath = os.environ["HOME"]+"{0[sep]}FEFelson{0[sep]}MLBProjections{0[sep]}"
mainUrl = "https://sports.yahoo.com"
scoreBoardUrl = "/mlb/scoreboard/?confId=&schedState=2&dateRange={}-{}-{}"
playerUrl = "/mlb/players/{}/"
rosterUrl = "/mlb/teams/{}/roster/"



def getJsonInfo(filePath):
    with open(filePath) as fileIn:
        info = json.load(fileIn)
    return info


def writeJsonInfo(filePath):
    with open(filePath, "w") as fileOut:
        json.dump(info, fileOut)


def getRosterUrl(teamId):
    slugId = None
    with open(mainPath.format({"sep":os.sep})+"Teams/{}.json".format(teamId)) as fileIn:
        slugId = json.load(fileIn)["slugId"]
    return mainUrl + rosterUrl.format(slugId)


def yearMonthDay(startDate=None):
    if not startDate:
        startDate = datetime.date(2016,4,3)
    endDate = datetime.date.today()
    pbpPath = getPath("boxscore").strip("None.json")

    while endDate > startDate:
        year,month,day = str(startDate).split("-")
        if os.path.isdir(pbpPath+year+"/"+month+"/"+day):
            yield pbpPath+year+"/"+month+"/"+day+"/"
        startDate += datetime.timedelta(1)


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
                    "logo":"Teams/Logos",
                    "g-logo":"Teams/Logos",
                    "stadium":"Stadiums",
                    "boxscore":"PlayByPlay",
                    "matchup":"PlayByPlay",
                    "roster":"Teams/Rosters",
                    "game":"Games"}.get(item, None)


    if folderPath:
        newPath += folderPath+"{0[sep]}"

    filePath = {"scoreboard": "scoreboard.json",
                "headshot": "{0[fileName]}.png",
                "database": "{0[fileName]}.db",
                "matchup": "M{0[fileName]}.json",
                "logo": "{0[fileName]}.png",
                "g-logo": "G{0[fileName]}.png",
                "game": "{0[fileName]}.db"}.get(item, "{0[fileName]}.json")

    if gameDate:
        gameDate = str(gameDate).split("-")
        newPath += "{0[sep]}".join([x for x in gameDate])+"{0[sep]}"

    newPath = (newPath+filePath).format({"sep":os.sep, "fileName": fileName})

    print("File Path- "+newPath+"\n")
    return newPath


def getProjPath(gameId):
    return mainPath.format({"sep": os.sep})+"Projections/{}.json".format(gameId)
