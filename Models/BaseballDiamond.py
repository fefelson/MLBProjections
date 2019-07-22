
################################################################################
################################################################################


emptyBase = (-10,-20)


################################################################################
################################################################################


class BaseFullError(Exception):
    pass


################################################################################
################################################################################


class BaseballDiamond:

    def __init__(self):

        self.firstBase = emptyBase
        self.secondBase = emptyBase
        self.thirdBase = emptyBase

        self.onBase = {}


    def clearBases(self):
        self.firstBase = emptyBase
        self.secondBase = emptyBase
        self.thirdBase = emptyBase
        self.onBase.clear()


    def moveBase(self, base1, base2):
        values = self.popBase(base1)
        self.reachedBase(base2, *values)


    def reachedBase(self, base, playerId, onHook=-20):
        value = getattr(self, base)
        if value != emptyBase:
            # print(self.firstBase, self.secondBase, self.thirdBase)
            # print()
            raise BaseFullError("Already a player on this base")

        setattr(self, base, (playerId, onHook))
        self.onBase[playerId] = {"base":base, "playerId":playerId, "onHook":onHook}


    def popPlayer(self, playerId):
        player = self.onBase[playerId]
        setattr(self, player["base"], emptyBase)
        return player["onHook"]


    def checkPlayer(self, playerId):
        return self.onBase.get(playerId, None)


    def popBase(self, base):
        value = getattr(self, base)
        setattr(self, base, emptyBase)
        return value


    def whoOnBase(self):
        return (self.firstBase[0], self.secondBase[0], self.thirdBase[0])


    def getBase(self, base):
        return getattr(self, base)


    def getDiamondState(self):
        return "_".join([base for base in ("firstBase", "secondBase", "thirdBase") if getattr(self, base) != emptyBase])


    def setBase(self, base, playerId):
        pass
        # if base == "first":
        #     self.firstBase = playerId
        # elif base == "second":
        #     self.secondBase = playerId
        # else:
        #     self.thirdBase = playerId


    def clearBase(self, base):
        pass
        # if base == "first":
        #     self.firstBase = None
        # elif base == "second":
        #     self.secondBase = None
        # else:
        #     self.thirdBase = None
