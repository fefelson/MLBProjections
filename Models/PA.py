import random
import sqlite3
from pprint import pprint

from MLBProjections.MLBProjections.Models.Umpire import Umpire
import MLBProjections.MLBProjections.DB.MLB as DB

################################################################################
################################################################################


selectCmd = "SELECT {0[item]} FROM {0[tableName]} AS main_table "

innerCmd = "INNER JOIN {0[joinTable]} AS join_table_{0[joinNum]} ON {0[joinRelation]} "

whereCmd = "WHERE {0[whereConditions]} "


def whereFunc(num, args):
    return " AND ".join([arg for arg in args[:num]]) if num else " AND ".join([arg for arg in args])


def formCmd(attempt, cmdValues):
    cmd = selectCmd.format(cmdValues["selectCmdFormat"])
    for innerJoin in cmdValues.get("innerCmdFormat", []):
        cmd += innerCmd.format(innerJoin)
    whereConditions = whereFunc(attempt, cmdValues["whereConditions"])
    cmd += whereCmd.format({"whereConditions": whereConditions})
    return cmd



# TODO: select multiple Items in selectCmdFormat

pitchTypesCmd = {"selectCmdFormat": {"item": "pitch_type_id", "tableName": "pitches"},
                    "innerCmdFormat": ({"joinTable": "pro_players", "joinNum": 1, "joinRelation": "main_table.batter_id = join_table_1.player_id"},),
                    "whereConditions": ("pitch_type_id != 7", "pitcher_id=?", "bats=?", "balls=?", "strikes=?")
                }


pitchVelocityCmd = {"selectCmdFormat": {"item": "velocity", "tableName": "pitches"},
                    "whereConditions": ("pitcher_id=?", "pitch_type_id=?", "balls=?", "strikes=?")
                }


pitchLocationCmd = {"selectCmdFormat": {"item": "box", "tableName": "pitch_locations"},
                    "innerCmdFormat": ({"joinTable": "pitches", "joinNum": 1, "joinRelation": "main_table.location_id = join_table_1.location_id"},
                                        {"joinTable": "pro_players", "joinNum": 2, "joinRelation": "join_table_1.batter_id = join_table_2.player_id"}),
                    "whereConditions": ("pitcher_id=?", "bats=?", "pitch_type_id=?", "balls=?", "strikes=?")
                }


batterResultCmd = {"selectCmdFormat": {"item": "pitch_id, pitch_result_id", "tableName": "pitches"},
                    "innerCmdFormat": ({"joinTable": "pitch_locations", "joinNum": 1, "joinRelation": "main_table.location_id = join_table_1.location_id"},
                                        {"joinTable": "pro_players", "joinNum": 2, "joinRelation": "main_table.pitcher_id = join_table_2.player_id"}),
                    "whereConditions": ("batter_id=?", "pitch_type_id=?", "throws=?", "box=?", "(velocity BETWEEN ? AND ?)",)
                }


hitResultCmd = {"selectCmdFormat": {"item": "title", "tableName": "result_types"},
                    "innerCmdFormat": ({"joinTable": "ab_results", "joinNum": 1, "joinRelation": "main_table.result_type_id = join_table_1.result_type_id"},
                                        {"joinTable": "contacts", "joinNum": 2, "joinRelation": "join_table_1.contact_id = join_table_2.contact_id"}),
                    "whereConditions": ("stadium_id=?", "hit_style=?", "hit_hardness=?", "hit_angle=?", )
                }


pitcherResultCmd = {"selectCmdFormat": {"item": "pitch_result_id", "tableName": "pitches"},
                    "innerCmdFormat": ({"joinTable": "pitch_locations", "joinNum": 1, "joinRelation": "main_table.location_id = join_table_1.location_id"},
                                        {"joinTable": "pro_players", "joinNum": 2, "joinRelation": "main_table.batter_id = join_table_2.player_id"}),
                    "whereConditions": ("pitcher_id=?", "pitch_type_id=?", "bats=?", "box=?", "(velocity BETWEEN ? AND ?)", "strikes=?", "balls=?")
                }


################################################################################
################################################################################


class PlateAppearance:

    def __init__(self, pitcher, batter, umpire):



        self.pitcher = pitcher
        try:
            *pName, throws = umpire.db.curs.execute("SELECT first_name, last_name, throws FROM pro_players WHERE player_id = ?", (pitcher,)).fetchone()
        except TypeError:
            pName = "First","Last"
            throws = "R"
        self.throws = throws
        #self.catcherId = catcherId
        #self.fielders = fielders
        self.batter = batter
        *bName, bats = umpire.db.curs.execute("SELECT first_name, last_name, bats FROM pro_players WHERE player_id = ?", (batter,)).fetchone()
        self.bats = bats
        #self.baseRunners = baseRunners
        self.umpire = umpire

        print()
        print(pName)
        print(bName)
        print()

        self.result = self.runPA()
        print(self.result)


    def getResult(self, cmd, args):
        #pprint(cmd)
        answer = None
        results = self.umpire.db.curs.execute(cmd, args).fetchall()

        index = round(random.random() * (len(results)-1))

        try:
            answer = results[index]
        except IndexError:
            raise
            # print()
            # pprint(cmd)
            # print(args)
            # print()
            # raise
        #print(results)
        #print("\n\nLength {}   Index {}".format(len(results), index))
        return answer


    def getPitchType(self, balls, strikes, attempt=0):
        args = [self.pitcher, self.bats, balls, strikes]
        args = args if not attempt else args[:attempt]
        cmd = formCmd(attempt, pitchTypesCmd)
        try:
            result = self.getResult(cmd, args)[0]
        except IndexError:
            if attempt > -3:
                result = self.getPitchType(balls, strikes, attempt-1)
            else:
                result = 1
        except sqlite3.ProgrammingError:
            self.umpire.db.openDB()
            result = 1

        return result


    def getPitchVelocity(self, pitchType, balls, strikes, attempt=0):
        args = [self.pitcher, pitchType, balls, strikes]
        args = args if not attempt else args[:attempt]
        cmd = formCmd(attempt, pitchVelocityCmd)
        try:
            result = self.getResult(cmd, args)[0]
        except IndexError:
            if attempt > -3:
                result = self.getPitchVelocity(pitchType, balls, strikes, attempt-1)
            else:
                result = 90
        except sqlite3.ProgrammingError:
            self.umpire.db.openDB()
            result = 90
        return result


    def getPitchLocation(self, pitchType, balls, strikes, attempt=0):
        args = [self.pitcher, self.bats, pitchType, balls, strikes]
        args = args if not attempt else args[:attempt]
        cmd = formCmd(attempt, pitchLocationCmd)
        try:
            result = self.getResult(cmd, args)[0]
        except IndexError:
            if attempt > -3:
                result = self.getPitchLocation(pitchType, balls, strikes, attempt-1)
            else:
                result = 13
        except sqlite3.ProgrammingError:
            self.umpire.db.openDB()
            result = 13
        return result


    def getBatterResult(self, pitchType, pitchLocation, pitchVelocity, attempt=0):
        pitchTuple = (pitchVelocity-2, pitchVelocity+2)

        if attempt > -1:
            args = [self.batter, pitchType, self.throws, pitchLocation, *pitchTuple,]
            cmd = formCmd(attempt, batterResultCmd)
        elif attempt == -1:
            args = [self.batter, pitchType, self.throws, pitchLocation,]
            cmd = formCmd(attempt, batterResultCmd)
        elif attempt == -2:
            cmd = "SELECT pitch_id, pitch_result_id FROM pitches AS main_table INNER JOIN pro_players AS join_table_2 ON main_table.pitcher_id = join_table_2.player_id WHERE batter_id=? AND pitch_type_id=? AND throws=?"
            args = [self.batter, pitchType, self.throws]

        elif attempt <= -3:
            cmd = "SELECT pitch_id, pitch_result_id FROM pitches AS main_table WHERE batter_id=? AND pitch_type_id=?"
            args = [self.batter, pitchType]


        try:
            result = self.getResult(cmd, args)
        except IndexError:
            if attempt > -4:
                result = self.getBatterResult(pitchType, pitchLocation, pitchVelocity, attempt-1)
            else:
                strikeZone = self.umpire.db.curs.execute("SELECT strike_zone FROM pitch_locations WHERE box = ?",(pitchLocation, )).fetchone()[0]
                result = (-1, 2) if strikeZone == "True" else (-1,0)
            # pprint(cmd)
            # print(args)
            # print("\n\n")
        except sqlite3.ProgrammingError:
            self.umpire.db.openDB()
            strikeZone = self.umpire.db.curs.execute("SELECT strike_zone FROM pitch_locations WHERE box = ?",(pitchLocation, )).fetchone()[0]
            result = (-1, 2) if strikeZone == "True" else (-1,0)

        return result


    def getHitResult(self, hitStyle, hitHard, hitAngle, attempt=0):
        args = [self.umpire.stadiumId,  hitStyle, hitHard, hitAngle,]
        args = args if not attempt else args[:attempt]
        cmd = formCmd(attempt, hitResultCmd)
        try:
            result = self.getResult(cmd, args)[0]
        except IndexError:
            result = self.getHitResult(hitStyle, hitHard, hitAngle, attempt-1)
        except sqlite3.ProgrammingError:
            self.umpire.db.openDB()
            result = "Fielder's Choice"
        return result


    def runPA(self):
        self.umpire.resetCount()

        pitchCount = 0

        while True:

            hitResult = None
            tag = "Out"

            balls, strikes = self.umpire.getCount()

            # print("COUNT: Balls {}  Strikes {}".format(balls,strikes))
            pitchType = self.getPitchType(balls, strikes)
            pitchLabel = self.umpire.db.curs.execute("SELECT title FROM pitch_types WHERE pitch_type_id = ?",(pitchType,)).fetchone()[0]
            pitchVelocity = self.getPitchVelocity(pitchType, balls, strikes)
            pitchLocation = self.getPitchLocation(pitchType, balls, strikes)
            # print("\n{}  {}\n".format(pitchLabel, pitchVelocity))
            # for y in range(5):
            #     row = [(y*5)+x for x in range(1,6)]
            #     rowFormat = []
            #     for i in row:
            #         if i == pitchLocation:
            #             rowFormat.append("XX")
            #         else:
            #             rowFormat.append("{:2d}".format(i))
            #     print(rowFormat)


            try:
                batterResult = self.getBatterResult(pitchType, pitchLocation, pitchVelocity)
                resultLabel = self.umpire.db.curs.execute("SELECT title FROM pitch_results WHERE pitch_result_id = ?",(batterResult[-1],)).fetchone()[0]
            except TypeError:
                resultLabel = "Ball"
            # print("\n{}\n".format(resultLabel))
            # input(batterResult)
            self.umpire.scoreKeeper.pitch(self.pitcher)
            try:
                if batterResult[-1] == 10:
                    pitchId = batterResult[0]

                    hitHard, hitAngle, hitStyle = self.umpire.db.curs.execute("SELECT hit_hardness, hit_angle, hit_style FROM contacts WHERE contacts.pitch_id = ?",(pitchId, )).fetchone()
                    hitResult = self.getHitResult(hitStyle, hitHard, hitAngle)
                #runner = Runner(self.umpire.getScoreKeeper(), self.pitchId, self.catcherId, self.baseRunners)
                outcome, tag = self.umpire.pitchRuling(batterResult[-1], hitResult)
            except TypeError:
                outcome = "Out"
                tag = "Out"


            #     outcome = "Out"
            pitchCount += 1
            if pitchCount > 20:
                outcome = "Out"
                tag = "Out"
            # #input("\n\n")
            if outcome:
                return tag




################################################################################
################################################################################


if __name__ == "__main__":

    db = DB.MLBDatabase()
    db.openDB()
    pa = PlateAppearance(pitcherId=7578, batterId=9111, umpire=Umpire(db))
    db.closeDB()
