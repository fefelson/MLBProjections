
################################################################################
################################################################################





################################################################################
################################################################################


class BaseFullError(Exception):
    pass


################################################################################
################################################################################


class BaseballDiamond:

    def __init__(self):

        self.firstBase = (-10, -20)
        self.secondBase = (-10, -20)
        self.thirdBase = (-10, -20)

        self.onBase = {}


    def clearBases(self):
        self.firstBase = (-10, -20)
        self.secondBase = (-10, -20)
        self.thirdBase = (-10, -20)

        self.onBase.clear()


    def reachedBase(self, base, playerId, onHook=-20):
        value = getattr(self, base)
        if value[0] != -10:
            # print(self.firstBase, self.secondBase, self.thirdBase)
            # print()
            raise BaseFullError("Already a player on this base")

        setattr(self, base, (playerId, onHook))
        self.onBase[playerId] = {"base":base, "playerId":playerId, "onHook":onHook}


    def popPlayer(self, playerId):
        player = self.onBase[playerId]
        setattr(self, player["base"], (-10, -20))
        return player["onHook"]


    def checkPlayer(self, playerId):
        return self.onBase.get(playerId, None)


    def popBase(self, base):
        value = getattr(self, base)
        setattr(self, base, (-10, -20))
        return value


    def whoOnBase(self):
        return (self.firstBase[0], self.secondBase[0], self.thirdBase[0])


    def getBase(self, base):
        return getattr(self, base)


    def getBasesLoaded(self):
        pass
        # return True if self.firstBase and self.secondBase and self.thirdBase else False


    def getBasesEmpty(self):
        pass
        # return True if not self.firstBase and not self.secondBase and not self.thirdBase else False


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



    def moveBase(self, base1, base2=None):
        pass
        # startBase = {"first":self.firstBase, "second":self.secondBase, "third":self.thirdBase}[base1]
        # playerId = startBase
        # self.clearBase(base1)
        #
        # if base2:
        #     self.setBase(base2, playerId)
