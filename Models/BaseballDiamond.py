
################################################################################
################################################################################





################################################################################
################################################################################


class BaseballDiamond:

    def __init__(self):

        self.firstBase = None
        self.secondBase = None
        self.thirdBase = None


    def getBase(self, base):
        return {"first":self.firstBase, "second":self.secondBase, "third":self.thirdBase}[base]


    def getBasesLoaded(self):
        return True if self.firstBase and self.secondBase and self.thirdBase else False


    def getBasesEmpty(self):
        return True if not self.firstBase and not self.secondBase and not self.thirdBase else False


    def setBase(self, base, playerId):
        if base == "first":
            self.firstBase = playerId
        elif base == "second":
            self.secondBase = playerId
        else:
            self.thirdBase = playerId


    def clearBase(self, base):
        if base == "first":
            self.firstBase = None
        elif base == "second":
            self.secondBase = None
        else:
            self.thirdBase = None



    def moveBase(self, base1, base2=None):
        startBase = {"first":self.firstBase, "second":self.secondBase, "third":self.thirdBase}[base1]
        playerId = startBase
        self.clearBase(base1)

        if base2:
            self.setBase(base2, playerId)


    def clearBases(self):
        self.firstBase = None
        self.secondBase = None
        self.thirdBase = None
