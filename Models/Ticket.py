from abc import ABCMeta, abstractmethod

################################################################################
################################################################################





################################################################################
################################################################################


class Ticket(metaclass=ABCMeta):

    def __init__(self, diamond, umpire):

        self.diamond = diamond
        self.umpire = umpire


    @abstractmethod
    def generateTicket(self, * , pitcher, batter):
        pass


################################################################################
################################################################################


class Out(Ticket):

    def __init__(self, diamond, umpire):
        super().__init__(diamond, umpire)


    def generateTicket(self, * , pitcher, batter):
        self.umpire.recordOut()
        self.umpire.scoreKeeper.pitcherOut(pitcher)
        self.umpire.scoreKeeper.batterAB(batter)



################################################################################
################################################################################


class Single(Ticket):

    def __init__(self, diamond, umpire):
        super().__init__(diamond, umpire)


    def generateTicket(self, * , pitcher, batter):
        if self.diamond.getBase("third"):
            self.umpire.recordRun()
            runner = self.diamond.getBase("third")
            self.umpire.scoreKeeper.batterR(runner)
            self.umpire.scoreKeeper.batterRBI(batter)
            self.umpire.scoreKeeper.pitcherR(pitcher)
            self.diamond.moveBase("third")

        if self.diamond.getBase("second"):
            self.diamond.moveBase("second", "third")

        if self.diamond.getBase("first"):
            self.diamond.moveBase("first", "second")

        self.diamond.setBase("first", batter)

        self.umpire.scoreKeeper.pitcherH(pitcher)
        self.umpire.scoreKeeper.batterH(batter)


################################################################################
################################################################################


class Double(Ticket):

    def __init__(self, diamond, umpire):
        super().__init__(diamond, umpire)


    def generateTicket(self, * , pitcher, batter):
        if self.diamond.getBase("third"):
            self.umpire.recordRun()
            runner = self.diamond.getBase("third")
            self.umpire.scoreKeeper.batterR(runner)
            self.umpire.scoreKeeper.batterRBI(batter)
            self.umpire.scoreKeeper.pitcherR(pitcher)
            self.diamond.moveBase("third")

        if self.diamond.getBase("second"):
            self.umpire.recordRun()
            runner = self.diamond.getBase("second")
            self.umpire.scoreKeeper.batterR(runner)
            self.umpire.scoreKeeper.batterRBI(batter)
            self.umpire.scoreKeeper.pitcherR(pitcher)
            self.diamond.moveBase("second")


        if self.diamond.getBase("first"):
            self.diamond.moveBase("first", "third")

        self.diamond.setBase("second", batter)

        self.umpire.scoreKeeper.pitcherH(pitcher)
        self.umpire.scoreKeeper.batter2B(batter)


################################################################################
################################################################################


class Triple(Ticket):

    def __init__(self, diamond, umpire):
        super().__init__(diamond, umpire)


    def generateTicket(self, * , pitcher, batter):
        if self.diamond.getBase("third"):
            self.umpire.recordRun()
            runner = self.diamond.getBase("third")
            self.umpire.scoreKeeper.batterR(runner)
            self.umpire.scoreKeeper.batterRBI(batter)
            self.umpire.scoreKeeper.pitcherR(pitcher)
            self.diamond.moveBase("third")

        if self.diamond.getBase("second"):
            self.umpire.recordRun()
            runner = self.diamond.getBase("second")
            self.umpire.scoreKeeper.batterR(runner)
            self.umpire.scoreKeeper.batterRBI(batter)
            self.umpire.scoreKeeper.pitcherR(pitcher)
            self.diamond.moveBase("second")


        if self.diamond.getBase("first"):
            runner = self.diamond.getBase("first")
            self.umpire.scoreKeeper.batterR(runner)
            self.umpire.scoreKeeper.batterRBI(batter)
            self.umpire.scoreKeeper.pitcherR(pitcher)
            self.diamond.moveBase("first")

        self.diamond.setBase("third", batter)

        self.umpire.scoreKeeper.pitcherH(pitcher)
        self.umpire.scoreKeeper.batter3B(batter)





################################################################################
################################################################################


class HomeRun(Ticket):

    def __init__(self, diamond, umpire):
        super().__init__(diamond, umpire)


    def generateTicket(self, * , pitcher, batter):
        if self.diamond.getBase("third"):
            self.umpire.recordRun()
            runner = self.diamond.getBase("third")
            self.umpire.scoreKeeper.batterR(runner)
            self.umpire.scoreKeeper.batterRBI(batter)
            self.umpire.scoreKeeper.pitcherR(pitcher)
            self.diamond.moveBase("third")

        if self.diamond.getBase("second"):
            self.umpire.recordRun()
            runner = self.diamond.getBase("second")
            self.umpire.scoreKeeper.batterR(runner)
            self.umpire.scoreKeeper.batterRBI(batter)
            self.umpire.scoreKeeper.pitcherR(pitcher)
            self.diamond.moveBase("second")


        if self.diamond.getBase("first"):
            self.umpire.recordRun()
            runner = self.diamond.getBase("first")
            self.umpire.scoreKeeper.batterR(runner)
            self.umpire.scoreKeeper.batterRBI(batter)
            self.umpire.scoreKeeper.pitcherR(pitcher)
            self.diamond.moveBase("first")

        self.umpire.recordRun()
        self.umpire.scoreKeeper.pitcherH(pitcher)
        self.umpire.scoreKeeper.pitcherR(pitcher)

        self.umpire.scoreKeeper.batterHR(batter)


################################################################################
################################################################################


class DoublePlay(Ticket):

    def __init__(self, diamond, umpire):
        super().__init__(diamond, umpire)


    def generateTicket(self, * , pitcher, batter):

        if self.diamond.getBase("third"):
            self.umpire.recordOut()
            self.umpire.scoreKeeper.pitcherOut(pitcher)
            self.diamond.moveBase("third")

        elif self.diamond.getBase("second"):
            self.umpire.recordOut()
            self.umpire.scoreKeeper.pitcherOut(pitcher)
            self.diamond.moveBase("second")


        elif self.diamond.getBase("first"):
            self.umpire.recordOut()
            self.umpire.scoreKeeper.pitcherOut(pitcher)
            self.diamond.moveBase("first")


        self.umpire.recordOut()
        self.umpire.scoreKeeper.pitcherOut(pitcher)
        self.umpire.scoreKeeper.batterAB(batter)


################################################################################
################################################################################


class Walk(Ticket):

    def __init__(self, diamond, umpire):
        super().__init__(diamond, umpire)


    def generateTicket(self, * , pitcher, batter):

        if self.diamond.getBasesLoaded():
            self.umpire.recordRun()
            runner = self.diamond.getBase("third")
            self.umpire.scoreKeeper.batterR(runner)
            self.umpire.scoreKeeper.batterRBI(batter)
            self.umpire.scoreKeeper.pitcherR(pitcher)
            self.diamond.moveBase("third")

        elif self.diamond.getBase("second") and self.diamond.getBase("first"):
            self.diamond.moveBase("second","third")
            self.diamond.moveBase("first", "second")

        elif self.diamond.getBase("first"):
            self.diamond.moveBase("first", "second")

        self.diamond.setBase("first", batter)

        self.umpire.scoreKeeper.pitcherBB(pitcher)
        self.umpire.scoreKeeper.batterBB(batter)


################################################################################
################################################################################


class StrikeOut(Ticket):

    def __init__(self, diamond, umpire):
        super().__init__(diamond, umpire)


    def generateTicket(self, * , pitcher, batter):
        self.umpire.recordOut()
        self.umpire.scoreKeeper.pitcherK(pitcher)
        self.umpire.scoreKeeper.batterAB(batter)


################################################################################
################################################################################
