from . import Database as DB
from ..Models.ScoreKeeper import inPlayResults, pitchLocations, pitchTypes, pitchResults, sortingHat
import MLBProjections.MLBProjections.Environ as ENV

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
                            season_type TEXT NOT NULL,
                            stadium_id INT NOT NULL,
                            FOREIGN KEY (home_id) REFERENCES pro_teams (team_id),
                            FOREIGN KEY (away_id) REFERENCES pro_teams (team_id),
                            FOREIGN KEY (winner_id) REFERENCES pro_teams (team_id),
                            FOREIGN KEY (loser_id) REFERENCES pro_teams (team_id),
                            FOREIGN KEY (stadium_id) REFERENCES stadiums (stadium_id)
                            """,
                "index": "season, game_date"
                }


locationsTable = {
                    "tableName": "locations",
                    "tableCols": ("location_id", "x_value", "y_value", "box", "strike_zone"),
                    "tableCmd": """
                                location_id INT PRIMARY KEY,
                                x_value INT NOT NULL,
                                y_value INT NOT NULL,
                                box INT NOT NULL,
                                strike_zone TEXT NOT NULL
                                """,
                    "index": "x_value, y_value"
                    }


pitchsTable = {
                "tableName": "pitchs",
                "tableCols": ("game_id", "pitch_num", "pitcher_id", "batter_id",
                                "location_id", "pitch_type_id", "pitch_velocity",
                                "balls", "strikes", "pitch_result_id"),
                "tableCmd": """
                            game_id INT NOT NULL,
                            pitch_num INT NOT NULL,
                            pitcher_id INT NOT NULL,
                            batter_id INT NOT NULL,
                            location_id INT NOT NULL,
                            pitch_type_id INT NOT NULL,
                            pitch_velocity INT NOT NULL,
                            balls INT NOT NULL,
                            strikes INT NOT NULL,
                            pitch_result_id INT NOT NULL,
                            PRIMARY KEY (game_id, pitch_num),
                            FOREIGN KEY (game_id) REFERENCES games (game_id),
                            FOREIGN KEY (pitcher_id) REFERENCES pro_players (player_id),
                            FOREIGN KEY (batter_id) REFERENCES pro_players (player_id),
                            FOREIGN KEY (location_id) REFERENCES locations (location_id),
                            FOREIGN KEY (pitch_type_id) REFERENCES pitch_types (pitch_type_id),
                            FOREIGN KEY (pitch_result_id) REFERENCES pitch_results (pitch_result_id)
                            """,
                "index": "pitcher_id, pitch_type_id, pitch_velocity, balls, strikes"
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


proPlayersTable = {
                    "tableName": "pro_players",
                    "tableCols": ("player_id", "first_name", "last_name", "bats", "throws"),
                    "tableCmd": """
                                player_id INT PRIMARY KEY,
                                first_name TEXT NOT NULL,
                                last_name TEXT NOT NULL,
                                bats TEXT NOT NULL,
                                throws TEXT NOT NULL
                                """
                    }


proTeamsTable = {
                    "tableName": "pro_teams",
                    "tableCols": ("team_id", "abrv", "city", "mascot"),
                    "tableCmd": """
                                team_id INT PRIMARY KEY,
                                abrv TEXT NOT NULL,
                                city TEXT NOT NULL,
                                mascot TEXT NOT NULL
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


hitResultsTable = {

                    "tableName": "hit_results",
                    "tableCols": ("hit_result_id", "result_tag", "title"),
                    "tableCmd": """
                                hit_result_id INT PRIMARY KEY,
                                result_tag TEXT NOT NULL,
                                title TEXT NOT NULL
                                """
                }


#TODO: Current configuration DEMANDS an index
contactTypeTable = {
                        "tableName": "contact_types",
                        "tableCols": ("contact_type_id", "hit_angle", "hit_distance",
                                        "hit_hardness", "hit_style"),
                        "tableCmd": """
                                    contact_type_id INT PRIMARY KEY,
                                    hit_angle INT NOT NULL,
                                    hit_distance INT NOT NULL,
                                    hit_hardness INT NOT NULL,
                                    hit_style INT NOT NULL
                                    """,
                        "index": "hit_angle, hit_distance, hit_hardness, hit_style"
}


resultTable = {
                    "tableName": "results",
                    "tableCols": ("game_id", "play_num", "batter_id", "pitcher_id", "contact_type_id", "hit_result_id" ),
                    "tableCmd": """
                                game_id INT NOT NULL,
                                play_num INT NOT NULL,
                                batter_id INT NOT NULL,
                                pitcher_id INT NOT NULL,
                                contact_type_id INT NOT NULL,
                                hit_result_id INT NOT NULL,
                                PRIMARY KEY (game_id, play_num),
                                FOREIGN KEY (batter_id) REFERENCES pro_players (player_id),
                                FOREIGN KEY (pitcher_id) REFERENCES pro_players (player_id),
                                FOREIGN KEY (contact_type_id) REFERENCES contact_types (contact_type_id),
                                FOREIGN KEY (hit_result_id) REFERENCES hit_results (hit_result_id)
                                """,
                    "index": "batter_id, contact_type_id"
}


lineupTable = {
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

rosterTable = {
                "tableName": "rosters",
                "tableCols": ("game_id", "player_id", "team_id"),
                "tableCmd": """
                            game_id INT NOT NULL,
                            player_id INT NOT NULL,
                            team_id INT NOT NULL,
                            PRIMARY KEY (game_id, player_id),
                            FOREIGN KEY (game_id) REFERENCES games (game_id),
                            FOREIGN KEY (player_id) REFERENCES pro_players (player_id),
                            FOREIGN KEY (team_id) REFERENCES pro_teams (team_id)
                            """
}

################################################################################
################################################################################


class MLBDatabase(DB.Database):

    def __init__(self):
        super().__init__(ENV.getPath("database", fileName="mlb"))


    def getTableList(self):
        return [gamesTable, locationsTable, pitchsTable, pitchTypesTable,
            pitchResultsTable, proPlayersTable, proTeamsTable, stadiumsTable, hitResultsTable,
            contactTypeTable, resultTable, lineupTable, rosterTable]


    def seed(self):
        for i, location in enumerate(pitchLocations):
            self.insert(locationsTable, (i, *location, sortingHat(*location), str(False if abs(location[0]) > 10000 or abs(location[1]) > 10000 else True)))

        for info in pitchTypes:
            self.insert(pitchTypesTable, info)

        for info in pitchResults:
            self.insert(pitchResultsTable, info)

        for i, info in enumerate(inPlayResults):
            self.insert(hitResultsTable, (i,*info))

        self.commit()
