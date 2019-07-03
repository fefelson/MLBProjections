import random
import sqlite3
import numpy
from pprint import pprint
from sklearn.linear_model import LogisticRegression as LogReg
from sklearn.linear_model import LinearRegression as LinReg

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

pitcherResultCmd = {"selectCmdFormat": {"item": "pitch_type_id, velocity, box, pitch_result_id", "tableName": "pitch_contacts"},
                    "innerCmdFormat": [],
                    "whereConditions": ("pitch_type_id != 7", "pitcher_id=?", "side=?", "balls=?", "strikes=?", "turn=?", "sequence=?")
                }


batterResultCmd = {"selectCmdFormat": {"item": "pitch_result_id", "tableName": "pitch_contacts"},
                    "innerCmdFormat": [],
                    "whereConditions": ("batter_id=?", "side=?",  "box=?", "pitch_type_id=?","velocity>= ?", "velocity <= ?", "balls=?", "strikes=?", "turn=?", "sequence=?")
                }


hitResultCmd = {"selectCmdFormat": {"item": "hit_style, hit_hardness, hit_angle, hit_distance", "tableName": "pitch_contacts"},
                    "innerCmdFormat": [],
                    "whereConditions": ("pitch_result_id=10", "batter_id=?", "side=?", "box=?", "pitch_type_id=?", "velocity>= ?", "velocity <= ?")
                }


inPlayResultCmd = {"selectCmdFormat": {"item": "title", "tableName": "result_types"},
                "innerCmdFormat": ({"joinTable": "contacts_at_bats", "joinNum": 1, "joinRelation": "main_table.result_type_id = join_table_1.ab_type_id"},),
                "whereConditions": ("hit_style=?", "hit_hardness=?", "hit_angle=?", "hit_distance=?")
            }









################################################################################
################################################################################


class PlateAppearance:

    def __init__(self, pitcher, batter, umpire):


        # playerId, firstName, lastName, throws
        self.pitcher = pitcher
        # playerId, firstName, lastName, bats
        self.batter = batter
        self.umpire = umpire


        print()
        print("Pitching:  {} {}   throws: {}".format(*pitcher[1:]))
        print("Batting:  {} {}   bats: {}".format(*batter[1:]))
        print()

        self.batSide = int(batter[-1] == pitcher[-1])

        self.result = self.runPA()
        print(self.result)


    def getResult(self, cmd, args):
        #pprint(cmd)
        answer = None
        results = self.umpire.db.fetchAll(cmd, args)


        answer = random.choice(results)
        return answer


    def getPitch(self, turn, sequence, side, balls, strikes, attempt=0):
        args = [self.pitcher[0], self.batSide, int(balls), int(strikes), int(turn), int(sequence)]
        args = args if not attempt else args[:attempt]
        cmd = formCmd(attempt, pitcherResultCmd)
        try:
            result = self.getResult(cmd, args)
        except IndexError:
            result = self.getPitch(turn, sequence, side, balls, strikes, attempt-1)

        return result


    def getBatResult(self, pitchType, box, pitchVelocity, side, balls, strikes, turn, sequence, attempt=0):
        pitchTuple = (pitchVelocity-2, pitchVelocity+2)
        args = [self.batter[0], side, int(box), int(pitchType), *pitchTuple, int(balls), int(strikes), int(turn), int(sequence)]
        args = args if not attempt else args[:attempt]
        result = None

        if attempt != -5:
            cmd = formCmd(attempt, batterResultCmd)

        try:
            result = self.getResult(cmd, args)[0]


        except IndexError:
            result = self.getBatResult(pitchType, box, pitchVelocity, side, balls, strikes, turn, sequence, attempt-1)


        except UnboundLocalError:
            pass
        except (ValueError, sqlite3.OperationalError):
            result = self.umpire.db.fetchOne("SELECT (CASE WHEN strike_zone = 'True' THEN 1 ELSE 0 END) FROM pitch_locations WHERE box = ?",(box,))[0]
        if result == None:
            result = self.getBatResult(pitchType, box, pitchVelocity, side, balls, strikes, turn, sequence, attempt-1)
        return result


    def getContact(self, pitchType, box, pitchVelocity, side, attempt=0):
        pitchTuple = (int(pitchVelocity)-2, int(pitchVelocity)+2)
        args = [int(self.batter[0]), side, int(box), int(pitchType),*pitchTuple]
        args = args if not attempt else args[:attempt]
        result = [None,]

        if attempt != -1:
            cmd = formCmd(attempt, hitResultCmd)

        try:
            result = self.getResult(cmd, args)
        except IndexError:
            result = self.getContact(pitchType, box, pitchVelocity, side, attempt-1)
        except sqlite3.ProgrammingError:
            pass
        except UnboundLocalError:
            pass
        except sqlite3.OperationalError:
            result = (1,1,1,1)


        if result[0] == None:
            result = self.getContact(pitchType, box, pitchVelocity, side, attempt-1)


        return result


    def getInPlayResult(self, hitStyle, hitHard, hitAngle, hitDistance, attempt=0):
        args = [hitStyle, hitHard, hitAngle, hitDistance]
        args = args if not attempt else args[:attempt]
        result = [None,]
        cmd = formCmd(attempt, inPlayResultCmd)
        try:
            result = self.getResult(cmd, args)[0]

        except IndexError:
            result = self.getInPlayResult(hitStyle, hitHard, hitAngle, hitDistance, attempt-1)
        if not result[0]:
            result = self.getInPlayResult(hitStyle, hitHard, hitAngle, hitDistance, attempt-1)

        return result




    def runPA(self):
        self.umpire.resetCount()

        sequence = 1
        turn = self.umpire.scoreKeeper.getTurn(self.batter, self.pitcher)
        self.prevPitch1 = 0
        self.prevPitch2 = 0
        self.prevBox1 = -1
        self.prevBox2 = -1

        while True:

            pitchNum = self.umpire.scoreKeeper.getPitchNum()


            hitResult = None
            tag = "Out"

            balls, strikes = self.umpire.getCount()

            # print("COUNT: Balls {}  Strikes {}".format(balls,strikes))
            pitch = self.getPitch(turn, sequence, self.batSide, balls, strikes)
            pitchType, pitchVelocity, pitchLocation, pitcherResult = pitch
            pitchLabel = self.umpire.db.fetchOne("SELECT title FROM pitch_types WHERE pitch_type_id = ?", (pitchType,))[0]
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

            batterResult = self.getBatResult(pitchType, pitchLocation, pitchVelocity, self.batSide, balls, strikes, turn, sequence)

            result = random.choice([pitcherResult, batterResult])



            #print("\n{}\n".format(resultLabel))
            self.umpire.scoreKeeper.pitch(self.pitcher)
            if result == 10:

                contact = self.getContact(pitchType, pitchLocation, pitchVelocity, self.batSide)

                hitResult = self.getInPlayResult(*contact)
            #runner = Runner(self.umpire.getScoreKeeper(), self.pitchId, self.catcherId, self.baseRunners)
            outcome, tag = self.umpire.pitchRuling(result, hitResult)



            self.prevPitch2 = self.prevPitch1 = 0
            self.prevBox1 = -1
            self.prevBox2 = -1


            #     outcome = "Out"
            sequence += 1
            if sequence > 20:
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
