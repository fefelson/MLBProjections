from pprint import pprint
from itertools import chain

################################################################################
################################################################################





################################################################################
################################################################################


class BaseballTeam:

    def __init__(self, db, isHome=False):

        team = "home" if isHome else "away"



        self.teamId = db.curs.execute("SELECT {0[team]}_id FROM games".format({"team":team})).fetchone()[0]
        self.isHome = isHome

        self.bullpen = []
        self.currentPitcher = None
        self.bullpen = [x[0] for x in db.curs.execute("SELECT player_id FROM bullpen WHERE team_id = ?",(self.teamId,)).fetchall()]
        self.lineup = [x[0] for x in db.curs.execute("SELECT player_id FROM lineups WHERE team_id = ? ORDER BY batt_order",(self.teamId,)).fetchall()]


        self.setPitcher(db.curs.execute("SELECT player_id FROM starter WHERE team_id = ?", (self.teamId, )).fetchone()[0])


    def getPitcher(self):
        return self.currentPitcher


    def getBullpen(self):
        return self.bullpen


    def setPitcher(self, pitcher):
        self.currentPitcher = pitcher
        # Remove pitcher from bullpen
        for i, player in enumerate(self.bullpen):
            if player == pitcher and len(self.bullpen) > 1:
                self.bullpen.pop(i)
                break


################################################################################
################################################################################
