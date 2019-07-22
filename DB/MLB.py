import os
import sqlite3
import re
import datetime

from itertools import chain

from . import Database as DB
from . import Table as TB
import MLBProjections.MLBProjections.Models.BaseballDiamond as BD
import MLBProjections.MLBProjections.Environ as ENV
from MLBProjections.MLBProjections.Utils.UpdateMixIn import UpdateMixIn
import MLBProjections.MLBProjections.Utils.ResultParse as RP

# for debugging
from pprint import pprint

################################################################################
################################################################################

### Meta Table
metaTable = TB.Table("game_meta")
    ### Primary Key
metaTable.addPk("game_id", "INT")
    ## Foreign Keys
metaTable.addFk("home_id", "pro_teams", "team_id")
metaTable.addFk("away_id", "pro_teams", "team_id")
metaTable.addFk("stadium_id", "stadiums", "stadium_id")
###############


### Games Table
gamesTable = TB.Table("games")
    ### Primary Key
gamesTable.addPk("game_id", "INT")
    ## Foreign Keys
gamesTable.addFk("home_id", "pro_teams", "team_id")
gamesTable.addFk("away_id", "pro_teams", "team_id")
gamesTable.addFk("winner_id", "pro_teams", "team_id")
gamesTable.addFk("loser_id", "pro_teams", "team_id")
gamesTable.addFk("stadium_id", "stadiums", "stadium_id")
    ## Table Cols
gamesTable.addCol("season", "INT")
gamesTable.addCol("game_date", "REAL")
gamesTable.addCol("season_type", "TEXT")
    ## Table Indexes
gamesTable.addIndex("season_date", "season, game_date")
###############



### ProPlayers Table
proPlayersTable = TB.Table("pro_players")
    ### Primary Key
proPlayersTable.addPk("player_id", "INT")
    ## Table Cols
proPlayersTable.addCol("first_name", "TEXT")
proPlayersTable.addCol("last_name", "TEXT")
proPlayersTable.addCol("pos", "INT")
proPlayersTable.addCol("height", "INT", True)
proPlayersTable.addCol("weight", "INT", True)
proPlayersTable.addCol("bats", "TEXT")
proPlayersTable.addCol("throws", "TEXT")
proPlayersTable.addCol("rookie_season", "INT", True)
proPlayersTable.addCol("birth_year", "INT", True)
proPlayersTable.addCol("birth_day", "REAL", True)
    ## Table Indexes
proPlayersTable.addIndex("names", "last_name, first_name")
###############



### ProTeams Table
proTeamsTable = TB.Table("pro_teams")
    ### Primary Key
proTeamsTable.addPk("team_id", "INT")
    ### Foreign Key
proTeamsTable.addFk("stadium_id", "stadiums", "stadium_id")
    ## Table Cols
proTeamsTable.addCol("abrv", "TEXT")
proTeamsTable.addCol("city", "TEXT")
proTeamsTable.addCol("mascot", "TEXT")
proTeamsTable.addCol("league", "TEXT")
proTeamsTable.addCol("division", "TEXT")
proTeamsTable.addCol("color", "TEXT")
###############


### Stadiums Table
stadiumsTable = TB.Table("stadiums")
    ### Primary Key
stadiumsTable.addPk("stadium_id", "INT")
    ## Table Cols
stadiumsTable.addCol("title", "TEXT")
###############


### PitchTypes Table
pitchTypesTable = TB.Table("pitch_types")
    ### Primary Key
pitchTypesTable.addPk("pitch_type_id", "INT")
    ## Table Cols
pitchTypesTable.addCol("title", "TEXT")
###############


### PitchResults Table
pitchResultsTable = TB.Table("pitch_results")
    ### Primary Key
pitchResultsTable.addPk("pitch_result_id", "INT")
    ## Table Cols
pitchResultsTable.addCol("title", "TEXT")
###############


### PitchLocations Table
pitchLocationsTable = TB.Table("pitch_locations")
    ### Primary Key
pitchLocationsTable.addPk("pitch_location_id", "INT")
    ## Table Cols
pitchLocationsTable.addCol("x_value", "INT")
pitchLocationsTable.addCol("y_value", "INT")
pitchLocationsTable.addCol("box", "INT")
pitchLocationsTable.addCol("strike_zone", "INT")
    ## Table Indexes
pitchLocationsTable.addIndex("x_y", "x_value, y_value")
###############


### Pitches Table
pitchesTable = TB.Table("pitches")
    ### Primary Key
pitchesTable.addPk("pitch_id","INT")
    ## Foreign Keys
pitchesTable.addFk("game_id", "games", "game_id")
pitchesTable.addFk("pitcher_id", "pro_players", "player_id")
pitchesTable.addFk("batter_id", "pro_players", "player_id")
pitchesTable.addFk("pitch_type_id", "pitch_types", "pitch_type_id")
pitchesTable.addFk("base_runners_id", "base_runners", "base_runners_id")
pitchesTable.addFk("pitch_count_id", "pitch_counts", "pitch_count_id")
pitchesTable.addFk("pitch_location_id", "pitch_locations", "pitch_location_id")
pitchesTable.addFk("pitch_result_id", "pitch_results", "pitch_result_id")
    ### Table Cols
pitchesTable.addCol("play_num", "INT")
pitchesTable.addCol("pitch_num", "INT")
pitchesTable.addCol("turn", "INT")
pitchesTable.addCol("sequence", "INT")
pitchesTable.addCol("pitch_velocity", "INT")
    ### Table Indexes
pitchesTable.addIndex("pitcher_pitch", "pitcher_id, game_id")
pitchesTable.addIndex("batter_pitch", "batter_id, game_id")
###############


### PitchContacts Table
pitchContactsTable = TB.Table("pitch_contacts")
    ### Primary Key
pitchContactsTable.addPk("pitch_contact_id","INT")
    ## Foreign Keys
pitchContactsTable.addFk("game_id", "games", "game_id")
pitchContactsTable.addFk("pitcher_id", "pro_players", "player_id")
pitchContactsTable.addFk("batter_id", "pro_players", "player_id")
pitchContactsTable.addFk("pitch_type_id", "pitch_types", "pitch_type_id")
pitchContactsTable.addFk("pitch_result_id", "pitch_results", "pitch_result_id")
pitchContactsTable.addCol("ab_type_id", "INT", True)
    ### Table Cols
pitchContactsTable.addCol("pitch_num", "INT")
pitchContactsTable.addCol("box", "INT")
pitchContactsTable.addCol("turn", "INT")
pitchContactsTable.addCol("sequence", "INT")
pitchContactsTable.addCol("pitch_velocity", "INT")
pitchContactsTable.addCol("balls", "INT")
pitchContactsTable.addCol("strikes", "INT")
pitchContactsTable.addCol("outs", "INT")
pitchContactsTable.addCol("side", "INT")
pitchContactsTable.addCol("first_base", "INT")
pitchContactsTable.addCol("second_base", "INT")
pitchContactsTable.addCol("third_base", "INT")
pitchContactsTable.addCol("hit_style", "INT", True)
pitchContactsTable.addCol("hit_hardness", "INT", True)
pitchContactsTable.addCol("hit_angle", "INT", True)
pitchContactsTable.addCol("hit_distance", "INT", True)
    ### Table Indexes
pitchContactsTable.addIndex("pitcher_pitch", "pitcher_id, side, balls, strikes, first_base, second_base, third_base, sequence, turn")
pitchContactsTable.addIndex("batter_pitch", "batter_id, side, strikes, balls, first_base, second_base, third_base, sequence, turn")
pitchContactsTable.addIndex("pitcher_contact", "pitcher_id, side, pitch_type_id, pitch_velocity, box, hit_style, hit_hardness, hit_angle, hit_distance")
pitchContactsTable.addIndex("batter_contact", "batter_id, side, pitch_type_id, pitch_velocity, box, hit_style, hit_hardness, hit_angle, hit_distance")

###############


### PitchCount Table
pitchCountsTable = TB.Table("pitch_counts")
    ### Primary Key
pitchCountsTable.addPk("pitch_count_id", "INT")
    ## Table Cols
pitchCountsTable.addCol("balls", "INT")
pitchCountsTable.addCol("strikes", "INT")
pitchCountsTable.addCol("outs", "INT")
###############


### BaseRunners Table
baseRunnersTable = TB.Table("base_runners")
    ### Primary Key
baseRunnersTable.addPk("base_runners_id", "INT")
    ### Foreign Keys
baseRunnersTable.addFk("first_base", "pro_players", "player_id")
baseRunnersTable.addFk("second_base", "pro_players", "player_id")
baseRunnersTable.addFk("third_base", "pro_players", "player_id")
    ## Table Indexes
baseRunnersTable.addIndex("on_bases", "first_base, second_base, third_base")
###############


### AtBatTypes Table
atBatTypesTable = TB.Table("ab_types")
    ### Primary Key
atBatTypesTable.addPk("ab_type_id", "INT")
    ### Table Cols
atBatTypesTable.addCol("title", "TEXT")
atBatTypesTable.addCol("is_ab", "INT")
atBatTypesTable.addCol("on_base", "INT")
atBatTypesTable.addCol("is_hit", "INT")
atBatTypesTable.addCol("is_out", "INT")
atBatTypesTable.addCol("ex_out", "INT")
atBatTypesTable.addCol("start_base", "INT")
###############


### AtBatReultss Table
atBatResultsTable = TB.Table("ab_results")
    ### Primary Key
atBatResultsTable.addPk("ab_id", "INT")
    ### Foreign Keys
atBatResultsTable.addFk("game_id", "games", "game_id")
atBatResultsTable.addFk("pitch_id", "pitches", "pitch_id")
atBatResultsTable.addFk("ab_type_id", "ab_types", "ab_type_id")
    ### Table Cols
atBatResultsTable.addCol("hit_style", "INT", True)
atBatResultsTable.addCol("hit_hardness", "INT", True)
atBatResultsTable.addCol("hit_angle", "INT", True)
atBatResultsTable.addCol("hit_distance", "INT", True)
    ### Table Indexes
atBatResultsTable.addIndex("ab_pitches", "pitch_id")
atBatResultsTable.addIndex("ab_contacts", "hit_style, hit_hardness, hit_angle, hit_distance")
###############


### RunsScored Table
runsScoredTable = TB.Table("runs_scored")
    ### Primary Key
runsScoredTable.addPk("score_id", "INT")
    ### Foreign Keys
runsScoredTable.addFk("game_id", "games", "game_id")
runsScoredTable.addFk("run_id", "pro_players", "player_id")
runsScoredTable.addFk("rbi_id", "pro_players", "player_id")
runsScoredTable.addFk("er_id", "pro_players", "player_id")
    ### Table Cols
runsScoredTable.addCol("play_num", "INT")
    ### Table Indexes
###############



### PitchRelace Table
pitchReplaceTable = TB.Table("pitcher_replace")
    ### Primary Key
pitchReplaceTable.addPk("pr_id", "INT")
    ### Foreign Keys
pitchReplaceTable.addFk("game_id", "games", "game_id")
pitchReplaceTable.addFk("team_id", "pro_teams", "team_id")
pitchReplaceTable.addFk("remove_id", "pro_players", "player_id")
pitchReplaceTable.addFk("replace_id", "pro_players", "player_id")
    ### Table Cols
pitchReplaceTable.addCol("play_num", "INT")
pitchReplaceTable.addCol("runs", "INT")
pitchReplaceTable.addCol("pitch_num", "INT")
pitchReplaceTable.addCol("inning", "INT")
###############


### contactAtBatsTable Table
contactAtBatsTable = TB.Table("contact_at_bats")
    ### Primary Key
contactAtBatsTable.addPk("c_a_b_id", "INT")
    ### Foreign Keys
contactAtBatsTable.addFk("team_id", "pro_teams", "team_id")
    ### Table Cols
contactAtBatsTable.addCol("hit_style", "INT")
contactAtBatsTable.addCol("hit_hardness", "INT")
contactAtBatsTable.addCol("hit_angle", "INT")
contactAtBatsTable.addCol("hit_distance", "INT")
contactAtBatsTable.addFk("ab_type_id", "ab_types", "ab_type_id")
    ### Table Indexes
contactAtBatsTable.addIndex("team_defense", "team_id, hit_style, hit_hardness, hit_angle, hit_distance")
###############


### Lineups Table
lineupsTable = TB.Table("lineups")
    ### Primary Key
lineupsTable.addPk("lineup_id", "INT")
    ### Foreign Keys
lineupsTable.addFk("game_id", "games", "game_id")
lineupsTable.addFk("team_id", "pro_teams", "team_id")
lineupsTable.addFk("player_id", "pro_players", "player_id")
    ### Table Cols
lineupsTable.addCol("batt_order", "INT")
lineupsTable.addCol("sub_order", "INT")
lineupsTable.addCol("pos", "TEXT")
###############


### Bullpens Table
bullpensTable = TB.Table("bullpens")
    ### Primary Key
bullpensTable.addPk("bullpen_id", "INT")
    ### Foreign Keys
bullpensTable.addFk("team_id", "pro_teams", "team_id")
bullpensTable.addFk("player_id", "pro_players", "player_id")
    ### Table Cols
bullpensTable.addCol("starter", "INT")
###############


### Bench Table
benchesTable = TB.Table("benches")
    ### Primary Key
benchesTable.addPk("bench_id", "INT")
    ### Foreign Keys
benchesTable.addFk("team_id", "pro_teams", "team_id")
benchesTable.addFk("player_id", "pro_players", "player_id")
###############



threeRuns = re.compile("\[\d*?\], \[\d*?\] and \[\d*?\] scored")
twoRuns = re.compile("\[\d*?\] and \[\d*?\] scored")
runScored = re.compile("\[\d*?\] scored")





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


                # title, is_ab, on_base, is_hit, is_out, ex_out, starting_base
atBatResults = (("Ground Out", 1, 0, 0, 1, 1, 0),
                ("Strike Out", 1, 0, 0, 1, 1, 0),
                ("Single", 1, 1, 1, 0, 0, 1),
                ("Fly Out", 1, 0, 0, 1, 1, 0),
                ("Walk", 0, 1, 0, 0, 0, 1),
                ("Line Out", 1, 0, 0, 1, 1, 0),
                ("Double", 1, 1, 1, 0, 0, 2),
                ("Pop Out", 1, 0, 0, 1, 1, 0),
                ("Home Run", 1, 1, 1, 0, 0, 4),
                ("Fielder's Choice", 1, 0, 0, 1, 1, 1),
                ("Double Play", 1, 0, 0, 1, 1, 0),
                ("Fouled Out", 1, 0, 0, 1, 1, 0),
                ("Hit by Pitch", 0, 1, 0, 0, 0, 1),
                ("Reached on Error", 1, 0, 0, 0, 1, 1),
                ("Sacrifice", 0, 0, 0, 1, 1, 0),
                ("Triple", 1, 1, 1, 0, 0, 3),
                ("Reached on Interference", 0, 1, 0, 0, 1, 1),
                ("Triple Play", 1, 0, 0, 1, 1, 0),
                ("Out on Interference", 1, 0, 0, 1, 1, 0),
                ("Out of Order", 1, 0, 0, 1, 1, 0))


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


unearnId = -20
emptyId = -10
noRbiId = -5




createTableCmd = """
                    CREATE TABLE IF NOT EXISTS {0[tableName]} (
                        player_id INT NOT NULL,
                        history_id TEXT NOT NULL,
                        {0[pitch_contact]}
                        {0[classifierCmd]}
                        intercept REAL NOT NULL,
                        {0[tableCmd]}
                        PRIMARY KEY ( {0[pkCmd]} ),
                        FOREIGN KEY (player_id) REFERENCES pro_players (player_id) )
                """


pitchesCmd =  """
                SELECT {0[selectCmd]}
                FROM pitches AS pitch0
                INNER JOIN pro_players AS pitcher ON pitch0.pitcher_id = pitcher.player_id
                INNER JOIN pro_players AS batter ON pitch0.batter_id = batter.player_id
                INNER JOIN pitch_locations ON pitch0.location_id = pitch_locations.location_id
                INNER JOIN lineups ON pitch0.game_id = lineups.game_id AND pitch0.batter_id = lineups.player_id

                INNER JOIN (SELECT pitch_id, pitch_type_id AS pitch_type_1, box AS box_1, prev_pitch_id
                                    FROM pitches
                                    INNER JOIN pitch_locations
                                        ON pitches.location_id = pitch_locations.location_id
                                    ) AS pitch1
                    ON pitch0.prev_pitch_id = pitch1.pitch_id

                INNER JOIN (SELECT pitch_id, pitch_type_id AS pitch_type_2, box AS box_2, prev_pitch_id
                                    FROM pitches
                                    INNER JOIN pitch_locations
                                        ON pitches.location_id = pitch_locations.location_id
                                    ) AS pitch2
                    ON pitch1.prev_pitch_id = pitch2.pitch_id

                WHERE pitcher_id = ?
                """


pitchContactCmd = """
                    SELECT {0[selectCmd]}
                    FROM pitches
                    LEFT OUTER JOIN contacts ON contacts.pitch_id = pitches.pitch_id
                    INNER JOIN pro_players AS pitcher ON pitches.pitcher_id = pitcher.player_id
                    INNER JOIN pro_players AS batter ON pitches.batter_id = batter.player_id
                    INNER JOIN pitch_locations ON pitches.location_id = pitch_locations.location_id

                    WHERE pitcher_id = ?
                    """


pitchRemoveCmd = """
                    SELECT {0[selectCmd]}
                    FROM removals

                    WHERE pitcher_id = ?
                    """


pitchReplaceCmd = """
                    SELECT {0[selectCmd]}
                    FROM new_pitchers

                    WHERE team_id = ?
                    """


pitchAtBatsCmd = """
                SELECT ab_results.game_id,
                        ab_results.play_num,
                        pitch_num,
                        runs
                FROM ab_results
                INNER JOIN pitches ON ab_results.pitch_id = pitches.pitch_id
                WHERE pitcher_id = ?
                """








battPitchesCmd = """
                    SELECT {0[selectCmd]}
                    FROM pitches
                    LEFT OUTER JOIN contacts ON contacts.pitch_id = pitches.pitch_id
                    INNER JOIN pro_players AS pitcher ON pitches.pitcher_id = pitcher.player_id
                    INNER JOIN pro_players AS batter ON pitches.batter_id = batter.player_id
                    INNER JOIN pitch_locations ON pitches.location_id = pitch_locations.location_id

                    WHERE batter_id = ?
                    """


battContactsCmd = """
                    SELECT {0[selectCmd]}
                    FROM contacts
                    INNER JOIN pitches ON contacts.pitch_id = pitches.pitch_id
                    INNER JOIN pro_players AS pitcher ON pitches.pitcher_id = pitcher.player_id
                    INNER JOIN pro_players AS batter ON pitches.batter_id = batter.player_id
                    INNER JOIN pitch_locations ON pitches.location_id = pitch_locations.location_id

                    WHERE batter_id = ?
                    """


################################################################################
################################################################################


class MLBDatabase(DB.Database, UpdateMixIn):

    def __init__(self):
        UpdateMixIn.__init__(self)
        DB.Database.__init__(self, ENV.getPath("database", fileName="mlb"))


    def getManagerKey(self):
        return "dbEntries"


    def update(self):
        self.loadManagerFile()
        if self.checkUpdate():
            checkDate = self.getItem().date()
            self.insertDates(checkDate)
            self.updateManagerFile()
            self.commit()


    def getTableList(self):
        return (gamesTable, proPlayersTable, proTeamsTable, stadiumsTable, pitchTypesTable,
                pitchResultsTable, pitchLocationsTable, pitchesTable, atBatTypesTable,
                atBatResultsTable, pitchReplaceTable, lineupsTable,
                pitchCountsTable, baseRunnersTable, runsScoredTable)


    def enterFileItems(self, itemType, itemTable):
        itemPath = ENV.getPath(itemType).strip("None.json")
        for itemFile in [itemPath+fileName for fileName in os.listdir(itemPath) if os.path.isfile(itemPath+fileName)]:
            info = ENV.getJsonInfo(itemFile)
            self.insert(itemTable, info=info)


    def insertDates(self, checkDate):
        for filePath in ENV.yearMonthDay(checkDate):
            info = ENV.getJsonInfo(filePath+"scoreboard.json")
            for gamePath in ["{}.json".format(filePath+game["game_id"]) for game in info["games"] if game["status"] == "final"]:
                try:
                    self.insertGame(gamePath)
                except sqlite3.IntegrityError as e:
                    print(e)



    def insertGame(self, gamePath):
        print("Inserting {}".format(gamePath))

        gameInfo = ENV.getJsonInfo(gamePath)

        gameId = gameInfo["game_id"]
        homeId = gameInfo["home_id"]
        awayId = gameInfo["away_id"]

        if gameInfo.get("season_type", None):
            gameInfo["season_type"] = "reg"



        try:
            pbp = gameInfo["play_by_play"].values()
            pitches = gameInfo["pitches"].values()
        except KeyError:
            print("Attempting to re-download")
            gameDate = datetime.date(*[int(n) for n in gamePath.split("/")[-4:-1]])
            # Delete game file
            DM.removeDownload(gamePath)
            # Download new game File
            DM.BoxScore(gameDate, gameInfo["url"])
            # re-load game info
            gameInfo = ENV.jsonFileInfo(gamePath)

        # Games Table
        self.insert(gamesTable, info=gameInfo)

        # Lineups Table
        for side in ("home", "away"):

            for lineup in gameInfo["lineups"][side]["B"]:
                lineupId = self.nextKey(lineupsTable)
                lineup["lineup_id"] = lineupId
                lineup["game_id"] = gameId
                lineup["batt_order"] = lineup["order"]
                lineup["team_id"] = gameInfo["{}_id".format(side)]
                lineup["pos"] = lineup["position"][0]
                self.insert(lineupsTable, info=lineup)


        # initialize variables
        pitchStaff = {}
        pitchId = -1
        turn = {}
        pitchTurn = None
        batterTurn = 1
        reset = True
        outs = 0
        exOuts = 0
        pitchTeam = homeId
        currentPitcher = {0:None, 1:None}
        newPitcher = {"pitch_num":0,"runs":0}
        diamond = BD.BaseballDiamond()


        for play in sorted(chain(pbp, pitches), key=lambda x: int(x["play_num"])):
            runs = 0
            outs = 2 if outs > 2 else outs
            activeTables = []

            info = {
                        "game_id": gameId,
                        "batter_id": play.get("batter",None),
                        "pitcher_id": play.get("pitcher",None),
                        "hit_angle": play.get("hit_angle",None),
                        "hit_distance": play.get("hit_distance",None),
                        "hit_hardness": play.get("hit_hardness",None),
                        "hit_style": play.get("hit_style",None),
                        "pitch_type_id": play.get("pitch_type", 7),
                        "pitch_velocity": play.get("velocity", -1),
                        "sequence": play.get("sequence",None),
                        "play_num": play.get("play_num",None),
                        "balls": play.get("balls",None),
                        "strikes": play.get("strikes",None),
                        "pitch_result_id": play.get("result",None),
                        "xValue": play.get("horizontal", None),
                        "yValue": play.get("vertical", None)
                    }
            if int(play.get("balls", 0)) > 3:
                info["balls"] = 3
            if int(play.get("strikes", 0)) > 2:
                info["strikes"] = 2




            if play["play_type"] == "PITCH":
                pitcherId = info["pitcher_id"]
                currentPitcher[int(play["period"])%2] = pitcherId
                batterId = info["batter_id"]

                if reset:
                    pitchTurn = turn.get(pitcherId, {})
                    batterTurn = pitchTurn.get(batterId, 0) + 1
                    reset = False
                # Setting table
                activeTables.append(pitchesTable)
                # Done for clarity

                # Setting pitchNum using pitchStaff register
                pitcher = pitchStaff.get(pitcherId, newPitcher.copy())
                pitcher["pitch_num"] += 1
                pitchNum = pitcher["pitch_num"]
                pitchStaff[pitcherId] = pitcher
                # Setting batterTurn using turn register
                pitchTurn[batterId] = batterTurn
                turn[pitcherId] = pitchTurn
                # Table column entries
                pitchId = self.nextKey(pitchesTable)
                countId = self.getKey(pitchCountsTable, balls=info["balls"], strikes=info["strikes"], outs=outs)
                firstBase, secondBase, thirdBase = diamond.whoOnBase()
                brId = self.getKey(baseRunnersTable, first_base=firstBase , second_base=secondBase , third_base=thirdBase )
                try:
                    locationId = self.getKey(pitchLocationsTable, x_value=info["xValue"], y_value =info["yValue"])
                except sqlite3.OperationalError:
                    locationId = -1
                # Entering column values into info dictionary
                for key, value in (("pitch_id", pitchId), ("pitch_count_id", countId), ("turn", batterTurn),
                                    ("base_runners_id", brId), ("pitch_location_id", locationId),
                                    ("pitch_num", pitchNum)):
                    info[key] = value


            if play["play_type"] == "RESULT":
                reset = True
                # initialize variables
                onHook = None
                rbiId = noRbiId
                # print()
                # pprint(play)
                # Setting table
                activeTables.append(atBatResultsTable)
                action, mainMovement, secondaryMovement = RP.parseAtBat(play["text"])
                # print("\n\n\n\n")
                # print(diamond.firstBase, diamond.secondBase, diamond.thirdBase)
                # print()
                # print(play["text"])
                # pprint(mainMovement)
                # print()
                # pprint(secondaryMovement)
                # print()

                for i, abResult in enumerate(atBatResults):
                    if abResult[0] == action:
                        # print(action)
                        info["ab_id"] = self.nextKey(atBatResultsTable)
                        info["ab_type_id"] = i
                        info["pitch_id"] = pitchId

                        outs += abResult[-3]
                        exOuts += abResult[-2]
                        # print()
                        # print(action, abResult[-1])

                        if action not in ("Reached on Error", "Double Play"):
                            rbiId = info["batter_id"]

                        if action in ("Reached on Error", "Reached on Interference") or exOuts > 2:
                            onHook = unearnId
                        else:
                            onHook = pitcherId



                        if action == "Home Run":
                            scoreId = self.nextKey(runsScoredTable)
                            info2 = {"game_id": gameId,
                                        "score_id": scoreId,
                                        "play_num": info["play_num"],
                                        "run_id": info["batter_id"],
                                        "rbi_id": rbiId,
                                        "er_id": onHook}

                            self.insert(runsScoredTable, info=info2)
                            runs += 1


                        for scored in mainMovement["scored"]:
                            runs += 1
                            # Run is unearned
                            try:
                                tempHook = diamond.popPlayer(scored)
                            except KeyError:
                                tempHook = pitcherId
                            if onHook != unearnId:
                                onHook = tempHook


                            scoreId = self.nextKey(runsScoredTable)
                            info2 = {"game_id": gameId,
                                        "score_id": scoreId,
                                        "play_num": info["play_num"],
                                        "run_id": scored,
                                        "rbi_id": rbiId,
                                        "er_id": onHook}
                            self.insert(runsScoredTable, info=info2)


                        for baseOut in mainMovement["out"]:
                            try:
                                diamond.popPlayer(baseOut)
                                outs += 1
                                exOuts += 1
                            except KeyError:
                                if action not in ("Out on Interference", "Out of Order"):
                                    outs += 1
                                    exOuts += 1


                        for third in mainMovement["thirdBase"]:
                            try:
                                thirdHook = diamond.popPlayer(third)
                            except KeyError:
                                thirdHook = pitcherId
                            try:
                                diamond.reachedBase("thirdBase", third, thirdHook)
                            except BD.BaseFullError:
                                _,thirdHook = diamond.popBase("thirdBase")
                                diamond.reachedBase("thirdBase", third, thirdHook)



                        for second in mainMovement["secondBase"]:
                            try:
                                secondHook = diamond.popPlayer(second)
                            except KeyError:
                                secondHook = pitcherId
                            try:
                                diamond.reachedBase("secondBase", second, secondHook)
                            except BD.BaseFullError:
                                _, secondHook = diamond.popBase("secondBase")
                                diamond.reachedBase("secondBase", second, secondHook)


                        if abResult[-1] >0 and abResult[-1] < 4:
                            base = {1:"firstBase", 2:"secondBase", 3:"thirdBase"}[abResult[-1]]
                            if not diamond.checkPlayer(batterId):
                                try:
                                    diamond.reachedBase(base, batterId, pitcherId)
                                except BD.BaseFullError:
                                    diamond.popBase(base)
                                    diamond.reachedBase(base, batterId, pitcherId)




                        for scored in secondaryMovement["scored"]:
                            # Run is unearned
                            try:
                                diamond.popPlayer(scored)
                            except KeyError:
                                pass

                            scoreId = self.nextKey(runsScoredTable)
                            info2 = {"game_id": gameId,
                                        "score_id": scoreId,
                                        "play_num": info["play_num"],
                                        "run_id": scored,
                                        "rbi_id": noRbiId,
                                        "er_id": unearnId}

                            self.insert(runsScoredTable, info=info2)



                        for baseOut in secondaryMovement["out"]:
                            try:
                                diamond.popPlayer(baseOut)
                            except KeyError:
                                pass
                            outs += 1
                            exOuts += 1


                        for third in secondaryMovement["thirdBase"][-1:]:
                            try:
                                thirdHook = diamond.popPlayer(third)
                            except KeyError:
                                thirdHook = pitcherId
                            try:
                                diamond.reachedBase("thirdBase", third, thirdHook)
                            except BD.BaseFullError:
                                _,thirdHook = diamond.popBase("thirdBase")
                                diamond.reachedBase("thirdBase", third, thirdHook)


                        for second in secondaryMovement["secondBase"][-1:]:
                            try:
                                secondHook = diamond.popPlayer(second)
                            except KeyError:
                                secondHook = pitcherId
                            try:
                                diamond.reachedBase("secondBase", second, secondHook)
                            except BD.BaseFullError:
                                _, secondHook = diamond.popBase("secondBase")
                                diamond.reachedBase("secondBase", second, secondHook)

                        # print(diamond.firstBase, diamond.secondBase, diamond.thirdBase)
                        # print("\n\n\n\n")
                        pitcher = pitchStaff.get(pitcherId, newPitcher.copy())
                        pitcher["runs"] += runs
                        pitchStaff[pitcherId] = pitcher
                        break




            if play["play_type"] == "SUB" and "pitching" in play["text"]:
                index = int(play["period"]) %2
                pp = pitchStaff.get(currentPitcher[index], newPitcher.copy())
                activeTables.append(pitchReplaceTable)
                prId = self.nextKey(pitchReplaceTable)
                inning = int((int(play["period"])+1)/2)
                for key, value in (("team_id", pitchTeam), ("remove_id", currentPitcher[index]), ("replace_id", play["players"]),
                                    ("inning", inning,), ("pr_id", prId), ("runs", pp["runs"]),
                                    ("pitch_num", pp["pitch_num"])):
                    info[key] = value
                #raise AssertionError
            if play["play_type"] == "INNING":

                diamond.clearBases()
                outs = 0
                exOuts = 0
                pitchTeam = homeId if pitchTeam == awayId else homeId

            # Enter records for activeTables
            for table in activeTables:
                try:
                    self.insert(table, info=info)
                except sqlite3.IntegrityError as e:
                    print(e)
                    print(table.getName)





    def seed(self):

        self.clearManagerFile()
        self.enterFileItems("player", proPlayersTable)
        self.enterFileItems("team", proTeamsTable)
        self.enterFileItems("stadium", stadiumsTable)

        self.insert(proPlayersTable, values=(-5, "No", "RBI", -1, None, None, "n", "n", -1, -1, -1.1))
        self.insert(proPlayersTable, values=(-10, "Empty", "Base", -1, None, None, "n", "n", -1, -1, -1.1))
        self.insert(proPlayersTable, values=(-20, "Unearned", "Run", -1, None, None, "n", "n", -1, -1, -1.1))

        self.insert(pitchLocationsTable, values=(-1, -1, -1, -1, False))
        for i, location in enumerate(pitchLocations):
            self.insert(pitchLocationsTable, values=(i, *location, sortingHat(*location), str(False if abs(location[0]) > 10000 or abs(location[1]) > 10000 else True)))

        for values in pitchTypes:
            self.insert(pitchTypesTable, values=values)

        for values in pitchResults:
            self.insert(pitchResultsTable, values=values)

        countId = 1
        for out in range(3):
            for strike in range(3):
                for ball in range(4):
                    self.insert(pitchCountsTable, values=(countId, ball, strike, out))
                    countId += 1

        for i, values in enumerate(atBatResults):
            self.insert(atBatTypesTable, values=(i, *values))
        self.commit()



################################################################################
################################################################################


class MLBGame(DB.Database):

    def __init__(self, gameId):
        super().__init__(ENV.getPath("game", fileName=gameId))


    def notify(self, info):
        self.openDB()
        self.executeCmd("DELETE FROM lineups")
        for team in info["teams"].values():
            for batter in team["lineup"]:
                lId = self.nextKey(lineupsTable)
                self.insert(lineupsTable, values=(lId, info["gameId"], team["teamId"], batter[0], batter[3], 1, batter[-1]))
        self.commit()

        self.closeDB()


    def getTableList(self):
        return (metaTable, gamesTable, proPlayersTable, proTeamsTable, stadiumsTable, pitchTypesTable,
               pitchResultsTable,  pitchContactsTable, atBatTypesTable,
               pitchReplaceTable, lineupsTable, bullpensTable, contactAtBatsTable)


    def enterFileItems(self, itemType, itemTable):
        itemPath = ENV.getPath(itemType).strip("None.json")
        for itemFile in [itemPath+fileName for fileName in os.listdir(itemPath) if os.path.isfile(itemPath+fileName)]:
            info = ENV.getJsonInfo(itemFile)
            self.insert(itemTable, info=info)


    def seed(self):

        self.insert(proPlayersTable, values=(-5, "No", "RBI", -1, None, None, "n", "n", -1, -1, -1.1))
        self.insert(proPlayersTable, values=(-10, "Empty", "Base", -1, None, None, "n", "n", -1, -1, -1.1))
        self.insert(proPlayersTable, values=(-20, "Unearned", "Run", -1, None, None, "n", "n", -1, -1, -1.1))

        for values in pitchTypes:
            self.insert(pitchTypesTable, values=values)

        for values in pitchResults:
            self.insert(pitchResultsTable, values=values)

        for i, values in enumerate(atBatResults):
            self.insert(atBatTypesTable, values=(i, *values))
        self.commit()
