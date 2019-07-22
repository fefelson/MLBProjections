import sqlite3
import os

import MLBProjections.MLBProjections.DB.MLB as MLB
import MLBProjections.MLBProjections.Environ as ENV

from pprint import pprint

################################################################################
################################################################################


pitchContactCmd = """
                    SELECT pitches.game_id,
                            pitcher_id,
                            batter_id,
                            pitch_type_id,
                            pitch_result_id,
                            ab_type_id,
                            pitch_num,
                            box,
                            turn,
                            sequence,
                            pitch_velocity,
                            balls,
                            strikes,
                            outs,
                            (CASE WHEN pitcher.throws = batter.bats THEN 1 ELSE 0 END) AS side,
                            (CASE WHEN base_runners.first_base != -10 THEN 1 ELSE 0 END) AS first_base,
                            (CASE WHEN base_runners.second_base != -10 THEN 1 ELSE 0 END) AS second_base,
                            (CASE WHEN base_runners.third_base != -10 THEN 1 ELSE 0 END) AS third_base,
                            hit_style,
                            hit_hardness,
                            hit_angle,
                            hit_distance
                        FROM pitches
                        LEFT JOIN ab_results
                            ON pitches.pitch_id = ab_results.pitch_id
                        INNER JOIN pro_players AS pitcher
                            ON pitches.pitcher_id = pitcher.player_id
                        INNER JOIN pro_players AS batter
                            ON pitches.batter_id = batter.player_id
                        INNER JOIN pitch_locations
                            ON pitches.pitch_location_id = pitch_locations.pitch_location_id
                        INNER JOIN pitch_counts
                            ON pitches.pitch_count_id = pitch_counts.pitch_count_id
                        INNER JOIN base_runners
                            ON pitches.base_runners_id = base_runners.base_runners_id

                        WHERE {0[playerType]}_id = ?
                """



playerNameCmd = "SELECT first_name, last_name FROM pro_players WHERE player_id = ?"

leagueCmd = "SELECT league FROM pro_teams WHERE team_id = ?"

lineupCmd = """
            SELECT lineups.player_id, first_name, last_name, batt_order, lineups.pos
                FROM lineups
                INNER JOIN pro_players
                    ON lineups.player_id = pro_players.player_id
                INNER JOIN (SELECT team_id, MAX(game_id) AS game_id
                                FROM lineups
                                WHERE team_id = ?) AS max_id
                    ON lineups.game_id = max_id.game_id AND lineups.team_id = max_id.team_id
                WHERE sub_order = 1 AND lineups.pos != 'P'
                ORDER BY batt_order
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


################################################################################
################################################################################


class DatabaseManager:

    def __init__(self, db):

        self.mlbDB = db
        self.mlbDB.openDB()

        self.gameDBs = {}


    def __del__(self):
        self.db.closeDB()


    def findPlayer(self, playerId):
        return self.mlbDB.fetchOne("SELECT player_id FROM pro_players WHERE player_id = ?", (playerId,))


    def addPlayerToDB(self, info):
        print("new Player")
        self.mlbDB.insert(MLB.proPlayersTable, info=info )
        self.mlbDB.commit()


    def getLeague(self, teamId):
        return self.mlbDB.fetchOne(leagueCmd, (teamId,))[0]


    def update(self):
        self.mlbDB.update()


    def gameDBExists(self, index):
        return index in self.gameDBs.keys()


    def getRecentLineup(self, teamId):
        return self.mlbDB.fetchAll(lineupCmd, (teamId,))


    def cloneDB(self, matchup):
        gameDB = MLB.MLBGame(matchup.getGameId())
        if not os.path.exists(ENV.getPath("game", fileName=matchup.getGameId())):
            gameDB.openDB()

            info = matchup.getInfo()
            self.setMetaData(gameDB, info)
            self.setTeams(gameDB, info)
            self.setBullpens(gameDB, info)
            self.setLineups(gameDB, info)
            self.setContacts(gameDB, info)
            self.setGames(gameDB)

            gameDB.commit()
            gameDB.closeDB()
        self.gameDBs[matchup.getGameId()] = gameDB
        return gameDB


    def setGames(self, gameDB):
        for gameId in gameDB.fetchAll("SELECT DISTINCT game_id FROM pitch_contacts"):
            gameDB.insert(MLB.gamesTable, values=self.mlbDB.fetchOne("SELECT * FROM games WHERE game_id = ?",(gameId[0],)))


    def setMetaData(self, gameDB, info):
        gameId = info["gameId"]
        homeId = info["teams"]["home"]["info"]["team_id"]
        awayId = info["teams"]["away"]["info"]["team_id"]
        stadiumId = info["teams"]["home"]["info"]["stadium_id"]
        gameDB.insert(MLB.metaTable, values=(gameId, homeId, awayId, stadiumId))
        stadiumInfo = self.mlbDB.fetchOne("SELECT * FROM stadiums WHERE stadium_id = ?",(stadiumId,))
        gameDB.insert(MLB.stadiumsTable, values=stadiumInfo)


    def setContacts(self, gameDB, info):
        homeId = info["teams"]["home"]["info"]["team_id"]
        awayId = info["teams"]["away"]["info"]["team_id"]
        for teamId in (homeId, awayId):
            for data in self.mlbDB.fetchAll("SELECT hit_style, hit_hardness, hit_angle, hit_distance, ab_type_id FROM pitches INNER JOIN ab_results ON pitches.pitch_id = ab_results.pitch_id INNER JOIN games ON pitches.game_id = games.game_id WHERE (home_id = ? OR away_id = ?) AND hit_style != -1", (teamId, teamId)):
                cabId = gameDB.nextKey(MLB.contactAtBatsTable)
                try:
                    gameDB.insert(MLB.contactAtBatsTable, values=[cabId,teamId]+list(data))
                except sqlite3.IntegrityError:
                    pass


    def setBullpens(self, gameDB, info):
        for key in ("home", "away"):
            team = info["teams"][key]
            teamId = team["teamId"]

            starterId = team["starter"]["playerId"]
            self.newPitcher(teamId, starterId, gameDB, True)

            for pitcher in team["roster"]["pitchers"]:
                self.newPitcher(teamId, pitcher["playerId"], gameDB)


    def setLineups(self, gameDB, info):
        for key in ("home", "away"):
            team = info["teams"][key]
            teamId = team["teamId"]

            for batterId in [batter["playerId"] for batter in team["roster"]["batters"]]:
                self.newBatter(teamId, batterId, gameDB)

            if info["league"] == "NL":
                self.newBatter(teamId, team["starter"]["playerId"], gameDB)

            for batter in team["lineup"]:
                lId = gameDB.nextKey(MLB.lineupsTable)
                gameDB.insert(MLB.lineupsTable, values=(lId, info["gameId"], teamId, batter[0], batter[3], 1, batter[-1]))


    def setTeams(self, gameDB, info):
        homeId = info["teams"]["home"]["teamId"]
        awayId = info["teams"]["away"]["teamId"]

        for teamId in (homeId, awayId):
            teamInfo = self.mlbDB.fetchOne("SELECT * FROM pro_teams WHERE team_id = ?", (teamId,))
            gameDB.insert(MLB.proTeamsTable, values=teamInfo)


    def addPlayer(self, gameDB, playerId):
        playerInfo = self.mlbDB.curs.execute("SELECT * FROM pro_players WHERE player_id = ?",(playerId,)).fetchone()
        pprint(playerInfo)
        gameDB.insert(MLB.proPlayersTable, values=playerInfo)


    def newBatter(self, teamId, batterId, gameDB):
        if not gameDB.curs.execute("SELECT player_id FROM pro_players WHERE player_id = ?",(batterId,)).fetchone():
            self.addPlayer(gameDB, batterId)

        pitchCount = self.mlbDB.fetchOne("SELECT COUNT(batter_id) FROM pitches INNER JOIN pro_players ON pitches.batter_id = pro_players.player_id WHERE  batter_id = ?", (batterId,))[0]

        checkId = batterId
        checkTeamId = teamId

        if pitchCount < 100:
            checkId, checkTeamId = self.mlbDB.fetchOne(similarBatterCmd, (batterId,))

        pitchContacts = self.mlbDB.fetchAll(pitchContactCmd.format({"playerType":"batter"}), (checkId,))
        for contact in pitchContacts:
            pitchContactId = gameDB.nextKey(MLB.pitchContactsTable)
            try:
                gameDB.insert(MLB.pitchContactsTable, values=[pitchContactId, *contact[:2], batterId, *contact[3:]])
            except sqlite3.IntegrityError:
                pass



    def newPitcher(self, teamId, pitcherId, gameDB, starter=0):
        if not gameDB.curs.execute("SELECT player_id FROM pro_players WHERE player_id = ?",(pitcherId,)).fetchone():
            self.addPlayer(gameDB, pitcherId)

            bpId = gameDB.nextKey(MLB.bullpensTable)
            gameDB.insert(MLB.bullpensTable, values=(bpId, teamId, pitcherId, starter))


            pitchCount = self.mlbDB.fetchOne("SELECT COUNT(pitcher_id) FROM pitches INNER JOIN pro_players ON pitches.pitcher_id = pro_players.player_id WHERE pitcher_id = ?", (pitcherId,))[0]

            checkId = pitcherId
            checkTeamId = teamId
            try:
                if pitchCount < 100:
                    checkId, checkTeamId = self.mlbDB.fetchOne(similarPitcherCmd, (pitcherId,))

            except TypeError:
                pass

            pitches = self.mlbDB.fetchAll(pitchContactCmd.format({"playerType":"pitcher"}), (checkId,))
            for contact in pitches:
                pitchContactId = gameDB.nextKey(MLB.pitchContactsTable)
                try:
                    gameDB.insert(MLB.pitchContactsTable, values=[pitchContactId, contact[0], pitcherId, *contact[2:]])
                except sqlite3.IntegrityError:
                    pass


            for replace in self.mlbDB.fetchAll("SELECT * FROM pitcher_replace WHERE (remove_id = ? OR replace_id = ?)",(checkId, checkId)):
                try:
                    gameDB.insert(MLB.pitchReplaceTable, values=replace)
                except sqlite3.IntegrityError:
                    pass


################################################################################
################################################################################
