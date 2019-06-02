import os
import json
import sqlite3

from itertools import chain

from . import Database as DB
from ..Models.GameRecord import GameRecord
import MLBProjections.MLBProjections.Environ as ENV

# for debugging
from pprint import pprint

################################################################################
################################################################################


gamesTable = {
                "tableName": "games",
                "tableCols": ("game_id", "home_id", "away_id", "winner_id",
                                "loser_id", "season", "game_date", "season_type",
                                "stadium_id"),
                "tableCmd": """
                            game_id INT PRIMARY KEY,
                            home_id INT NOT NULL,
                            away_id INT NOT NULL,
                            winner_id INT NOT NULL,
                            loser_id INT NOT NULL,
                            season INT NOT NULL,
                            game_date REAL NOT NULL,
                            season_type TEXT,
                            stadium_id INT  NOT NULL,
                            FOREIGN KEY (home_id) REFERENCES pro_teams (team_id),
                            FOREIGN KEY (away_id) REFERENCES pro_teams (team_id),
                            FOREIGN KEY (winner_id) REFERENCES pro_teams (team_id),
                            FOREIGN KEY (loser_id) REFERENCES pro_teams (team_id),
                            FOREIGN KEY (stadium_id) REFERENCES stadiums (stadium_id)
                            """,
                "indexes": (("seasons","season, game_date"),
                            ("stadium", "stadium_id, season, game_date"))
                }


proPlayersTable = {
                    "tableName": "pro_players",
                    "tableCols": ("player_id", "first_name", "last_name", "pos", "height",
                                    "weight", "bats", "throws", "rookie_season", "birth_year",
                                    "birth_day"),
                    "tableCmd": """
                                player_id INT PRIMARY KEY,
                                first_name TEXT NOT NULL,
                                last_name TEXT NOT NULL,
                                pos INT NOT NULL,
                                height INT,
                                weight INT,
                                bats TEXT NOT NULL,
                                throws TEXT NOT NULL,
                                rookie_season INT,
                                birth_year INT,
                                birth_day REAL
                                """,
                    "indexes": (("names","last_name, first_name"),
                                ("bat_side", "bats"),
                                ("pitch_arm", "throws"))
                    }


proTeamsTable = {
                    "tableName": "pro_teams",
                    "tableCols": ("team_id", "abrv", "city", "mascot", "league",
                                    "division", "color", "stadium_id"),
                    "tableCmd": """
                                team_id INT PRIMARY KEY,
                                abrv TEXT NOT NULL,
                                city TEXT NOT NULL,
                                mascot TEXT NOT NULL,
                                league TEXT NOT NULl,
                                division TEXT NOT NULL,
                                color TEXT,
                                stadium_id INT NOT NULL,
                                FOREIGN KEY (stadium_id) REFERENCES stadiums (stadium_id)
                                """
                }


stadiumsTable = {
                    "tableName": "stadiums",
                    "tableCols": ("stadium_id", "title"),
                    "tableCmd": """
                                stadium_id INT PRIMARY KEY,
                                title TEXT NOT NULL
                                """
                }


pitchTypesTable = {
                    "tableName": "pitch_types",
                    "tableCols": ("pitch_type_id", "title"),
                    "tableCmd": """
                                pitch_type_id INT PRIMARY KEY,
                                title TEXT NOT NULL
                                """
                    }


pitchResultsTable = {
                    "tableName": "pitch_results",
                    "tableCols": ("pitch_result_id", "title"),
                    "tableCmd": """
                                pitch_result_id INT PRIMARY KEY,
                                title TEXT NOT NULL
                                """
                    }


locationsTable = {
                    "tableName": "pitch_locations",
                    "tableCols": ("location_id", "x_value", "y_value", "box", "strike_zone"),
                    "tableCmd": """
                                location_id INT PRIMARY KEY,
                                x_value INT NOT NULL,
                                y_value INT NOT NULL,
                                box INT NOT NULL,
                                strike_zone TEXT NOT NULL
                                """,
                    "indexes": (("values", "x_value, y_value"),)
                    }


pitchesTable = {
                    "tableName": "pitches",
                    "tableCols": ("pitch_id", "game_id", "play_num", "pitcher_id", "batter_id",
                                    "pitch_num", "pitch_type_id", "velocity", "location_id",
                                    "balls", "strikes", "pitch_result_id"),
                    "tableCmd": """
                                pitch_id INT PRIMARY KEY,
                                game_id INT NOT NULL,
                                play_num INT NOT NULL,
                                pitcher_id INT NOT NULL,
                                batter_id INT NOT NULL,
                                pitch_num INT NOT NULL,
                                pitch_type_id INT NOT NULL,
                                velocity INT NOT NULL,
                                location_id INT NOT NULL,
                                balls INT NOT NULL,
                                strikes INT NOT NULL,
                                pitch_result_id INT NOT NULL,
                                FOREIGN KEY (game_id) REFERENCES games (game_id),
                                FOREIGN KEY (pitcher_id) REFERENCES pro_players (player_id),
                                FOREIGN KEY (batter_id) REFERENCES pro_players (player_id),
                                FOREIGN KEY (pitch_type_id) REFERENCES pitch_types (pitch_type_id),
                                FOREIGN KEY (location_id) REFERENCES locations (location_id),
                                FOREIGN KEY (pitch_result_id) REFERENCES pitch_results (pitch_result_id)
                                """,
                    "indexes": (("pitcher_pitches", "pitcher_id, pitch_type_id, location_id, velocity"),
                                ("pitcher_count", "pitcher_id, balls, strikes"),
                                ("batter_pitches", "batter_id, pitch_type_id, location_id, velocity"),
                                ("batter_count", "batter_id, strikes, balls"))
                }


contactTypesTable = {
                        "tableName": "contacts",
                        "tableCols": ("contact_id", "pitch_id", "hit_style", "hit_hardness",
                                        "hit_angle", "hit_distance"),
                        "tableCmd": """
                                    contact_id INT PRIMARY KEY,
                                    pitch_id INT NOT NULL,
                                    hit_style INT NOT NULL,
                                    hit_hardness INT NOT NULL,
                                    hit_angle INT NOT NULL,
                                    hit_distance INT NOT NULL,
                                    FOREIGN KEY (pitch_id) REFERENCES pitches (pitch_id)
                                    """,
                        "indexes": (("hits", "hit_style, hit_hardness, hit_angle, hit_distance"),
                                    ("contact_pitch", "pitch_id"))
                    }


resultTypesTable = {
                    "tableName": "result_types",
                    "tableCols": ("result_type_id", "title" ),
                    "tableCmd": """
                                result_type_id INT PRIMARY KEY,
                                title TEXT NOT NULL
                                """
                    }


atBatTypesTable = {
                    "tableName": "ab_types",
                    "tableCols": ("ab_type_id", "result_type_id", "is_ab", "on_base",
                                    "is_hit", "starting_base"),
                    "tableCmd":"""
                                ab_type_id INT PRIMARY KEY,
                                result_type_id INT NOT NULL,
                                is_ab INT NOT NULL,
                                on_base INT NOT NULL,
                                is_hit INT NOT NULL,
                                starting_base INT NOT NULL,
                                FOREIGN KEY (result_type_id) REFERENCES result_types (result_type_id)
                                """
                }


atBatResultsTable = {
                    "tableName": "ab_results",
                    "tableCols": ("ab_id", "game_id", "play_num", "pitch_id", "batter_id",
                                    "contact_id", "result_type_id", "stadium_id"),
                    "tableCmd": """
                                ab_id INT PRIMARY KEY,
                                game_id INT NOT NULL,
                                play_num INT NOT NULL,
                                pitch_id INT NOT NULL,
                                batter_id INT NOT NULL,
                                contact_id INT NOT NULL,
                                result_type_id INT NOT NULL,
                                stadium_id INT NOT NULL,
                                FOREIGN KEY (batter_id) REFERENCES pro_players (player_id),
                                FOREIGN KEY (contact_id) REFERENCES contacts (contact_id),
                                FOREIGN KEY (result_type_id) REFERENCES result_types (result_type_id),
                                FOREIGN KEY (stadium_id) REFERENCES stadiums (stadium_id)
                                """,
                    "indexes": (("game_play", "pitch_id"),
                                ("stadium_contact", "stadium_id, contact_id"))
}


pitchRemovalsTable = {
                        "tableName": "removals",
                        "tableCols": ("remove_id", "game_id", "pitcher_id", "runs", "pitch_num"),
                        "tableCmd": """
                                    remove_id INT PRIMARY KEY,
                                    game_id INT NOT NULL,
                                    pitcher_id INT NOT NULL,
                                    runs INT NOT NULL,
                                    pitch_num INT NOT NULL,
                                    FOREIGN KEY (game_id) REFERENCES games (game_id),
                                    FOREIGN KEY (pitcher_id) REFERENCES pro_players (player_id)
                                    """,
                    }


newPitchersTable = {
                        "tableName": "new_pitchers",
                        "tableCols": ("new_pitcher_id", "team_id", "game_id", "pitcher_id", "inning"),
                        "tableCmd": """
                                    new_pitcher_id INT PRIMARY KEY,
                                    team_id INT NOT NULL,
                                    game_id INT NOT NULL,
                                    pitcher_id INT NOT NULL,
                                    inning INT NOT NULL,
                                    FOREIGN KEY (game_id) REFERENCES games (game_id),
                                    FOREIGN KEY (team_id) REFERENCES pro_teams (team_id),
                                    FOREIGN KEY (pitcher_id) REFERENCES pro_players (player_id)
                                    """,
                    }


lineupsTable = {
                    "tableName": "lineups",
                    "tableCols": ("game_id", "team_id", "player_id", "batt_order", "sub_order", "pos" ),
                    "tableCmd": """
                                game_id INT NOT NULL,
                                team_id INT NOT NULL,
                                player_id INT NOT NULL,
                                batt_order INT NOT NULL,
                                sub_order INT NOT NULL,
                                pos TEXT NOT NULL,
                                PRIMARY KEY (game_id, team_id, player_id),
                                FOREIGN KEY (team_id) REFERENCES pro_teams (team_id),
                                FOREIGN KEY (player_id) REFERENCES pro_players (player_id)
                                """
}


rostersTable = {
                "tableName": "rosters",
                "tableCols": ("player_id", "team_id"),
                "tableCmd": """
                            player_id INT NOT NULL,
                            team_id INT NOT NULL,
                            PRIMARY KEY (player_id, team_id),
                            FOREIGN KEY (player_id) REFERENCES pro_players (player_id),
                            FOREIGN KEY (team_id) REFERENCES pro_teams (team_id)
                            """
}


bullpenTable = {
                "tableName": "bullpen",
                "tableCols": ("team_id", "player_id"),
                "tableCmd": """
                            team_id INT NOT NULL,
                            player_id INT NOT NULL,
                            PRIMARY KEY (player_id, team_id),
                            FOREIGN KEY (player_id) REFERENCES pro_players (player_id),
                            FOREIGN KEY (team_id) REFERENCES pro_teams (team_id)
                            """
}

starterTable = {
                "tableName": "starter",
                "tableCols": ("team_id", "player_id"),
                "tableCmd": """
                            team_id INT NOT NULL,
                            player_id INT NOT NULL,
                            PRIMARY KEY (player_id, team_id),
                            FOREIGN KEY (player_id) REFERENCES pro_players (player_id),
                            FOREIGN KEY (team_id) REFERENCES pro_teams (team_id)
                            """
}































pitchTypes = ((1,"Fastball"),
                (2,"Curveball"),
                (3,"Slider"),
                (4,"Changeup"),
                (6,"Knuckleball"),
                (7,"Unknown"),
                (8,"Split-Finger"),
                ("9","Cut Fastball"))


pitchResults = ((0,"Ball"),
                (1,"Called Strike"),
                (2,"Swinging Strike"),
                (3,"Foul Ball"),
                (5,"Bunt Foul"),
                (10,"In Play"))


                # title, is_ab, on_base, is_hit, starting_base
atBatResults = (("Ground Out", 1, 0, 0, 0),
                ("Strike Out", 1, 0, 0, 0),
                ("Single", 1, 1, 1, 1),
                ("Fly Out", 1, 0, 0, 0),
                ("Walk", 0, 1, 0, 1),
                ("Line Out", 1, 0, 0, 0),
                ("Double", 1, 1, 1, 2),
                ("Pop Out", 1, 0, 0, 0),
                ("Home Run", 1, 1, 1, 4),
                ("Fielder's Choice", 1, 0, 0, 1),
                ("Double Play", 1, 0, 0, 0),
                ("Fouled Out", 1, 0, 0, 0),
                ("Hit by Pitch", 0, 1, 0, 0),
                ("Reached on Error", 1, 0, 0, 1),
                ("Sacrifice", 0, 0, 0, 0),
                ("Triple", 1, 1, 1, 3),
                ("Reached on Interference", 0, 1, 0, 1),
                ("Triple Play", 1, 0, 0, 0),
                ("Out on Interference", 1, 0, 0, 0),
                ("Out of Order", 1, 0, 0, 0))


runnerResults = ("Stolen Base", "Wild Pitch", "Caught Stealing", "Passed Ball",
                    "Fielder's Indifference", "Picked Off", "Advanced on Error",
                    "Balk")


managerResults = ("Pitching Change", "Fielding Change", "Pinch Hitter", "Pinch Runner")


positionNumbers = {"pitcher":1, "catcher":2, "first":3, "second":4, "third":5,
                    "shortstop":6, "left":7, "center":8, "right":9}


valuesBase = (0,1667,3333, 5000, 6667, 8333, 10000, 11667, 13333, 15000, 16667)
values = list(valuesBase) + [ x*-1 for x in valuesBase if x ]
pitchLocations = []
for horizontal in values:
    for vertical in values:
        # append a tuple (valA, valB)
        pitchLocations.append((horizontal,vertical))


def sortingHat(horizontal, vertical):
    # find a box for the pitch location
    y = round(vertical/1667) - 11
    x = round(horizontal/1667) + 11

    yValue = _hat(abs(y))
    xValue = _hat(x)+1
    return (yValue *5) + xValue


def _hat(item):
    value = None
    if item <= 3:
        value = 0
    elif item <= 7:
        value = 1
    elif item <=12:
        value = 2
    elif item <= 16:
        value = 3
    else:
        value = 4
    return value


################################################################################
################################################################################


class MLBDatabase(DB.Database):

    def __init__(self):
        super().__init__(ENV.getPath("database", fileName="mlb"))
        #super().__init__("/home/ededub/Desktop/testDB.db")


    def getTableList(self):
        return (gamesTable, proPlayersTable, proTeamsTable, stadiumsTable, pitchTypesTable,
                pitchResultsTable, locationsTable, pitchesTable, contactTypesTable,
                resultTypesTable, atBatTypesTable, atBatResultsTable, pitchRemovalsTable,
                newPitchersTable, lineupsTable, rostersTable)


    def enterFileItems(self, itemType, itemTable):
        itemPath = ENV.getPath(itemType).strip("None.json")
        for itemFile in [itemPath+fileName for fileName in os.listdir(itemPath) if os.path.isfile(itemPath+fileName)]:
            with open(itemFile) as fileIn:
                info = json.load(fileIn)
                self.insert(itemTable, [info[index] for index in itemTable["tableCols"]])


    def seed(self):

        self.enterFileItems("player", proPlayersTable)
        self.enterFileItems("team", proTeamsTable)
        self.enterFileItems("stadium", stadiumsTable)

        self.insert(proPlayersTable, (-10, "Empty", "Base", -1, None, None, "n", "n", -1, -1, -1.1))

        self.insert(locationsTable, (-1, -1, -1, -1, False))
        for i, location in enumerate(pitchLocations):
            self.insert(locationsTable, (i, *location, sortingHat(*location), str(False if abs(location[0]) > 10000 or abs(location[1]) > 10000 else True)))

        for info in pitchTypes:
            self.insert(pitchTypesTable, info)

        for info in pitchResults:
            self.insert(pitchResultsTable, info)

        self.insert(contactTypesTable, (-1, -1, -1, -1, -1, -1))

        self.insert(resultTypesTable, (-1, "Label Error"))
        for i, info in enumerate(chain(atBatResults, )):#runnerResults, managerResults)):
            self.insert(resultTypesTable, (i, info[0]))

        self.insert(atBatTypesTable, (-1, -1, 0, 0, 0, 0))
        for i, info in enumerate(atBatResults):
            self.insert(atBatTypesTable, (i, i, *info[1:]))





        self.commit()

        # for filePath in ENV.yearMonthDay():
        #     with open(filePath+"scoreboard.json") as fileIn:
        #         for gamePath in ["{}.json".format(filePath+game["gameId"]) for game in json.load(fileIn)["games"]]:
        #             self.enterNewGame(filePath, gameId)


################################################################################
################################################################################


class MLBGame(DB.Database):

    def __init__(self, matchup, mlbDB):
        gameId = matchup["gameId"]
        super().__init__(ENV.getPath("game", fileName=gameId))

        mlbDB.openDB()

        self.openDB()



        try:
            stadiums = mlbDB.curs.execute("SELECT stadiums.stadium_id, title FROM stadiums INNER JOIN pro_teams ON stadiums.stadium_id = pro_teams.stadium_id WHERE team_id = ?", (matchup["homeTeam"]["teamId"],)).fetchone()
            stadiumId = stadiums[0]
            try:
                self.insert(stadiumsTable, stadiums)
            except sqlite3.IntegrityError:
                pass

            self.insert(gamesTable, (matchup["gameId"], matchup["homeTeam"]["teamId"],
                                    matchup["awayTeam"]["teamId"], -1, -1, -1, -1.1,
                                    "simulation", stadiumId))


            stadiumAB = mlbDB.curs.execute("SELECT * FROM ab_results WHERE stadium_id = ?", (stadiumId,)).fetchall()
            for ab in stadiumAB:
                try:
                    self.insert(atBatResultsTable, ab)
                except sqlite3.IntegrityError:
                    pass

            for contactId in [x[5] for x in stadiumAB]:
                contact =  mlbDB.curs.execute("SELECT * FROM contacts WHERE contact_id = ?", (contactId,)).fetchone()
                try:
                    self.insert(contactTypesTable, contact)
                except sqlite3.IntegrityError:
                    pass


            for team in ("homeTeam", "awayTeam"):

                teamId = matchup[team]["teamId"]
                teamInfo = mlbDB.curs.execute("SELECT * FROM pro_teams WHERE team_id = ?", (teamId,)).fetchone()
                try:
                    self.insert(proTeamsTable, teamInfo)
                except sqlite3.IntegrityError:
                    pass

                try:
                    self.insert(starterTable, (teamId, matchup[team]["starter"][0]))
                except sqlite3.IntegrityError:
                    pass

                for player in matchup[team]["bullpen"]:
                    playerId = player[0]
                    playerInfo = mlbDB.curs.execute("SELECT * FROM pro_players WHERE player_id = ?", (playerId,)).fetchone()

                    try:
                        self.insert(proPlayersTable, playerInfo)
                    except sqlite3.IntegrityError:
                        pass

                    try:
                        self.insert(bullpenTable, (teamId, playerId))
                    except sqlite3.IntegrityError:
                        pass

                    pitchRemoval = [x for x in mlbDB.curs.execute("SELECT * FROM removals WHERE pitcher_id = ?", (player[0],)).fetchall()]
                    if not len(pitchRemoval):
                        removeId = self.nextKey({"pk":"remove_id","tableName":"removals"})*-1
                        try:
                            self.insert(pitchRemovalsTable, (removeId, gameId, playerId, 5, 80))
                        except sqlite3.IntegrityError:
                            pass
                    else:
                        for removal in pitchRemoval:
                            try:
                                self.insert(pitchRemovalsTable, removal)
                            except sqlite3.IntegrityError:
                                pass

                    for newPitch in mlbDB.curs.execute("SELECT * FROM new_pitchers WHERE pitcher_id = ?", (player[0],)).fetchall():
                        try:
                            self.insert(newPitchersTable, newPitch)
                        except sqlite3.IntegrityError:
                            pass



                    pitchesThrown = mlbDB.curs.execute("SELECT * FROM pitches WHERE pitcher_id = ?", (player[0],)).fetchall()

                    for pitch in pitchesThrown:
                        try:
                            self.insert(pitchesTable, pitch)
                        except sqlite3.IntegrityError:
                            pass

                    if len(pitchesThrown) < 500:
                        playerIds = [x[0] for x in mlbDB.curs.execute("SELECT player_id FROM pro_players WHERE pos = ? AND throws = ? AND rookie_season = ?", (playerInfo[3], playerInfo[7], int(playerInfo[8])-1)).fetchall()]
                        try:
                            newPitches = mlbDB.curs.execute("SELECT * FROM pitches WHERE pitcher_id in {}".format(tuple(playerIds))).fetchall()
                        except:
                            newPitches = []
                        for i, pitch in enumerate(newPitches):
                            if i + len(pitchesThrown) < 500:
                                pitch = list(pitch)
                                pitch[3] = playerId
                                try:
                                    self.insert(pitchesTable, pitch)
                                except sqlite3.IntegrityError:
                                    pass

                print(team)
                pprint(matchup[team]["lineup"])
                for i, playerId in enumerate(matchup[team]["lineup"]):

                    try:
                        self.insert(lineupsTable, [matchup["gameId"], teamId, playerId, i+1, 1, "n/a"])
                    except sqlite3.IntegrityError:
                        pass

                    playerInfo = mlbDB.curs.execute("SELECT * FROM pro_players WHERE player_id = ?", (playerId,)).fetchone()
                    try:
                        self.insert(proPlayersTable, playerInfo)
                    except sqlite3.IntegrityError:
                        pass

                    pitchesFaced = mlbDB.curs.execute("SELECT * FROM pitches WHERE batter_id = ?", (playerId,)).fetchall()

                    for pitch in pitchesFaced:
                        try:
                            self.insert(pitchesTable, pitch)
                        except sqlite3.IntegrityError:
                            pass

                    if len(pitchesFaced) < 500:
                        playerIds = [x[0] for x in mlbDB.curs.execute("SELECT player_id FROM pro_players WHERE pos = ? AND bats = ? AND rookie_season = ?", (playerInfo[3], playerInfo[7], int(playerInfo[8])-1)).fetchall()]
                        try:
                            newBatters = mlbDB.curs.execute("SELECT * FROM pitches WHERE batter_id in {}".format(tuple(playerIds))).fetchall()
                        except:
                            newBatters = []
                        for i, pitch in enumerate(newBatters):
                            if i + len(pitchesFaced) < 500:
                                pitch = list(pitch)
                                pitch[3] = playerId
                                try:
                                    self.insert(pitchesTable, pitch)
                                except sqlite3.IntegrityError:
                                    pass

                            pitchId = pitch[0]

                            contact =  mlbDB.curs.execute("SELECT * FROM contacts WHERE pitch_id = ?", (pitchId,)).fetchone()
                            try:
                                self.insert(contactTypesTable, contact)
                            except (sqlite3.IntegrityError, ValueError):
                                pass

            totalContacts = [x[0] for x in self.curs.execute("SELECT pitch_id FROM contacts").fetchall()]
            totalPitches = [x[0] for x in self.curs.execute("SELECT pitch_id FROM pitches").fetchall()]

            missing = set(totalPitches)- set(totalContacts)
            for pitchId in missing:
                contact = mlbDB.curs.execute("SELECT * FROM contacts WHERE pitch_id = ?", (pitchId,)).fetchone()
                try:
                    self.insert(contactTypesTable, contact)
                except (sqlite3.IntegrityError, ValueError):
                    pass


        except sqlite3.IntegrityError:
            pass







        self.commit()
            # raise AssertionError
        #super().__init__("/home/ededub/Desktop/testDB.db")

        # mlbDB.openDB()
        #
        #
        # pprint(matchup)
        # raise AssertionError


        self.closeDB()

        mlbDB.closeDB()


    def getTableList(self):
        return (gamesTable, proPlayersTable, proTeamsTable, stadiumsTable, pitchTypesTable,
                pitchResultsTable, locationsTable, pitchesTable, contactTypesTable,
                resultTypesTable, atBatTypesTable, atBatResultsTable, pitchRemovalsTable,
                newPitchersTable, lineupsTable, bullpenTable, starterTable)


    def enterFileItems(self, itemType, itemTable):
        itemPath = ENV.getPath(itemType).strip("None.json")
        for itemFile in [itemPath+fileName for fileName in os.listdir(itemPath) if os.path.isfile(itemPath+fileName)]:
            with open(itemFile) as fileIn:
                info = json.load(fileIn)
                self.insert(itemTable, [info[index] for index in itemTable["tableCols"]])


    def seed(self):


        self.insert(proPlayersTable, (-10, "Empty", "Base", -1, None, None, "n", "n", -1, -1, -1.1))

        self.insert(locationsTable, (-1, -1, -1, -1, False))
        for i, location in enumerate(pitchLocations):
            self.insert(locationsTable, (i, *location, sortingHat(*location), str(False if abs(location[0]) > 10000 or abs(location[1]) > 10000 else True)))

        for info in pitchTypes:
            self.insert(pitchTypesTable, info)

        for info in pitchResults:
            self.insert(pitchResultsTable, info)

        self.insert(contactTypesTable, (-1, -1, -1, -1, -1, -1))

        self.insert(resultTypesTable, (-1, "Label Error"))
        for i, info in enumerate(chain(atBatResults, )):#runnerResults, managerResults)):
            self.insert(resultTypesTable, (i, info[0]))

        self.insert(atBatTypesTable, (-1, -1, 0, 0, 0, 0))
        for i, info in enumerate(atBatResults):
            self.insert(atBatTypesTable, (i, i, *info[1:]))





        self.commit()

        # for filePath in ENV.yearMonthDay():
        #     with open(filePath+"scoreboard.json") as fileIn:
        #         for gamePath in ["{}.json".format(filePath+game["gameId"]) for game in json.load(fileIn)["games"]]:
        #             self.enterNewGame(filePath, gameId)
