from abc import ABCMeta, abstractmethod
import random

from pprint import pprint

################################################################################
################################################################################


pitchContactCmd = """
                    SELECT {0[itemCmd]}
                        FROM pitch_contacts
                        INNER JOIN ({0[gdCmd]}) AS gd
                            ON pitch_contacts.game_id = gd.game_id
                        WHERE {0[whereCmd]}
                    """


probPitchContactCmd = """
                        SELECT {0[itemCmd]}
                            FROM pitch_contacts
                            INNER JOIN ({0[gdCmd]}) AS gd
                                ON pitch_contacts.game_id = gd.game_id
                            WHERE {0[whereCmd]}
                            GROUP BY {0[itemCmd]}
                            ORDER BY COUNT({0[itemCmd]}) DESC
                        """


abResultCmd = """
                SELECT title
                    FROM ab_types
                    INNER JOIN contact_at_bats
                        ON ab_types.ab_type_id = contact_at_bats.ab_type_id
                    WHERE {0[whereCmd]}
                """


def whereFunc(args):
    whereList = []
    for arg in args:
        for item in arg.split(","):
            if item.split("-")[-1] == "gtn":
                whereList.append("{}>=?".format(item.split("-")[0].strip()))
            elif item.split("-")[-1] == "ltn":
                whereList.append("{}<=?".format(item.split("-")[0].strip()))
            else:
                whereList.append("{}=?".format(item.strip()))
    return " AND ".join(whereList)


################################################################################
################################################################################


class OutcomeType(metaclass=ABCMeta):

    def __init__(self, dungeonMaster):

        self.dungeonMaster = dungeonMaster


    @abstractmethod
    def getPitch(self, pitcher, batter, scoreKeeper):
        pass


    @abstractmethod
    def getSwing(self, pitcher, batter, pitch, scoreKeeper):
        pass


    @abstractmethod
    def getPitcherContact(self, pitcher, batter, pitch):
        pass


    @abstractmethod
    def getBatterContact(self, pitcher, batter, pitch):
        pass


    @abstractmethod
    def getContactResult(self, contact, scoreKeeper):
        pass



################################################################################
################################################################################


class RandomOutcome(OutcomeType):

    def __init__(self, dungeonMaster):
        super().__init__(dungeonMaster)


    def getPitch(self, pitcher, batter, scoreKeeper, diamondState):
        itemCmd = "pitch_type_id, pitch_velocity, box, pitch_result_id"

        argList = ["pitcher_id", "side", "balls, strikes",
                    "first_base, second_base, third_base", "turn, sequence"]

        values = {"pitcher_id":pitcher.getId(),
                    "side": int(batter.getBatSide() == pitcher.getThrowSide()),
                    "balls": scoreKeeper.getBalls(),
                    "strikes": scoreKeeper.getStrikes(),
                    "turn": scoreKeeper.getTurn(batter),
                    "sequence": scoreKeeper.getSequence()}
        for base in ("first_base", "second_base", "third_base"):
            values[base] = int(base in diamondState.split("_"))

        gdCmd = pitcher.getGDCmd()
        mainCmd = pitchContactCmd
        return self.dungeonMaster.getRandomItem(mainCmd, itemCmd, gdCmd, argList, values)


    def getSwing(self, pitcher, batter, pitch, scoreKeeper, diamondState):
        itemCmd = "pitch_result_id"

        argList = ["batter_id", "side", "pitch_type_id", "pitch_velocity-gtn, pitch_velocity-ltn",
                    "box", "strikes, balls", "first_base, second_base, third_base",
                    "turn, sequence"]

        values = {"batter_id":batter.getId(),
                    "side": int(batter.getBatSide() == pitcher.getThrowSide()),
                    "balls": scoreKeeper.getBalls(),
                    "strikes": scoreKeeper.getStrikes(),
                    "turn": scoreKeeper.getTurn(batter),
                    "sequence": scoreKeeper.getSequence(),
                    "pitch_velocity-gtn": pitch[1]-2,
                    "pitch_velocity-ltn": pitch[1]+2,
                    "box": pitch[2],
                    "pitch_type_id": pitch[0]}
        for base in ("first_base", "second_base", "third_base"):
            values[base] = int(base in diamondState.split("_"))

        gdCmd = batter.getGDCmd()
        mainCmd = pitchContactCmd
        return self.dungeonMaster.getRandomItem(mainCmd, itemCmd, gdCmd, argList, values)[0]


    def getPitcherContact(self, pitcher, batter, pitch):
        itemCmd = "hit_style, hit_hardness, hit_angle, hit_distance"

        argList = ["pitch_result_id", "pitcher_id", "side", "pitch_type_id",
                    "pitch_velocity-gtn, pitch_velocity-ltn", "box"]

        values = {"pitcher_id":pitcher.getId(),
                    "side": int(batter.getBatSide() == pitcher.getThrowSide()),
                    "pitch_velocity-gtn": pitch[1]-2,
                    "pitch_velocity-ltn": pitch[1]+2,
                    "box": pitch[2],
                    "pitch_type_id": pitch[0],
                    "pitch_result_id": 10}

        gdCmd = pitcher.getGDCmd()
        mainCmd = pitchContactCmd
        return self.dungeonMaster.getRandomItem(mainCmd, itemCmd, gdCmd, argList, values)


    def getBatterContact(self, pitcher, batter, pitch):
        itemCmd = "hit_style, hit_hardness, hit_angle, hit_distance"

        argList = ["pitch_result_id", "batter_id", "side", "pitch_type_id",
                    "pitch_velocity-gtn, pitch_velocity-ltn", "box"]

        values = {"batter_id":batter.getId(),
                    "side": int(batter.getBatSide() == pitcher.getThrowSide()),
                    "pitch_velocity-gtn": pitch[1]-2,
                    "pitch_velocity-ltn": pitch[1]+2,
                    "box": pitch[2],
                    "pitch_type_id": pitch[0],
                    "pitch_result_id":10}

        gdCmd = pitcher.getGDCmd()
        mainCmd = pitchContactCmd
        return self.dungeonMaster.getRandomItem(mainCmd, itemCmd, gdCmd, argList, values)



    def getContactResult(self, pitcherContact, batterContact, scoreKeeper):
        contact = random.choice((pitcherContact,batterContact))
        argList = ["team_id", "hit_style", "hit_hardness", "hit_angle-gtn, hit_angle-ltn",
                    "hit_distance-gtn, hit_distance-ltn"]
        values = {"team_id":scoreKeeper.getFieldingTeam(),
                    "hit_style": contact[0],
                    "hit_hardness": contact[1],
                    "hit_angle-gtn": contact[2]-2,
                    "hit_angle-ltn": contact[2]+2,
                    "hit_distance-gtn": contact[3]-20,
                    "hit_distance-ltn": contact[3]+20,}

        mainCmd = abResultCmd
        return self.dungeonMaster.getRandomItem(mainCmd, None, None, argList, values)


################################################################################
################################################################################


class ProbableOutcome(OutcomeType):

    def __init__(self, dungeonMaster):
        super().__init__(dungeonMaster)


    def getPitch(self, pitcher, batter, scoreKeeper, diamondState):
        pitchType = self.getPitchType(pitcher, batter, scoreKeeper, diamondState)
        pitchVelocity = self.getPitchVelocity(pitcher, batter, scoreKeeper, diamondState, pitchType)
        pitchLocation = self.getPitchLocation(pitcher, batter, scoreKeeper, diamondState, pitchType)
        pitchResult = self.getPitchResult(pitcher, batter, scoreKeeper, diamondState, pitchType, pitchVelocity, pitchLocation)
        return (pitchType, pitchVelocity, pitchLocation, pitchResult)


    def getPitchType(self, pitcher, batter, scoreKeeper, diamondState):
        itemCmd = "pitch_type_id"
        argList = ["pitcher_id", "side", "balls, strikes",
                    "first_base, second_base, third_base", "turn, sequence"]

        values = {"pitcher_id":pitcher.getId(),
                    "side": int(batter.getBatSide() == pitcher.getThrowSide()),
                    "balls": scoreKeeper.getBalls(),
                    "strikes": scoreKeeper.getStrikes(),
                    "turn": scoreKeeper.getTurn(batter),
                    "sequence": scoreKeeper.getSequence()}
        for base in ("first_base", "second_base", "third_base"):
            values[base] = int(base in diamondState.split("_"))

        gdCmd = pitcher.getGDCmd()
        mainCmd = probPitchContactCmd
        return self.dungeonMaster.getItem(mainCmd, itemCmd, gdCmd, argList, values)


    def getPitchLocation(self, pitcher, batter, scoreKeeper, diamondState, pitchType):
        itemCmd = "box"
        argList = ["pitcher_id", "side", "pitch_type_id", "balls, strikes",
                    "first_base, second_base, third_base", "turn, sequence"]

        values = {"pitcher_id":pitcher.getId(),
                    "side": int(batter.getBatSide() == pitcher.getThrowSide()),
                    "pitch_type_id": pitchType,
                    "balls": scoreKeeper.getBalls(),
                    "strikes": scoreKeeper.getStrikes(),
                    "turn": scoreKeeper.getTurn(batter),
                    "sequence": scoreKeeper.getSequence()}
        for base in ("first_base", "second_base", "third_base"):
            values[base] = int(base in diamondState.split("_"))

        gdCmd = pitcher.getGDCmd()
        mainCmd = probPitchContactCmd
        return self.dungeonMaster.getItem(mainCmd, itemCmd, gdCmd, argList, values)


    def getPitchVelocity(self, pitcher, batter, scoreKeeper, diamondState, pitchType):
        itemCmd = "pitch_velocity"
        argList = ["pitcher_id", "side", "pitch_type_id", "balls, strikes",
                    "first_base, second_base, third_base", "turn, sequence"]

        values = {"pitcher_id":pitcher.getId(),
                    "side": int(batter.getBatSide() == pitcher.getThrowSide()),
                    "pitch_type_id": pitchType,
                    "balls": scoreKeeper.getBalls(),
                    "strikes": scoreKeeper.getStrikes(),
                    "turn": scoreKeeper.getTurn(batter),
                    "sequence": scoreKeeper.getSequence()}
        for base in ("first_base", "second_base", "third_base"):
            values[base] = int(base in diamondState.split("_"))

        gdCmd = pitcher.getGDCmd()
        mainCmd = probPitchContactCmd
        return self.dungeonMaster.getItem(mainCmd, itemCmd, gdCmd, argList, values)


    def getPitchResult(self, pitcher, batter, scoreKeeper, diamondState, pitchType, pitchVelocity, pitchLocation):
        itemCmd = "pitch_result_id"
        argList = ["pitcher_id", "side", "pitch_type_id", "box", "pitch_velocity", "balls, strikes",
                    "first_base, second_base, third_base", "turn, sequence"]

        values = {"pitcher_id":pitcher.getId(),
                    "side": int(batter.getBatSide() == pitcher.getThrowSide()),
                    "pitch_type_id": pitchType,
                    "box": pitchLocation,
                    "pitch_velocity": pitchVelocity,
                    "balls": scoreKeeper.getBalls(),
                    "strikes": scoreKeeper.getStrikes(),
                    "turn": scoreKeeper.getTurn(batter),
                    "sequence": scoreKeeper.getSequence()}
        for base in ("first_base", "second_base", "third_base"):
            values[base] = int(base in diamondState.split("_"))

        gdCmd = pitcher.getGDCmd()
        mainCmd = probPitchContactCmd
        return self.dungeonMaster.getItem(mainCmd, itemCmd, gdCmd, argList, values)



    def getSwing(self, pitcher, batter, pitch, scoreKeeper, diamondState):
        itemCmd = "pitch_result_id"

        argList = ["batter_id", "side", "pitch_type_id", "pitch_velocity-gtn, pitch_velocity-ltn",
                    "box", "strikes, balls", "first_base, second_base, third_base",
                    "turn, sequence"]

        values = {"batter_id":batter.getId(),
                    "side": int(batter.getBatSide() == pitcher.getThrowSide()),
                    "balls": scoreKeeper.getBalls(),
                    "strikes": scoreKeeper.getStrikes(),
                    "turn": scoreKeeper.getTurn(batter),
                    "sequence": scoreKeeper.getSequence(),
                    "pitch_velocity-gtn": pitch[1]-2,
                    "pitch_velocity-ltn": pitch[1]+2,
                    "box": pitch[2],
                    "pitch_type_id": pitch[0]}
        for base in ("first_base", "second_base", "third_base"):
            values[base] = int(base in diamondState.split("_"))

        gdCmd = batter.getGDCmd()
        mainCmd = pitchContactCmd
        return self.dungeonMaster.getItem(mainCmd, itemCmd, gdCmd, argList, values)


    def getHitItem(self, pitcher, batter, pitch, itemCmd, isPitcher=False):
        player = pitcher if isPitcher else batter
        playerId = "pitcher_id" if isPitcher else "batter_id"
        argList = ["pitch_result_id", playerId, "side", "pitch_type_id",
                    "pitch_velocity-gtn, pitch_velocity-ltn", "box"]

        values = {playerId:player.getId(),
                    "side": int(batter.getBatSide() == pitcher.getThrowSide()),
                    "pitch_velocity-gtn": pitch[1]-2,
                    "pitch_velocity-ltn": pitch[1]+2,
                    "box": pitch[2],
                    "pitch_type_id": pitch[0],
                    "pitch_result_id":10}

        gdCmd = player.getGDCmd()
        mainCmd = probPitchContactCmd
        return self.dungeonMaster.getItem(mainCmd, itemCmd, gdCmd, argList, values)


    def getPitcherContact(self, pitcher, batter, pitch):
        hitStyle = self.getHitItem(pitcher, batter, pitch, "hit_style", True)
        hitHardness = self.getHitItem(pitcher, batter, pitch, "hit_hardness", True)
        hitAngle = self.getHitItem(pitcher, batter, pitch, "hit_angle", True)
        hitDistance = self.getHitItem(pitcher, batter, pitch, "hit_distance", True)
        return (hitStyle, hitHardness, hitAngle, hitDistance)


    def getBatterContact(self, pitcher, batter, pitch):
        hitStyle = self.getHitItem(pitcher, batter, pitch, "hit_style")
        hitHardness = self.getHitItem(pitcher, batter, pitch, "hit_hardness")
        hitAngle = self.getHitItem(pitcher, batter, pitch, "hit_angle")
        hitDistance = self.getHitItem(pitcher, batter, pitch, "hit_distance")
        print(hitStyle, hitHardness, hitAngle, hitDistance)
        raise AssertionError
        return (hitStyle, hitHardness, hitAngle, hitDistance)


    def getContactResult(self, pitcher, batter, pitch, scoreKeeper):
        pass


################################################################################
################################################################################


class DungeonMaster:

    def __init__(self, db, outcome):
        self.db = db
        self.outcomeType = self.setOutcome(outcome)


    def getItemValues(self, mainCmd, itemCmd, gdCmd, argList, values, attempt):
        argList = argList if not attempt else argList[:attempt]
        args = []
        for arg in argList:
            for item in arg.split(","):
                args.append(values[item.strip()])
        cmd = mainCmd.format({"itemCmd":itemCmd, "gdCmd": gdCmd, "whereCmd": whereFunc(argList)})
        return cmd, args


    def getRandomItem(self, mainCmd, itemCmd, gdCmd, argList, values, attempt=0):
        cmd, args = self.getItemValues(mainCmd, itemCmd, gdCmd, argList, values, attempt)
        try:
            result = self.getRandomResult(cmd, args)
        except IndexError:
            result = self.getRandomItem(mainCmd, itemCmd, gdCmd, argList, values, attempt-1)
        return result


    def getItem(self, mainCmd, itemCmd, gdCmd, argList, values, attempt=0):
       cmd, args = self.getItemValues(mainCmd, itemCmd, gdCmd, argList, values, attempt)
       print(cmd)
       print(args)
       print()
       try:
           result = self.getResult(cmd, args)[0]
       except (IndexError, TypeError):
           result = self.getItem(mainCmd, itemCmd, gdCmd, argList, values, attempt-1)
       return result


    def setOutcome(self, outcome):
        outcomeType = None
        if outcome == "Random":
            outcomeType = RandomOutcome(self)
        if outcome == "Probable":
            outcomeType = ProbableOutcome(self)
        return outcomeType


    def getPitchResult(self, pitch, swing):
        return random.choice((pitch, swing))



    def getRandomResult(self, cmd, args):
        #pprint(cmd)
        results = self.db.fetchAll(cmd, args)
        answer = random.choice(results)
        return answer


    def getResult(self, cmd, args):
        return self.db.fetchOne(cmd, args)


    def getPitch(self, pitcher, batter, scoreKeeper, diamondState):
        return self.outcomeType.getPitch(pitcher, batter, scoreKeeper, diamondState)


    def getSwing(self, pitcher, batter, pitch, scoreKeeper, diamondState):
        return self.outcomeType.getSwing(pitcher, batter, pitch, scoreKeeper, diamondState)


    def getPitcherContact(self, pitcher, batter, pitch):
        return self.outcomeType.getPitcherContact(pitcher, batter, pitch)


    def getBatterContact(self, pitcher, batter, pitch):
        return self.outcomeType.getBatterContact(pitcher, batter, pitch)


    def getContactResult(self, pitcherContact, batterContact, scoreKeeper):
        return self.outcomeType.getContactResult(pitcherContact, batterContact, scoreKeeper)
