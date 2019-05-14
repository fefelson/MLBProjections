import wx
from pprint import pprint
from os import environ
from json import load, dump
from datetime import date, timedelta
import sqlite3

###########################################

matchupPath = environ["HOME"] +"/FEFelson/MLBProjections/Matchups/{}.json"
lineupPath = environ["HOME"] +"/FEFelson/MLBProjections/Lineups/{}.json"
dBPath = environ["HOME"] +"/FEFelson/MLBProjections/mlb.db"

conn = sqlite3.connect(dBPath)
curs = conn.cursor()


gameDate = date.today()

############################################



########  SQL Commands ##############################################


starterCmd = """
            SELECT player_id, first_name, last_name FROM pro_players
            WHERE player_id = ?
            """


benchCmd = """
            SELECT DISTINCT rosters.player_id, first_name, last_name FROM pro_players
            INNER JOIN rosters ON pro_players.player_id = rosters.player_id
            INNER JOIN results ON pro_players.player_id = results.batter_id
            INNER JOIN games ON rosters.game_id = games.game_id
            WHERE team_id = ?
            ORDER BY last_name
            """


bullpenCmd = """
            SELECT DISTINCT rosters.player_id, first_name, last_name FROM pro_players
            INNER JOIN rosters ON pro_players.player_id = rosters.player_id
            INNER JOIN results ON pro_players.player_id = results.pitcher_id
            INNER JOIN games ON rosters.game_id = games.game_id
            WHERE season = 2019 AND team_id = ?
            ORDER BY last_name
            """


lineupCmd = """
            SELECT lineups.player_id, first_name, last_name, batt_order, pos FROM lineups
            INNER JOIN pro_players ON lineups.player_id = pro_players.player_id
            INNER JOIN (SELECT team_id, MAX(game_id) AS game_id FROM lineups WHERE team_id = ?) AS max_id ON lineups.game_id = max_id.game_id AND lineups.team_id = max_id.team_id
            WHERE sub_order = 1 AND pos != 'P'
            ORDER BY batt_order
            """


#####################################################################




class Model:

    def __init__(self):

        self.matchups = []
        self.teams = []
        self.setMatchups()
        self.index = 0
        self.team = None
        self.player = None


    def setStarter(self, player):
        self.team.starter = player


    def changeBenchOrder(self, oldN, newN, player):
        self.team.lineup.pop(oldN)
        self.team.lineup.insert(newN, player)


    def removeLineup(self, player):
        self.team.lineup.remove(player)


    def addLineup(self, player):
        self.team.lineup.append(player)


    def nextTeam(self):
        self.team = self.teams[self.index]
        self.index += 1


    def writeFile(self):
        x = []
        for match in self.matchups:
            x.append({"gameId":match["gameId"], "homeTeam": match["homeTeam"].getJson(), "awayTeam": match["awayTeam"].getJson()})


        with open(lineupPath.format("".join(str(gameDate).split("-"))), "w") as fileOut:
            dump({"matchups":x}, fileOut)


    def setMatchups(self):
        filePath = matchupPath.format("".join(str(gameDate).split("-")))
        with open(filePath) as fileIn:
            matchups = load(fileIn)

        for game in matchups:
            gameId = game["gameId"]
            homeId = game["homeTeam"]
            awayId = game["awayTeam"]
            gameTime = game["gameTime"]
            homePitcher = game["homePitcher"]
            awayPitcher = game["awayPitcher"]

            homeTeam = Team(homeId, homePitcher)
            awayTeam = Team(awayId, awayPitcher)
            self.teams.append(homeTeam)
            self.teams.append(awayTeam)
            self.matchups.append({"gameId":gameId, "homeTeam": homeTeam, "awayTeam": awayTeam})



class Controller:

    def __init__(self):

        self.model = Model()
        self.view = View(None)
        self.model.nextTeam()
        self.view.setTeam(self.model.team)
        self.view.actionBtn.Bind(wx.EVT_BUTTON, self.onActionBtn)
        self.view.upBtn.Bind(wx.EVT_BUTTON, self.upMove)
        self.view.downBtn.Bind(wx.EVT_BUTTON, self.downMove)
        self.view.pitchers.Bind(wx.EVT_LISTBOX_DCLICK, self.selectPitcher)
        self.view.bench.Bind(wx.EVT_LISTBOX_DCLICK, self.setLineup)
        self.view.lineup.Bind(wx.EVT_LISTBOX_DCLICK, self.removeLineup)
        self.view.Show()


    def setLineup(self, event):
        listBox = event.GetEventObject()
        player = listBox.GetClientData(listBox.GetSelection())
        self.view.lineup.Append(str(player),player)
        self.model.addLineup(player)
        self.view.lineup.Clear()
        for player in self.model.team.lineup:
            self.view.lineup.Append(str(player), player)


    def removeLineup(self, event):
        listBox = event.GetEventObject()
        player = listBox.GetClientData(listBox.GetSelection())
        self.model.removeLineup(player)
        self.view.lineup.Clear()
        for player in self.model.team.lineup:
            self.view.lineup.Append(str(player), player)




    def selectPitcher(self, event):
        listBox = event.GetEventObject()
        player = listBox.GetClientData(listBox.GetSelection())

        self.view.starter.SetLabel(str(player))
        self.model.setStarter(player)
        self.view.Layout()


    def upMove(self, event):
        n = self.view.lineup.GetSelection()
        if  n > 0:
            player = self.view.lineup.DetachClientObject(n)
            self.view.lineup.Delete(n)
            self.view.lineup.Insert(str(player), n-1, player)
            self.view.lineup.SetSelection(n-1)
            self.model.changeBenchOrder(n, n-1, player)
            self.view.Layout()


    def downMove(self, event):
        n = self.view.lineup.GetSelection()
        if  n > -1 and n+1 < len(self.view.lineup.GetItems()):
            player = self.view.lineup.DetachClientObject(n)
            self.view.lineup.Delete(n)
            self.view.lineup.Insert(str(player), n+1, player)
            self.view.lineup.SetSelection(n+1)
            self.model.changeBenchOrder(n, n+1, player)
            self.view.Layout()




    def onActionBtn(self, event):
        self.view.starter.SetLabel("")
        self.view.lineup.Clear()
        self.view.bench.Clear()
        self.view.pitchers.Clear()
        if self.model.index == len(self.model.teams):
            self.model.writeFile()
            self.view.Close()
        else:
            self.model.nextTeam()
            self.view.setTeam(self.model.team)
        self.view.Layout()


class Team:

    def __init__(self, teamId, starter):

        self.teamId = teamId
        self.starter = curs.execute(starterCmd,(starter,)).fetchone()

        self.batters = []
        self.pitchers = []
        self.lineup = []


        self.setLineup()
        self.setBullpen()
        self.setBench()


    def getJson(self):
        return {"teamId": self.teamId, "starter": self.starter, "lineup": [ x[0] for x in self.lineup ]}


    def setBench(self):
        for playerId, firstName, lastName in curs.execute(benchCmd,(self.teamId,)).fetchall():
            self.batters.append((playerId, firstName, lastName))


    def setBullpen(self):
        for playerId, firstName, lastName in curs.execute(bullpenCmd,(self.teamId,)).fetchall():
            self.pitchers.append((playerId, firstName, lastName))


    def setLineup(self):
        for playerId, firstName, lastName, battOrder, pos in curs.execute(lineupCmd, (self.teamId,)).fetchall():
            self.lineup.append((playerId, firstName, lastName, battOrder, pos))




class View(wx.Frame):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.panel = wx.Panel(self)

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.pitcherSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.orderSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.btnSizer = wx.BoxSizer(wx.VERTICAL)

        ##########
        self.starter = wx.StaticText(self.panel, label="No Selection")
        self.pitchers = wx.ListBox(self.panel)
        self.pitcherSizer.Add(self.starter, 1, wx.EXPAND)
        self.pitcherSizer.Add(self.pitchers, 1, wx.EXPAND)

        ##########

        self.lineup = wx.ListBox(self.panel)
        self.bench = wx.ListBox(self.panel)

        self.upBtn = wx.Button(self.panel, label="up")
        self.downBtn = wx.Button(self.panel, label="dn")
        self.btnSizer.Add(self.upBtn, 0)
        self.btnSizer.Add(self.downBtn, 0)

        self.orderSizer.Add(self.lineup, 1, wx.EXPAND)
        self.orderSizer.Add(self.btnSizer, 0, wx.EXPAND)
        self.orderSizer.Add(self.bench, 1, wx.EXPAND)

        ##########

        self.actionBtn = wx.Button(self.panel, label="Next")

        self.mainSizer.Add(self.pitcherSizer, 1, wx.EXPAND)
        self.mainSizer.Add(self.orderSizer, 1, wx.EXPAND)
        self.mainSizer.Add(self.actionBtn, 0, wx.EXPAND)

        self.panel.SetSizer(self.mainSizer)




    def setTeam(self, team):
        self.team = team
        self.starter.SetLabel(str(self.team.starter))


        for player in self.team.batters:
            self.bench.Append(str(player), player)

        for player in self.team.pitchers:
            self.pitchers.Append(str(player), player)

        for player in self.team.lineup:
            self.lineup.Append(str(player), player)
        self.Layout()








if __name__ == "__main__":

    app = wx.App()
    c = Controller()
    app.MainLoop()


    conn.close()
