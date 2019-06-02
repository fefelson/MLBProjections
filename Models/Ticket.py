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


class Pitch(Ticket):

    _data = {   "game_id": -1,
                "play_num": -1,
                "pitcher_id": -1,
                "batter_id": -1,
                "pitch_num": -1,
                "location_id": -1,
                "count_id": -1,
                "diamond_id": -1
            }

    def __init__(self, diamond, umpire):
        super().__init__(diamond, umpire)


    def generateTicket(self, info):

        data = Pitch._data.copy()
        data


        pitchTicket = {"sql":getSql("pitch")}

        self.umpire.recordOut()
        self.umpire.scoreKeeper.pitcherOut(pitcher)
        self.umpire.scoreKeeper.batterAB(batter)


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


class Hit(Ticket):

    def __init__(self, diamond, umpire):
        super().__init__(diamond, umpire)


    def generateTicket(self, * , pitcher, batter):
        self.umpire.scoreKeeper.pitcherH(pitcher)
        self.umpire.scoreKeeper.batterH(batter)


################################################################################
################################################################################


class GroundOut(Out):

    def __init__(self, diamond, umpire):
        super().__init__(diamond, umpire)


    def generateTicket(self, * , pitcher, batter):
        super().generateTicket(pitcher=pitcher, batter=batter)

        if self.umpire.getOuts() < 3 and not self.diamond.getBasesEmpty():


            # State Pattern desired
            # Bases Loaded
            if self.diamond.getBasesLoaded():

                # Player out at home
                self.diamond.moveBase("third")
                # Player at second moves to third
                self.diamond.moveBase("second", "third")
                # Player at first moves to second
                self.diamond.moveBase("first", "second")
                # Batter reaches first
                self.diamond.setBase("first", batter)

            # ThirdBase and SecondBase
            elif self.diamond.getBase("third") and self.diamond.getBase("second"):

                # Player at third scores
                player = self.diamond.getBase("third")
                self.umpire.recordRun()
                self.umpire.scoreKeeper.batterR(player)
                self.umpire.scoreKeeper.batterRBI(batter)
                self.umpire.scoreKeeper.pitcherR(pitcher)
                self.diamond.moveBase("third")
                ##############################
                # Player as second moves to third
                self.diamond.moveBase("second", "third")

            # ThirdBase and FirstBase
            elif self.diamond.getBase("third") and self.diamond.getBase("first"):

                # Player at third scores
                player = self.diamond.getBase("third")
                self.umpire.recordRun()
                self.umpire.scoreKeeper.batterR(player)
                self.umpire.scoreKeeper.batterRBI(batter)
                self.umpire.scoreKeeper.pitcherR(pitcher)
                self.diamond.moveBase("third")
                ##############################
                # Player out going from first to second
                self.diamond.moveBase("first")
                # Batter reaches first
                self.diamond.setBase("first", batter)

            # SecondBase and FirstBase
            elif self.diamond.getBase("second") and self.diamond.getBase("first"):

                # Player out going from second to third
                self.diamond.moveBase("second")
                # Player moves from first to second
                self.diamond.moveBase("first", "second")
                # Batter reaches first
                self.diamond.setBase("first", batter)

            # ThirdBase
            elif self.diamond.getBase("third"):

                # Player at third scores
                player = self.diamond.getBase("third")
                self.umpire.recordRun()
                self.umpire.scoreKeeper.batterR(player)
                self.umpire.scoreKeeper.batterRBI(batter)
                self.umpire.scoreKeeper.pitcherR(pitcher)
                self.diamond.moveBase("third")
                ##############################

            # SecondBase
            elif self.diamond.getBase("second"):
                # Player as second moves to third
                self.diamond.moveBase("second", "third")

            # FirstBase
            elif self.diamond.getBase("first"):
                # Player out going from first to second
                self.diamond.moveBase("first")
                # Batter reaches first
                self.diamond.setBase("first", batter)


################################################################################
################################################################################


class FlyOut(Out):

    def __init__(self, diamond, umpire):
        super().__init__(diamond, umpire)


    def generateTicket(self, * , pitcher, batter):
        super().generateTicket(pitcher=pitcher, batter=batter)

        if self.umpire.getOuts() < 3 and not self.diamond.getBasesEmpty():


            # State Pattern desired
            # Bases Loaded
            if self.diamond.getBasesLoaded():

                # Player at third scores
                player = self.diamond.getBase("third")
                self.umpire.recordRun()
                self.umpire.scoreKeeper.batterR(player)
                self.umpire.scoreKeeper.batterRBI(batter)
                self.umpire.scoreKeeper.pitcherR(pitcher)
                self.diamond.moveBase("third")
                ##############################
                # Player as second moves to third
                self.diamond.moveBase("second", "third")


            # ThirdBase and SecondBase
            elif self.diamond.getBase("third") and self.diamond.getBase("second"):

                # Player at third scores
                player = self.diamond.getBase("third")
                self.umpire.recordRun()
                self.umpire.scoreKeeper.batterR(player)
                self.umpire.scoreKeeper.batterRBI(batter)
                self.umpire.scoreKeeper.pitcherR(pitcher)
                self.diamond.moveBase("third")
                ##############################
                # Player as second moves to third
                self.diamond.moveBase("second", "third")

            # ThirdBase and FirstBase
            elif self.diamond.getBase("third") and self.diamond.getBase("first"):
                # Player at third scores
                player = self.diamond.getBase("third")
                self.umpire.recordRun()
                self.umpire.scoreKeeper.batterR(player)
                self.umpire.scoreKeeper.batterRBI(batter)
                self.umpire.scoreKeeper.pitcherR(pitcher)
                self.diamond.moveBase("third")
                ##############################


            # SecondBase and FirstBase
            elif self.diamond.getBase("second") and self.diamond.getBase("first"):

                # Player as second moves to third
                self.diamond.moveBase("second", "third")


            # ThirdBase
            elif self.diamond.getBase("third"):

                # Player at third scores
                player = self.diamond.getBase("third")
                self.umpire.recordRun()
                self.umpire.scoreKeeper.batterR(player)
                self.umpire.scoreKeeper.batterRBI(batter)
                self.umpire.scoreKeeper.pitcherR(pitcher)
                self.diamond.moveBase("third")
                ##############################


            # SecondBase
            elif self.diamond.getBase("second"):

                # Player as second moves to third
                self.diamond.moveBase("second", "third")


            # FirstBase
            elif self.diamond.getBase("first"):
                pass


################################################################################
################################################################################


class LineOut(Out):

    def __init__(self, diamond, umpire):
        super().__init__(diamond, umpire)


    def generateTicket(self, * , pitcher, batter):
        super().generateTicket(pitcher=pitcher, batter=batter)

        if self.umpire.getOuts() < 3 and not self.diamond.getBasesEmpty():


            # State Pattern desired
            # Bases Loaded
            if self.diamond.getBasesLoaded():
                pass

            # ThirdBase and SecondBase
            elif self.diamond.getBase("third") and self.diamond.getBase("second"):
                pass

            # ThirdBase and FirstBase
            elif self.diamond.getBase("third") and self.diamond.getBase("first"):
                pass

            # SecondBase and FirstBase
            elif self.diamond.getBase("second") and self.diamond.getBase("first"):
                pass

            # ThirdBase
            elif self.diamond.getBase("third"):
                pass

            # SecondBase
            elif self.diamond.getBase("second"):
                pass

            # FirstBase
            elif self.diamond.getBase("first"):
                pass


################################################################################
################################################################################


class PopOut(Out):

    def __init__(self, diamond, umpire):
        super().__init__(diamond, umpire)


    def generateTicket(self, * , pitcher, batter):
        super().generateTicket(pitcher=pitcher, batter=batter)

        if self.umpire.getOuts() < 3 and not self.diamond.getBasesEmpty():


            # State Pattern desired
            # Bases Loaded
            if self.diamond.getBasesLoaded():
                pass

            # ThirdBase and SecondBase
            elif self.diamond.getBase("third") and self.diamond.getBase("second"):
                pass

            # ThirdBase and FirstBase
            elif self.diamond.getBase("third") and self.diamond.getBase("first"):
                pass

            # SecondBase and FirstBase
            elif self.diamond.getBase("second") and self.diamond.getBase("first"):
                pass

            # ThirdBase
            elif self.diamond.getBase("third"):
                pass

            # SecondBase
            elif self.diamond.getBase("second"):
                pass

            # FirstBase
            elif self.diamond.getBase("first"):
                pass


################################################################################
################################################################################


class FielderChoice(GroundOut):

    def __init__(self, diamond, umpire):
        super().__init__(diamond, umpire)


    def generateTicket(self, * , pitcher, batter):
        super().generateTicket(pitcher=pitcher, batter=batter)



################################################################################
################################################################################


class FoulOut(Out):

    def __init__(self, diamond, umpire):
        super().__init__(diamond, umpire)


    def generateTicket(self, * , pitcher, batter):
        super().generateTicket(pitcher=pitcher, batter=batter)



################################################################################
################################################################################


class Single(Hit):

    def __init__(self, diamond, umpire):
        super().__init__(diamond, umpire)


    def generateTicket(self, * , pitcher, batter):
        super().generateTicket(pitcher=pitcher, batter=batter)

        if self.diamond.getBase("third"):
            # Player at third scores
            player = self.diamond.getBase("third")
            self.umpire.recordRun()
            self.umpire.scoreKeeper.batterR(player)
            self.umpire.scoreKeeper.batterRBI(batter)
            self.umpire.scoreKeeper.pitcherR(pitcher)
            self.diamond.moveBase("third")
            ##############################

        # SecondBase
        elif self.diamond.getBase("second"):
            # Player at third scores
            player = self.diamond.getBase("second")
            self.umpire.recordRun()
            self.umpire.scoreKeeper.batterR(player)
            self.umpire.scoreKeeper.batterRBI(batter)
            self.umpire.scoreKeeper.pitcherR(pitcher)
            self.diamond.moveBase("second")
            ##############################

        # FirstBase
        elif self.diamond.getBase("first"):

            # Player at first moves to second
            self.diamond.moveBase("first", "second")

        self.diamond.setBase("first", batter)


################################################################################
################################################################################


class Double(Ticket):

    def __init__(self, diamond, umpire):
        super().__init__(diamond, umpire)


    def generateTicket(self, * , pitcher, batter):
        super().generateTicket(pitcher=pitcher, batter=batter)
        self.umpire.scoreKeeper.batter2B(batter)

        if self.diamond.getBase("third"):
            # Player at third scores
            player = self.diamond.getBase("third")
            self.umpire.recordRun()
            self.umpire.scoreKeeper.batterR(player)
            self.umpire.scoreKeeper.batterRBI(batter)
            self.umpire.scoreKeeper.pitcherR(pitcher)
            self.diamond.moveBase("third")
            ##############################

        # SecondBase
        elif self.diamond.getBase("second"):
            # Player at third scores
            player = self.diamond.getBase("second")
            self.umpire.recordRun()
            self.umpire.scoreKeeper.batterR(player)
            self.umpire.scoreKeeper.batterRBI(batter)
            self.umpire.scoreKeeper.pitcherR(pitcher)
            self.diamond.moveBase("second")
            ##############################

        # FirstBase
        elif self.diamond.getBase("first"):

            # Player at first moves to second
            self.diamond.moveBase("first", "third")

        self.diamond.setBase("second", batter)




################################################################################
################################################################################


class Triple(Ticket):

    def __init__(self, diamond, umpire):
        super().__init__(diamond, umpire)


    def generateTicket(self, * , pitcher, batter):
        super().generateTicket(pitcher=pitcher, batter=batter)
        self.umpire.scoreKeeper.batter3B(batter)

        if self.diamond.getBase("third"):
            # Player at third scores
            player = self.diamond.getBase("third")
            self.umpire.recordRun()
            self.umpire.scoreKeeper.batterR(player)
            self.umpire.scoreKeeper.batterRBI(batter)
            self.umpire.scoreKeeper.pitcherR(pitcher)
            self.diamond.moveBase("third")
            ##############################

        # SecondBase
        elif self.diamond.getBase("second"):
            # Player at second scores
            player = self.diamond.getBase("second")
            self.umpire.recordRun()
            self.umpire.scoreKeeper.batterR(player)
            self.umpire.scoreKeeper.batterRBI(batter)
            self.umpire.scoreKeeper.pitcherR(pitcher)
            self.diamond.moveBase("second")
            ##############################

        # FirstBase
        elif self.diamond.getBase("first"):

            # Player at second scores
            player = self.diamond.getBase("first")
            self.umpire.recordRun()
            self.umpire.scoreKeeper.batterR(player)
            self.umpire.scoreKeeper.batterRBI(batter)
            self.umpire.scoreKeeper.pitcherR(pitcher)
            self.diamond.moveBase("first")

        self.diamond.setBase("third", batter)





################################################################################
################################################################################


class HomeRun(Ticket):

    def __init__(self, diamond, umpire):
        super().__init__(diamond, umpire)


    def generateTicket(self, * , pitcher, batter):
        super().generateTicket(pitcher=pitcher, batter=batter)
        self.umpire.recordRun()
        self.umpire.scoreKeeper.batterHR(batter)
        self.umpire.scoreKeeper.pitcherR(pitcher)

        if self.diamond.getBase("third"):
            # Player at third scores
            player = self.diamond.getBase("third")
            self.umpire.recordRun()
            self.umpire.scoreKeeper.batterR(player)
            self.umpire.scoreKeeper.batterRBI(batter)
            self.umpire.scoreKeeper.pitcherR(pitcher)
            self.diamond.moveBase("third")
            ##############################

        # SecondBase
        elif self.diamond.getBase("second"):
            # Player at second scores
            player = self.diamond.getBase("second")
            self.umpire.recordRun()
            self.umpire.scoreKeeper.batterR(player)
            self.umpire.scoreKeeper.batterRBI(batter)
            self.umpire.scoreKeeper.pitcherR(pitcher)
            self.diamond.moveBase("second")
            ##############################

        # FirstBase
        elif self.diamond.getBase("first"):

            # Player at second scores
            player = self.diamond.getBase("first")
            self.umpire.recordRun()
            self.umpire.scoreKeeper.batterR(player)
            self.umpire.scoreKeeper.batterRBI(batter)
            self.umpire.scoreKeeper.pitcherR(pitcher)
            self.diamond.moveBase("first")


################################################################################
################################################################################


class DoublePlay(Out):

    def __init__(self, diamond, umpire):
        super().__init__(diamond, umpire)


    def generateTicket(self, * , pitcher, batter):
        super().generateTicket(pitcher=pitcher, batter=batter)

        if self.umpire.getOuts() < 3 and not self.diamond.getBasesEmpty():
            self.umpire.recordOut()
            self.umpire.scoreKeeper.pitcherOut(pitcher)

            if self.umpire.getOuts() < 3 and not self.diamond.getBasesEmpty():

                # State Pattern desired
                # Bases Loaded
                if self.diamond.getBasesLoaded():

                    # Player out at home
                    self.diamond.moveBase("third")
                    # Player at second moves to third
                    self.diamond.moveBase("second", "third")
                    # Player at first moves to second
                    self.diamond.moveBase("first", "second")
                    # Batter out at first


                # ThirdBase and SecondBase
                elif self.diamond.getBase("third") and self.diamond.getBase("second"):
                    # NONSENSE
                    # Player out at home
                    self.diamond.moveBase("third")
                    # Player at second moves to third
                    self.diamond.moveBase("second", "third")
                    # Batter out at first

                # ThirdBase and FirstBase
                elif self.diamond.getBase("third") and self.diamond.getBase("first"):

                    # Player at third scores
                    player = self.diamond.getBase("third")
                    self.umpire.recordRun()
                    self.umpire.scoreKeeper.batterR(player)
                    self.umpire.scoreKeeper.pitcherR(pitcher)
                    self.diamond.moveBase("third")
                    ##############################
                    # Player out moving to second
                    self.diamond.moveBase("first")
                    # Player out at first

                # SecondBase and FirstBase
                elif self.diamond.getBase("second") and self.diamond.getBase("first"):
                    # Player out moving to third
                    self.diamond.moveBase("second")
                    # Player out moving to second
                    self.diamond.moveBase("first")
                    # Player reaches first
                    self.diamond.setBase("first", batter)

                # ThirdBase
                elif self.diamond.getBase("third"):
                    self.diamond.moveBase("third")

                # SecondBase
                elif self.diamond.getBase("second"):
                    self.diamond.moveBase("second")

                # FirstBase
                elif self.diamond.getBase("first"):
                    # Player out moving to second
                    self.diamond.moveBase("first")


################################################################################
################################################################################


class TriplePlay(Ticket):

    def __init__(self, diamond, umpire):
        super().__init__(diamond, umpire)


    def generateTicket(self, * , pitcher, batter):
        super().generateTicket(pitcher=pitcher, batter=batter)

        # I know. This is stupid
        if self.umpire.getOuts() < 3 and not self.diamond.getBasesEmpty():
            self.umpire.recordOut()
            self.umpire.scoreKeeper.pitcherOut(pitcher)
        if self.umpire.getOuts() < 3 and not self.diamond.getBasesEmpty():
            self.umpire.recordOut()
            self.umpire.scoreKeeper.pitcherOut(pitcher)



################################################################################
################################################################################


class Walk(Ticket):

    def __init__(self, diamond, umpire):
        super().__init__(diamond, umpire)


    def generateTicket(self, * , pitcher, batter):
        super().generateTicket(pitcher=pitcher, batter=batter)

        if self.diamond.getBasesLoaded():

            # Player at third scores
            player = self.diamond.getBase("third")
            self.umpire.recordRun()
            self.umpire.scoreKeeper.batterR(player)
            self.umpire.scoreKeeper.batterRBI(batter)
            self.umpire.scoreKeeper.pitcherR(pitcher)
            self.diamond.moveBase("third")
            ##############################
            # Player as second moves to third
            self.diamond.moveBase("second", "third")
            # Player as first moves to second
            self.diamond.moveBase("first", "second")


        # ThirdBase and SecondBase
        elif self.diamond.getBase("third") and self.diamond.getBase("second"):
            pass


        # ThirdBase and FirstBase
        elif self.diamond.getBase("third") and self.diamond.getBase("first"):
            # Player as first moves to second
            self.diamond.moveBase("first", "second")


        # SecondBase and FirstBase
        elif self.diamond.getBase("second") and self.diamond.getBase("first"):
            # Player as second moves to third
            self.diamond.moveBase("second", "third")
            # Player as first moves to second
            self.diamond.moveBase("first", "second")


        # ThirdBase
        elif self.diamond.getBase("third"):
            pass

        # SecondBase
        elif self.diamond.getBase("second"):
            pass

        # FirstBase
        elif self.diamond.getBase("first"):
            # Player as first moves to second
            self.diamond.moveBase("first", "second")


        self.diamond.setBase("first", batter)

        self.umpire.scoreKeeper.pitcherBB(pitcher)
        self.umpire.scoreKeeper.batterBB(batter)


################################################################################
################################################################################


class HitByPitch(Walk):

    def __init__(self, diamond, umpire):
        super().__init__(diamond, umpire)


    def generateTicket(self, * , pitcher, batter):
        super().generateTicket(pitcher=pitcher, batter=batter)



################################################################################
################################################################################


class StrikeOut(Out):

    def __init__(self, diamond, umpire):
        super().__init__(diamond, umpire)


    def generateTicket(self, * , pitcher, batter):
        super().generateTicket(pitcher=pitcher, batter=batter)

        self.umpire.scoreKeeper.pitcherK(pitcher)


################################################################################
################################################################################


class ReachOnError(Ticket):

    def __init__(self, diamond, umpire):
        super().__init__(diamond, umpire)


    def generateTicket(self, * , pitcher, batter):
        super().generateTicket(pitcher=pitcher, batter=batter)
        self.umpire.scoreKeeper.batterAB(batter)

        if self.diamond.getBase("third"):
            # Player at third scores
            player = self.diamond.getBase("third")
            self.umpire.recordRun()
            self.umpire.scoreKeeper.batterR(player)
            self.umpire.scoreKeeper.pitcherR(pitcher)
            self.diamond.moveBase("third")
            ##############################

        # SecondBase
        elif self.diamond.getBase("second"):

            # Player at first moves to second
            self.diamond.moveBase("second", "third")
            ##############################

        # FirstBase
        elif self.diamond.getBase("first"):

            # Player at first moves to second
            self.diamond.moveBase("first", "second")

        self.diamond.setBase("first", batter)


################################################################################
################################################################################


class Sacrifice(FlyOut):

    def __init__(self, diamond, umpire):
        super().__init__(diamond, umpire)


    def generateTicket(self, * , pitcher, batter):
        super().generateTicket(pitcher=pitcher, batter=batter)


################################################################################
################################################################################
