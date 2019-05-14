import random
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

pitchTypesCmd = {"selectCmdFormat": {"item": "pitch_type_id", "tableName": "pitchs"},
                    "innerCmdFormat": ({"joinTable": "pro_players", "joinNum": 1, "joinRelation": "main_table.batter_id = join_table_1.player_id"},),
                    "whereConditions": ("pitcher_id=?", "bats=?", "balls=?", "strikes=?")
                }


pitchVelocityCmd = {"selectCmdFormat": {"item": "pitch_velocity", "tableName": "pitchs"},
                    "whereConditions": ("pitcher_id=?", "pitch_type_id=?", "balls=?", "strikes=?")
                }



pitchLocationCmd = {"selectCmdFormat": {"item": "box", "tableName": "locations"},
                    "innerCmdFormat": ({"joinTable": "pitchs", "joinNum": 1, "joinRelation": "main_table.location_id = join_table_1.location_id"},
                                        {"joinTable": "pro_players", "joinNum": 2, "joinRelation": "join_table_1.batter_id = join_table_2.player_id"}),
                    "whereConditions": ("pitcher_id=?", "bats=?", "pitch_type_id=?", "balls=?", "strikes=?")
                }



batterResultCmd = {"selectCmdFormat": {"item": "game_id, pitch_num, pitch_result_id", "tableName": "pitchs"},
                    "innerCmdFormat": ({"joinTable": "locations", "joinNum": 1, "joinRelation": "main_table.location_id = join_table_1.location_id"},
                                        {"joinTable": "pro_players", "joinNum": 2, "joinRelation": "main_table.pitcher_id = join_table_2.player_id"}),
                    "whereConditions": ("batter_id=?", "pitch_type_id=?", "throws=?", "box=?", "(pitch_velocity BETWEEN ? AND ?)", "strikes=?", "balls=?")
                }


hitResultCmd = {"selectCmdFormat": {"item": "title", "tableName": "hit_results"},
                    "innerCmdFormat": ({"joinTable": "results", "joinNum": 1, "joinRelation": "main_table.hit_result_id = join_table_1.hit_result_id"},
                                        {"joinTable": "contact_types", "joinNum": 2, "joinRelation": "join_table_1.contact_type_id = join_table_2.contact_type_id"}),
                    "whereConditions": ("batter_id=?", "hit_hardness=?", "hit_angle=?", "hit_style=?")
                }


pitcherResultCmd = {"selectCmdFormat": {"item": "pitch_result_id", "tableName": "pitchs"},
                    "innerCmdFormat": ({"joinTable": "locations", "joinNum": 1, "joinRelation": "main_table.location_id = join_table_1.location_id"},
                                        {"joinTable": "pro_players", "joinNum": 2, "joinRelation": "main_table.batter_id = join_table_2.player_id"}),
                    "whereConditions": ("pitcher_id=?", "pitch_type_id=?", "bats=?", "box=?", "(pitch_velocity BETWEEN ? AND ?)", "strikes=?", "balls=?")
                }



################################################################################
################################################################################


class PlateAppearance:

    def __init__(self, pitcherId, batterId, umpire):

        print(pitcherId, umpire.db.curs.execute("SELECT first_name, last_name, throws FROM pro_players WHERE player_id = ?", (pitcherId,)).fetchone())
        print(batterId, umpire.db.curs.execute("SELECT first_name, last_name, bats FROM pro_players WHERE player_id = ?", (batterId,)).fetchone())


        self.pitcher = pitcherId
        self.throws = umpire.db.curs.execute("SELECT throws FROM pro_players WHERE player_id = ?",(self.pitcher,) ).fetchone()[0]
        #self.catcherId = catcherId
        #self.fielders = fielders
        self.batter = batterId
        self.bats = umpire.db.curs.execute("SELECT bats FROM pro_players WHERE player_id = ?",(self.batter,) ).fetchone()[0]
        #self.baseRunners = baseRunners
        self.umpire = umpire

        self.result = self.runPA()
        print(self.result)


    def getResult(self, cmd, args):
        #pprint(cmd)
        results = self.umpire.db.curs.execute(cmd, args).fetchall()
        index = round(random.random() * (len(results)-1))
        #pprint(results)
        #print("\n\nLength {}   Index {}".format(len(results), index))
        return results[index]


    def getPitchType(self, balls, strikes, attempt=0):
        args = [self.pitcher, self.bats, balls, strikes]
        args = args if not attempt else args[:attempt]
        cmd = formCmd(attempt, pitchTypesCmd)
        try:
            result = self.getResult(cmd, args)[0]
        except IndexError:
            result = self.getPitchType(balls, strikes, attempt-1)
        return result


    def getPitchVelocity(self, pitchType, balls, strikes, attempt=0):
        args = [self.pitcher, pitchType, balls, strikes]
        args = args if not attempt else args[:attempt]
        cmd = formCmd(attempt, pitchVelocityCmd)
        try:
            result = self.getResult(cmd, args)[0]
        except IndexError:
            result = self.getPitchVelocity(pitchType, balls, strikes, attempt-1)
        return result


    def getPitchLocation(self, pitchType, balls, strikes, attempt=0):
        args = [self.pitcher, self.bats, pitchType, balls, strikes]
        args = args if not attempt else args[:attempt]
        cmd = formCmd(attempt, pitchLocationCmd)
        try:
            result = self.getResult(cmd, args)[0]
        except IndexError:
            result = self.getPitchLocation(pitchType, balls, strikes, attempt-1)
        return result


    def getBatterResult(self, pitchType, pitchLocation, pitchVelocity, strikes, balls, attempt=0):
        pitchTuple = (pitchVelocity-2, pitchVelocity+2)

        if attempt > -3:
            args = [self.batter, pitchType, self.throws, pitchLocation, *pitchTuple, strikes, balls]
        else:
            args = [self.batter, pitchType, self.throws, pitchLocation, pitchVelocity, strikes, balls]
        args = args if not attempt else args[:attempt]
        cmd = formCmd(attempt, batterResultCmd)
        try:
            result = self.getResult(cmd, args)
        except IndexError:
            result = self.getBatterResult(pitchType, pitchLocation, pitchVelocity, strikes, balls, attempt-1)
        return result


    def getHitResult(self, hitHard, hitAngle, hitStyle):

        args = [self.batter, hitHard, hitAngle, hitStyle]
        cmd = formCmd(0, hitResultCmd)
        result = self.getResult(cmd, args)[0]
        return result


    def runPA(self):
        self.umpire.resetCount()

        while True:
            hitResult = None
            balls, strikes = self.umpire.getCount()
            #print("COUNT: Balls {}  Strikes {}".format(balls,strikes))
            pitchType = self.getPitchType(balls, strikes)
            pitchLabel = self.umpire.db.curs.execute("SELECT title FROM pitch_types WHERE pitch_type_id = ?",(pitchType,)).fetchone()[0]
            pitchVelocity = self.getPitchVelocity(pitchType, balls, strikes)
            pitchLocation = self.getPitchLocation(pitchType, balls, strikes)
            #print("\n{}  {}\n".format(pitchLabel, pitchVelocity))
            # for y in range(5):
            #     row = [(y*5)+x for x in range(1,6)]
            #     rowFormat = []
            #     for i in row:
            #         if i == pitchLocation:
            #             rowFormat.append("XX")
            #         else:
            #             rowFormat.append("{:2d}".format(i))
            #     print(rowFormat)

            batterResult = self.getBatterResult(pitchType, pitchLocation, pitchVelocity, strikes, balls)
            resultLabel = self.umpire.db.curs.execute("SELECT title FROM pitch_results WHERE pitch_result_id = ?",(batterResult[-1],)).fetchone()[0]
            #print("\n{}\n".format(resultLabel))
            try:
                if batterResult[-1] == 10:
                    gameId, pitchNum = batterResult[:-1]
                    hitHard, hitAngle, hitStyle = self.umpire.db.curs.execute("SELECT hit_hardness, hit_angle, hit_style FROM contact_types INNER JOIN results ON contact_types.contact_type_id = results.contact_type_id WHERE game_id = ? AND play_num = ?",(gameId, int(pitchNum)+1)).fetchone()
                    hitResult = self.getHitResult(hitHard, hitAngle, hitStyle)
                #runner = Runner(self.umpire.getScoreKeeper(), self.pitchId, self.catcherId, self.baseRunners)
                outcome, tag = self.umpire.pitchRuling(batterResult[-1], hitResult)
            except TypeError:
                outcome = "Out"
            #input("\n\n")
            if outcome:
                return tag




################################################################################
################################################################################


if __name__ == "__main__":

    db = DB.MLBDatabase()
    db.openDB()
    pa = PlateAppearance(pitcherId=7578, batterId=9111, umpire=Umpire(db))
    db.closeDB()
