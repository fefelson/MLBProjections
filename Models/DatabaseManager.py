import json
import sqlite3
import warnings
import time
import datetime

import MLBProjections.MLBProjections.DB.MLB as DB
import MLBProjections.MLBProjections.Environ as ENV

from pprint import pprint

################################################################################
################################################################################

contactsCmd = """
                SELECT pitches.pitch_id, pitcher_id, pitches.batter_id, pitch_num, pitch_type_id, box,
                        velocity, (CASE WHEN pitcher.throws = batter.bats THEN 1 ELSE 0 END) AS side,
                        turn, sequence, balls, strikes, pitch_result_id, hit_style,
                        hit_hardness, hit_angle, hit_distance

                    FROM pitches

                    INNER JOIN games
                        ON pitches.game_id = games.game_id

                    INNER JOIN pitch_locations
                        ON pitches.location_id = pitch_locations.location_id

                    INNER JOIN pro_players AS batter
                        ON pitches.batter_id = batter.player_id

                    INNER JOIN pro_players AS pitcher
                        ON pitches.pitcher_id = pitcher.player_id

                    LEFT OUTER JOIN contacts
                        ON pitches.pitch_id = contacts.pitch_id

                    WHERE {0[playerType]}_id = ?
                """



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


similarPitcherCmd = """
                        SELECT pp.player_id,
                                team_id
                        FROM pro_players AS pp
                        INNER JOIN (SELECT pos, throws FROM pro_players WHERE player_id =?) AS a
                            ON pp.pos = a.pos AND pp.throws = a.throws
                        INNER JOIN (SELECT pitcher_id, COUNT(pitcher_id) AS pitch_count FROM pitches GROUP BY pitcher_id) AS b
                            ON pp.player_id = b.pitcher_id
                        INNER JOIN (SELECT MAX(game_id), player_id, team_id FROM lineups GROUP BY player_id) AS c
                            ON pp.player_id = c.player_id
                        WHERE pitch_count >= 100
                        ORDER BY pp.player_id DESC
                    """


similarBatterCmd = """
                        SELECT pp.player_id,
                                team_id
                        FROM pro_players AS pp
                        INNER JOIN (SELECT pos, bats FROM pro_players WHERE player_id =?) AS a
                            ON pp.pos = a.pos AND pp.bats = a.bats
                        INNER JOIN (SELECT batter_id, COUNT(batter_id) AS pitch_count FROM pitches GROUP BY batter_id) AS b
                            ON pp.player_id = b.batter_id
                        INNER JOIN (SELECT MAX(game_id), player_id, team_id FROM lineups GROUP BY player_id) AS c
                            ON pp.player_id = c.player_id
                        WHERE pitch_count >= 100
                        ORDER BY pp.player_id DESC
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


class DatabaseManager:

    # _stores = (RS.PitcherRemovalStore,
    #             RS.PitcherReplaceStore,)

    _stores = []

    def __init__(self):

        self.gameDB = None
        self.mlbDB = None
        self.info = {}


    def newBatter(self, teamId, batterId):
        startTime = time.clock()
        if not self.gameDB.curs.execute("SELECT player_id FROM pro_players WHERE player_id = ?",(batterId,)).fetchone():
            self.addPlayer(batterId)

        data = {"removals":None,
                "replaces":None}

        pitchCount = self.mlbDB.curs.execute("SELECT COUNT(batter_id) FROM pitches INNER JOIN pro_players ON pitches.batter_id = pro_players.player_id WHERE  batter_id = ?", (batterId,)).fetchone()[0]

        checkId = batterId
        checkTeamId = teamId

        if pitchCount < 100:
            checkId, checkTeamId = self.mlbDB.fetchOne(similarBatterCmd, (batterId,))

        pitchContacts = self.mlbDB.fetchAll(contactsCmd.format({"playerType": "batter"}), (checkId,))
        for contact in pitchContacts:
            try:
                self.gameDB.insert(DB.pitchContactsTable, [*contact[:2], batterId, *contact[3:]])
            except sqlite3.IntegrityError:
                pass





        endTime = time.clock()
        print(endTime-startTime)
        print()



    def newPitcher(self, teamId, pitcherId, starter=0):
        startTime = time.clock()
        if not self.gameDB.curs.execute("SELECT player_id FROM pro_players WHERE player_id = ?",(pitcherId,)).fetchone():
            self.addPlayer(pitcherId)

            data = {"removals":[],
                    "atbats":[],
                    "replaces":[]}



            self.gameDB.insert(DB.bullpenTable, (teamId, pitcherId, starter))


            pitchCount = self.mlbDB.curs.execute("SELECT COUNT(pitcher_id) FROM pitches INNER JOIN pro_players ON pitches.pitcher_id = pro_players.player_id WHERE pitcher_id = ?", (pitcherId,)).fetchone()[0]

            checkId = pitcherId
            checkTeamId = teamId
            try:
                if pitchCount < 100:
                    checkId, checkTeamId = self.mlbDB.fetchOne(similarPitcherCmd, (pitcherId,))

            except TypeError:
                pass

            pitchContacts = self.mlbDB.fetchAll(contactsCmd.format({"playerType": "pitcher"}), (checkId,))
            for contact in pitchContacts:
                try:
                    self.gameDB.insert(DB.pitchContactsTable, [contact[0], pitcherId, *contact[2:]])
                except sqlite3.IntegrityError:
                    pass

            for removal in self.mlbDB.fetchAll("SELECT * FROM removals WHERE pitcher_id = ?",(checkId,)):
                try:
                    self.gameDB.insert(DB.pitchRemovalsTable,[*removal[:3], pitcherId, *removal[4:]])
                except sqlite3.IntegrityError:
                    pass


            for replace in self.mlbDB.fetchAll("SELECT * FROM new_pitchers WHERE pitcher_id = ? AND team_id = ?",(pitcherId,teamId)):
                try:
                    self.gameDB.insert(DB.newPitchersTable, replace)
                except sqlite3.IntegrityError:
                    pass






            endTime = time.clock()
            print(endTime-startTime)
            print()
            #     pitches = [dict(zip(pitcherValues,pitch)) for pitch in mlbDB.curs.execute(pitcherCmd, (pitcherId,)).fetchall()]
            # else:
            #     pitches = [dict(zip(pitcherValues,pitch)) for pitch in mlbDB.curs.execute(unknownPitcherCmd, (pitcherId,)).fetchall()][:500]
            #     print(len(pitches))
            # pitchTypes = setPitchTypes(pitcherId, pitches)
            # for pitchType in pitchTypes:
            #     gameDB.insert(DB.pitchTypeLogTables, [pitcherId, "career", int(pitchType[0]), pitchType[1], *pitchType[2]])



    def setBullpens(self):

        for key in ("homeTeam", "awayTeam"):
            team = self.info[key]
            teamId = team["teamId"]

            starterId = team["starter"][0]
            self.newPitcher(teamId, starterId, True)

            for pitcher in team["bullpen"]:
                pitcherId = pitcher[0]
                if int(self.mlbDB.fetchOne("SELECT pos FROM pro_players WHERE player_id = ?", (pitcherId,))[0]) > 20:
                    self.newPitcher(teamId, pitcherId)


    def setLineups(self):

        for key in ("homeTeam", "awayTeam"):
            team = self.info[key]
            teamId = team["teamId"]

            for batterId in [batter[0] for batter in team["bench"]]:
                self.newBatter(teamId, batterId)

            if self.mlbDB.fetchOne("SELECT league FROM pro_teams WHERE team_id = ?",(teamId,))[0] == "NL":
                self.newBatter(teamId, team["starter"][0])

            for i,batterId in enumerate(team["lineup"]):
                self.gameDB.insert(DB.lineupsTable,(self.info["gameId"], teamId, batterId, i, 1, "n/a"))







    def setTeams(self):
        homeId = self.info["homeId"]
        awayId = self.info["awayId"]

        for teamId in (homeId, awayId):
            teamInfo = self.mlbDB.curs.execute("SELECT * FROM pro_teams WHERE team_id = ?", (teamId,)).fetchone()
            self.gameDB.insert(DB.proTeamsTable, teamInfo)


    def setMetaData(self):
        gameId = self.info["gameId"]
        homeId = self.info["homeId"]
        awayId = self.info["awayId"]
        stadiumId = self.info["stadiumId"]
        self.gameDB.insert(DB.metaTable, (gameId, homeId, awayId, stadiumId))



    def setStadiumContacts(self):
        stadiumId = self.info["stadiumId"]
        stadiumData = self.mlbDB.curs.execute("SELECT hit_style, hit_hardness, hit_angle, hit_distance, result_type_id FROM contacts INNER JOIN ab_results ON contacts.contact_id = ab_results.contact_id WHERE stadium_id = ? AND hit_style != -1", (stadiumId,)).fetchall()
        for data in stadiumData:
            cabId = self.gameDB.nextKey({"pk":"c_a_b_id", "tableName": DB.contactAtBatsTable["tableName"]})
            try:
                self.gameDB.insert(DB.contactAtBatsTable, [cabId,]+list(data))
            except sqlite3.IntegrityError:
                pass


    def setStadium(self):
        stadiumId = self.info["stadiumId"]
        stadiumInfo = self.mlbDB.curs.execute("SELECT * FROM stadiums WHERE stadium_id = ?",(stadiumId,)).fetchone()
        self.gameDB.insert(DB.stadiumsTable, stadiumInfo)


    def addPlayer(self, playerId):
        playerInfo = self.mlbDB.curs.execute("SELECT * FROM pro_players WHERE player_id = ?",(playerId,)).fetchone()
        pprint(playerInfo)
        self.gameDB.insert(DB.proPlayersTable, playerInfo)


    def createGameDB(self, mlbDB, matchup):
        startGame = time.clock()
        self.mlbDB = mlbDB

        self.info["gameId"] = matchup["gameId"]
        self.info["homeId"] = matchup["homeTeam"]["teamId"]
        self.info["awayId"] = matchup["awayTeam"]["teamId"]
        self.info["stadiumId"] = mlbDB.curs.execute("SELECT stadium_id FROM pro_teams WHERE team_id = ?", (self.info["homeId"],)).fetchone()[0]
        for key in ("homeTeam", "awayTeam"):
            self.info[key] = matchup[key]


        self.gameDB = DB.MLBGame(self.info["gameId"])
        self.gameDB.openDB()

        for store in self._stores:
            reg = store().orderRegression()
            self.createTable(reg.info)
            self.regressions[reg.info["tableName"]] = reg


        # Inserting Meta Data
        self.setMetaData()

        self.setStadium()
        self.setStadiumContacts()

        self.setTeams()

        self.setBullpens()

        self.setLineups()


        self.gameDB.commit()
        endGame = time.clock()
        print((endGame-startGame)/60)
        print()
        self.gameDB.closeDB()



    def createTable(self, info):

        self.gameDB.executeCmd(createTableCmd.format(info))




################################################################################
################################################################################


if __name__ == "__main__":

    mlbDB = DB.MLBDatabase()
    mlbDB.openDB()
    today = datetime.date.today()


    filePath = "/home/ededub/FEFelson/MLBProjections/Lineups/{}.json".format("".join(str(today).split("-")))

    with open(filePath) as fileIn:
        info = json.load(fileIn)["matchups"]

    manager = DatabaseManager()

    for matchup in info:

        manager.createGameDB(mlbDB, matchup)

    mlbDB.closeDB()
