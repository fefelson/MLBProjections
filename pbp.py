import os
import json
from bs4 import BeautifulSoup
from pprint import pprint
from urllib.request import urlopen, Request
from urllib.error import HTTPError
from datetime import date, timedelta

gameKeys = ("away_team_id", "gameid", "home_team_id", "lineups", "odds",
            "pitches", "play_by_play", "stadium", "stadium_id", "winning_team_id")


startDate = date(2019,5,13)
endDate = date.today()

mainUrl = "https://sports.yahoo.com"
scoreboardUrl = "/mlb/scoreboard/?confId=&schedState=2&dateRange={}-{}-{}"
filePath = os.environ["HOME"] + "/Desktop/Baseball/{}.json"
errorPath = os.environ["HOME"] + "/Desktop/Baseball/error.log"

headers = {"Host": "sports.yahoo.com",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0",
            "Connection": "close",
            "Cache-Control": "max-age=0"}


while startDate < endDate:
    print(startDate)
    req = Request(mainUrl+scoreboardUrl.format(*str(startDate).split("-")), headers=headers)
    html = urlopen(req)
    parser = BeautifulSoup(html,"lxml")

    urls = []
    for line in parser.text.split("\n"):
        #line = str(line)    
        if "root.App.main" in line:
            
            
            line = ";".join(line.split("root.App.main = ")[1].split(";")[:-1])
        
            urls = [ y["navigation_links"]["boxscore"]["url"] for y in json.loads(line)["context"]["dispatcher"]["stores"]["GamesStore"]["games"].values() if y["status_type"] == "final" and y["game_type"] != "Preseason"]
    ##        x = json.loads(line)["context"]["dispatcher"]["stores"]["GamesStore"]["games"]
    ##            x = json.loads(line.split("root.App.main = ")[-1].split(";\n")[0])["context"]["dispatcher"]["stores"]

    for url in urls:
        try:
            print(mainUrl+url)
            gameId = url.split("-")[-1].strip("/")
            req = Request(mainUrl+url, headers=headers)
            html = urlopen(req)
            parser = BeautifulSoup(html, "lxml")



            gameJson = {}
            for line in parser.text.split("\n"):
                #line = str(line)    
                if "root.App.main" in line:
                    
                    
                    line = ";".join(line.split("root.App.main = ")[1].split(";")[:-1])
                
                    x = json.loads(line.split("root.App.main = ")[-1].split(";\n")[0])["context"]["dispatcher"]["stores"]
##                    for key,value in x.items():
##                        if key != "GamesStvore":
##                            print(key,"\n")
##                            pprint(value)
##                            print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
##                            
##                    raise AssertionError
                    gameJson["game"] = x["PageStore"]["pageData"]
                    gameJson["players"] = x["PlayersStore"]["players"]
                    gameJson["teams"] = [team for team in x["TeamsStore"]["teams"].values() if "mlb" in team["team_id"]]
                    for key in gameKeys:
                        try:
                            gameJson[key] = x["GamesStore"]["games"]["mlb.g.{}".format(gameId)][key]
                        except KeyError:
                            pass

            with open(filePath.format(gameId),"w") as fileOut:
                json.dump(gameJson, fileOut)
        except HTTPError:
            print("ERROR")
            with open(errorPath, "a") as errorFile:
                errorFile.write(mainUrl+url)
    startDate = startDate+ timedelta(1)
    print("\n")

