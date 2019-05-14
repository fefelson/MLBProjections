import json
import os
import sqlite3
import MLBProjections.MLBProjections.DB.MLB as MLB
import MLBProjections.MLBProjections.Models.ScoreKeeper as SB

from collections import Counter
from pprint import pprint
from urllib.request import urlopen, Request



def getLocation(db, pitch):
    locationId = -1
    try:
        x = pitch["horizontal"]
        y = pitch["vertical"]
        locationId = db.curs.execute("SELECT location_id FROM locations WHERE x_value = ? AND y_value = ?",(x,y)).fetchone()[0]
    except KeyError:
        pass
    return locationId
##
##
##
##for pitch in Pitch.pitchLocations:
##    if Pitch.sortingHat(*pitch) == 1:
##        x = round(pitch[0]/1667) + 11
##        y = round(pitch[1]/1667) - 11
##        print(pitch[0], x, abs((x + (4-(x%4)))/4))
##        print(pitch[1], y, abs((y + (4-(y%4)))/4))
##        print("\n\n")


filePath = os.environ["HOME"] + "/Desktop/Baseball/"
headShotPath = os.environ["HOME"]+"/Desktop/Baseball/Headshots/{}.png"
headers = headers = {"Host": "s.yimg.com",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br"
            }

x = MLB.MLBDatabase()
x.openDB()

gameStats = {}
for gamePath in os.listdir(filePath):
    try:
        with open(filePath+gamePath) as fileIn:
            gameStats = json.load(fileIn)
            
            

    ##    for value in gameStats["players"].values():
    ##        imagePath = value.get("image", None)
    ##        
    ##        if imagePath:
    ##            playerId = imagePath.split("/")[-1].split(".")[0]
    ##            print(playerId)
    ##            if not os.path.exists(headShotPath.format(playerId)):
    ##                req = Request(imagePath, headers=headers)
    ##                html = urlopen(req)
    ##                with open(headShotPath.format(playerId), "wb") as fileOut:
    ##                    fileOut.write(html.read())
    ##        
                

        for team in gameStats["teams"]:
            teamId = team["team_id"].split(".")[-1]
            abrv = team["abbr"]
            city = team["first_name"]
            mascot = team["last_name"]

            try:
                x.insert(MLB.proTeamsTable, (teamId, abrv, city, mascot))
            except sqlite3.IntegrityError:
                pass

        for player in gameStats["players"].values():
            playerId = player["player_id"].split(".")[-1]
            firstName = player["first_name"]
            lastName = player["last_name"]
            bats = player["bat"]
            throws = player["throw"]
            try:
                x.insert(MLB.proPlayersTable, (playerId, firstName, lastName, bats, throws))
            except sqlite3.IntegrityError:
                pass
        gameId = gameStats["gameid"].split(".")[-1]
        for pitch in gameStats["pitches"].values():
            try:
                locationId = getLocation(x, pitch)
                pitchNum = pitch["play_num"]
                pitcherId = pitch["pitcher"]
                batterId = pitch["batter"]
                pitchTypeId = pitch.get("pitch_type", 7)
                pitchVelocity = pitch.get("velocity", -1)
                balls = pitch["balls"]
                strikes = pitch["strikes"]
                pitchResultId = pitch["result"]
                try:
                    x.insert(MLB.pitchsTable, (gameId, pitchNum, pitcherId, batterId, locationId, pitchTypeId, pitchVelocity, balls, strikes, pitchResultId))
                except sqlite3.IntegrityError:
                    pass
            except:
                pprint(pitch)
                raise AssertionError

            

        game = gameStats["game"]
        gD = game["title"].split("|")[1].strip().split("-")
        

        homeId = game["entityData"]["homeTeamId"].split(".")[-1]
        awayId = game["entityData"]["awayTeamId"].split(".")[-1]
        winnerId = gameStats["winning_team_id"].split(".")[-1]
        loserId = homeId if awayId == winnerId else awayId
        season = gD[0]
        gameDate = ".".join(gD[1:])
        seasonType = "all"
        stadiumId = gameStats["stadium_id"]

        items = (gameId, homeId, awayId, winnerId, loserId, season, gameDate, seasonType, stadiumId)

        try:
            x.insert(MLB.gamesTable, items)
        except sqlite3.IntegrityError:
            pass

        
        stadiumId = gameStats["stadium_id"]
        title = gameStats["stadium"]
        try:
            x.insert(MLB.stadiumsTable, (stadiumId, title))
        except sqlite3.IntegrityError:
            pass


        for play in gameStats["play_by_play"].values():
            if play["play_type"] == "RESULT" and play["ball_hit"] == "1":
                batterId = play["batter"]
                pitcherId = play["pitcher"]
                hitAngle = play["hit_angle"]
                hitDist = play["hit_distance"]
                hitHard = play["hit_hardness"]
                hitStyle = play["hit_style"]
                try:
                    contactId = x.curs.execute("SELECT contact_type_id FROM contact_types WHERE hit_angle = ? AND hit_distance = ? AND hit_hardness = ? AND hit_style = ?",(hitAngle, hitDist, hitHard, hitStyle)).fetchone()[0] 
                except TypeError:
                    contactId = x.curs.execute("SELECT COUNT(contact_type_id) FROM contact_types").fetchone()[0] +1
                    x.insert(MLB.contactTypeTable, (contactId, hitAngle, hitDist, hitHard, hitStyle))
                text = SB.manageText(play["text"])
                try:
                    resultId = x.curs.execute("SELECT hit_result_id FROM hit_results WHERE result_tag = ?", (text,)).fetchone()[0]
                except TypeError:
                    resultId = -1
                try:
                    x.insert(MLB.resultTable, (gameId, play["play_num"], batterId, pitcherId, contactId, resultId))
                except sqlite3.IntegrityError:
                    pass

        for item in gameStats["lineups"]["away_lineup"]["B"].values():
            order = item["order"]
            subOrder = item["suborder"]
            pos = item["position"]
            playerId = item["player_id"].split(".")[-1]

            try:
                x.insert(MLB.lineupTable, (gameId, awayId, playerId, order, subOrder, pos))
            except sqlite3.IntegrityError:
                pass


        for item in gameStats["lineups"]["home_lineup"]["B"].values():
            order = item["order"]
            subOrder = item["suborder"]
            pos = item["position"]
            playerId = item["player_id"].split(".")[-1]

            try:
                x.insert(MLB.lineupTable, (gameId, homeId, playerId, order, subOrder, pos))
            except sqlite3.IntegrityError:
                pass


        for player in gameStats["players"].values():
            if player["team_id"].split(".")[-1] in (homeId, awayId):
                playerId = player["player_id"].split(".")[-1]
                teamId = player["team_id"].split(".")[-1]
                try:
                    x.insert(MLB.rosterTable, (gameId, playerId, teamId))
                except sqlite3.IntegrityError:
                    pass

    
                
 
        
    except json.decoder.JSONDecodeError:
        print(gamePath)
    except IsADirectoryError:
        print(gamePath)
    except KeyError:
        print(gamePath)
x.commit()

##pitcherId = 8180
##balls = 0
##strikes = 0
##bats = "R"
##pitchTitle = ""
##
##print(x.curs.execute("SELECT first_name, last_name, throws FROM pro_players WHERE player_id = ?",(pitcherId,)).fetchone())
##
##pitchTypes = [y[0] for y in x.curs.execute("SELECT pitch_type_id FROM pitchs WHERE pitcher_id = ? AND balls = ? AND strikes = ?",(pitcherId, 0, 2)).fetchall()]
##pitchCount = Counter(pitchTypes)
##for key, value in pitchCount.items():
##    title = x.curs.execute("SELECT title FROM pitch_types WHERE player_type_id = ?",(key,)).fetchone()[0]
##    print("{}: {}%".format(title,int(value/len(pitchTypes)*100)))
##
##pitchLocations = [y[0] for y in x.curs.execute("SELECT box FROM locations INNER JOIN pitchs ON locations.location_id = pitchs.location_id INNER JOIN pro_players AS batter ON pitchs.batter_id = batter.player_id WHERE pitcher_id = ? AND balls = ? AND strikes = ? AND batter.bats = ?",(pitcherId, 0, 0, "L")).fetchall()]
##pitchCount = Counter(pitchLocations)
##
##for y in range(5):
##    row = [pitchCount[(y*5)+x] for x in range(1,6)]
##    rowFormat = ["{:2d}%".format(int(pitchCount.get(i,0))) for i in row]
##    print(rowFormat)
##        
##    
##    
##    
x.closeDB()


