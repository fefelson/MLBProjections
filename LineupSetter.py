import wx
from pprint import pprint
from itertools import chain

################################################################################
################################################################################





################################################################################
################################################################################


class LineupFrame(wx.Frame):


    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.SetSize((800,500))
        self.panel = wx.Panel(self)

        self.teamNames = {}
        self.starters = {}
        self.lineupSlots = {"home":[], "away":[]}
        self.orders = {"home":[], "away":[]}
        self.pos = {"home":[], "away":[]}
        self.sizers = {"home":[], "away":[]}

        for team in ("away", "home"):
            self.teamNames[team] = self._team(team)
            self.starters[team] = self._starter(team)
            for i in range(9):
                self.lineupSlots[team].append(wx.ComboBox(self.panel, style=wx.CB_READONLY))
                self.orders[team].append(self._order(team, i))
                self.pos[team].append(self._pos(team, i))

        self.setLineupButton = wx.Button(self.panel, label="Set Lineup")

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.matchSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.leftSizer = wx.BoxSizer(wx.VERTICAL)
        self.leftSizer.Add(self.teamNames["away"], 0, wx.ALIGN_CENTER | wx.BOTTOM, 10)
        self.leftSizer.Add(self.starters["away"], 0, wx.ALIGN_CENTER | wx.BOTTOM, 20)
        self.rightSizer = wx.BoxSizer(wx.VERTICAL)
        self.rightSizer.Add(self.teamNames["home"], 0, wx.ALIGN_CENTER | wx.BOTTOM, 10)
        self.rightSizer.Add(self.starters["home"], 0, wx.ALIGN_CENTER | wx.BOTTOM, 20)

        for i in range(9):
            for team in ("away", "home"):
                sizer = wx.BoxSizer(wx.HORIZONTAL)
                sizer.Add(self.orders[team][i], 0)
                sizer.Add(self.lineupSlots[team][i], 1, wx.EXPAND)
                sizer.Add(self.pos[team][i], 0)
                self.sizers[team].append(sizer)

                if team == "home":
                    self.rightSizer.Add(sizer, 0)
                else:
                    self.leftSizer.Add(sizer, 0)

        self.matchSizer.Add(self.leftSizer, 1, wx.EXPAND | wx.RIGHT, 20)
        self.matchSizer.Add(self.rightSizer, 1, wx.EXPAND | wx.LEFT, 20)
        self.mainSizer.Add(self.matchSizer,1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 40)
        self.mainSizer.Add(self.setLineupButton, 0, wx.EXPAND)

        self.panel.SetSizer(self.mainSizer)


    def _team(self, team):
        newTeam = wx.StaticText(self.panel, label="New Team", name=team)
        newTeam.SetFont(wx.Font(15, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        return newTeam


    def _starter(self, team):
        newStarter = wx.ComboBox(self.panel, value="{} Starter".format(team.capitalize()), name=team)
        newStarter.SetMinSize((200,30))
        return newStarter


    def _order(self, team, i):
        newOrder = wx.ComboBox(self.panel, choices=[str(n) for n in range(1,10)], style=wx.CB_READONLY, name="{} {}".format(team, i))
        newOrder.SetValue(str(i+1))
        newOrder.SetMinSize((50,30))
        return newOrder


    def _pos(self, team, i):
        newPos = wx.ComboBox(self.panel, choices=["C","1B","2B","3B","SS","LF", "CF", "RF", "DH", "P"], style=wx.CB_READONLY, name="{} {}".format(team, i))
        newPos.SetMinSize((70,30))
        newPos.Disable()
        return newPos


    def _name(self, player):
        firstName = player["firstName"]
        lastName = player["lastName"]
        return firstName, lastName


    def setView(self, info):
        # pprint(info)
        for homeAway in ("home", "away"):
            team = info["teams"][homeAway]
            self.teamNames[homeAway].SetLabel("{} {}".format(team["info"]["city"], team["info"]["mascot"]))


            for i, pitcher in enumerate(info["teams"][homeAway]["roster"]["pitchers"]):
                self.starters[homeAway].Append("{} {}".format(*self._name(pitcher)), pitcher)
                try:
                    #  This is embarassing hack about playerId player_id
                    if str(pitcher["playerId"]) == str(info["teams"][homeAway]["starter"]["player_id"]):
                        self.starters[homeAway].SetSelection(i)
                except KeyError:
                    if str(pitcher["playerId"]) == str(info["teams"][homeAway]["starter"]["playerId"]):
                        self.starters[homeAway].SetSelection(i)
                except TypeError:
                    pass

            i = 0
            for batter in info["teams"][homeAway]["lineup"]:
                if batter[-1] != "P" and (info["league"] == "AL" or batter[-1] != "DH"):
                    self.pos[homeAway][i].SetValue(batter[-1])
                    for j, player in enumerate(info["teams"][homeAway]["roster"]["batters"]):
                        self.lineupSlots[homeAway][i].Append("{} {}".format(*self._name(player)), player)
                        if str(player["playerId"]) == str(batter[0]):
                            self.lineupSlots[homeAway][i].SetSelection(j)
                    i+=1


            if self.lineupSlots[homeAway][-1].GetSelection() == -1:
                if info["league"] == "AL":
                    self.pos[homeAway][-1].SetValue("DH")
                    for j, player in enumerate(info["teams"][homeAway]["roster"]["batters"]):
                        self.lineupSlots[homeAway][-1].Append("{} {}".format(*self._name(player)), player)
                else:
                    self.pos[homeAway][-1].SetValue("P")
                    for j, player in enumerate(info["teams"][homeAway]["roster"]["batters"]):
                        self.lineupSlots[homeAway][-1].Append("{} {}".format(*self._name(player)), player)
                    if self.starters[homeAway].GetSelection() != -1:
                        player = self.starters[homeAway].GetClientData(self.starters[homeAway].GetSelection())
                        for k in range(9):
                            self.lineupSlots[homeAway][k].Append("{} {}".format(*self._name(player)), player)

                        self.lineupSlots[homeAway][-1].SetValue("{} {}".format(*self._name(player)))
                        self.lineupSlots[homeAway][-1].Disable()

################################################################################
################################################################################


class LineupSetter:

    def __init__(self, groundControl):

        self.gameId = None
        self.groundControl = groundControl
        self.frame = LineupFrame(groundControl.frame)

        for team in ("away", "home"):
            self.frame.starters[team].Bind(wx.EVT_COMBOBOX, self.onStarter)
            for batOrder in self.frame.orders[team]:
                batOrder.Bind(wx.EVT_COMBOBOX, self.onOrder)
        self.frame.setLineupButton.Bind(wx.EVT_BUTTON, self.onLineup)


    def setView(self, info):
        self.gameId = info["gameId"]
        self.frame.setView(info)


    def show(self):
        self.frame.Show()


    def onStarter(self, event):
        object = event.GetEventObject()
        pitcher = object.GetClientData(object.GetSelection())
        firstName = pitcher["firstName"]
        lastName = pitcher["lastName"]

        team = object.GetName()
        lineupSlots = self.frame.lineupSlots[team]
        pos = self.frame.pos[team]

        for slot in lineupSlots:
            slot.Append("{} {}".format(firstName, lastName), pitcher)
        for p in pos:
            if p.GetStringSelection() == "P":
                index = int(p.GetName().split()[-1])
                lineupSlots[index].SetValue("{} {}".format(firstName, lastName))
        self.frame.Layout()


    def onOrder(self, event):
        object = event.GetEventObject()
        team, index = object.GetName().split()
        value = int(object.GetStringSelection()) -1

        lineupSlots = self.frame.lineupSlots[team]
        pos = self.frame.pos[team]
        orders = self.frame.orders[team]


        player = lineupSlots[int(index)].GetClientData(lineupSlots[int(index)].GetSelection())
        pFirst = player["firstName"]
        pLast = player["lastName"]
        playerPos = pos[int(index)].GetStringSelection()

        tempPlayer = lineupSlots[value].GetClientData(lineupSlots[value].GetSelection())
        tFirst = tempPlayer["firstName"]
        tLast = tempPlayer["lastName"]
        tempPos = pos[value].GetStringSelection()

        lineupSlots[value].SetValue("{} {}".format(pFirst, pLast))
        pos[value].SetValue(playerPos)
        if playerPos == "P":
            lineupSlots[value].Disable()
        else:
            lineupSlots[value].Enable()

        lineupSlots[int(index)].SetValue("{} {}".format(tFirst, tLast))
        pos[int(index)].SetValue(tempPos)
        if tempPos == "P":
            lineupSlots[int(index)].Disable()
        else:
            lineupSlots[int(index)].Enable()

        object.SetValue(str(int(index)+1))
        self.frame.Layout()


    def onLineup(self, event):
        info = {"home":{"starter":None, "lineup":[]},
                "away": {"starter":None, "lineup":[]}}

        for homeAway in ("home", "away"):
            lineupSlots = self.frame.lineupSlots[homeAway]
            pos = self.frame.pos[homeAway]
            orders = self.frame.orders[homeAway]
            starters = self.frame.starters[homeAway]

            info[homeAway]["starter"] = starters.GetClientData(starters.GetSelection())
            info[homeAway]["lineup"] = []
            for i in range(9):
                p = pos[i].GetStringSelection()
                player = lineupSlots[i].GetClientData(lineupSlots[i].GetSelection())
                player["battOrder"] = i+1
                player["pos"] = p
                info[homeAway]["lineup"].append(player)
        self.frame.Close()
        self.groundControl.setModelLineup(self.gameId, info)


################################################################################
################################################################################


if __name__ == "__main__":

    app = wx.App()
    frame = LineupFrame(None)
    frame.Show()
    app.MainLoop()
