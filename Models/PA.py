import random
import sqlite3
import numpy

from MLBProjections.MLBProjections.Models.Umpire import Umpire
import MLBProjections.MLBProjections.DB.MLB as DB

################################################################################
################################################################################


def formCmd(attempt, cmdValues):
    cmd = selectCmd.format(cmdValues["selectCmdFormat"])
    for innerJoin in cmdValues.get("innerCmdFormat", []):
        cmd += innerCmd.format(innerJoin)
    whereConditions = whereFunc(attempt, cmdValues["whereConditions"])
    cmd += whereCmd.format({"whereConditions": whereConditions})
    return cmd


################################################################################
################################################################################


class PlateAppearance:


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










################################################################################
################################################################################
