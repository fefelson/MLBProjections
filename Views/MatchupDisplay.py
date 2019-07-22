import datetime
import wx

import MLBProjections.MLBProjections.Environ as ENV

################################################################################
################################################################################





################################################################################
################################################################################


class MatchupDisplay(wx.Panel):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.gameDayPanel = wx.ScrolledWindow(self, style=wx.VSCROLL)
        self.gameDayPanel.SetScrollbars(20, 20, 50, 50)

        self.gameDate = wx.StaticText(self, label=datetime.datetime.today().strftime("%A %B %d %Y"))
        self.gameDate.SetFont(wx.Font(16, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.gameDaySizer = wx.GridSizer(cols=4, vgap=50, hgap=50)
        self.gameDayPanel.SetSizer(self.gameDaySizer)

        self.mainSizer.Add(self.gameDate, 0, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 10)
        self.mainSizer.Add(self.gameDayPanel, 1, wx.EXPAND | wx.TOP | wx.BOTTOM, 20)
        self.SetSizer(self.mainSizer)


    def addMatchupPanel(self, matchupPanel):
        self.gameDaySizer.Add(matchupPanel)


    def getMainPanel(self):
        return self.gameDayPanel



################################################################################
################################################################################


class MatchupPanel(wx.Panel):


    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.SetMinSize((200,200))

        self.isSet = False
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.topSizer = wx.BoxSizer(wx.HORIZONTAL)
        # BoxSizer(wx.HORIZONTAL)
        self.pitcherSizer = {}

        self.gameTime = wx.StaticText(self)
        self.gameTime.SetFont(wx.Font(12, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

        vs = wx.StaticText(self, label="VS.")

        # StaticBitmaps
        self.logos = {}
        # StaticText
        self.abrvs = {}
        # StaticText
        self.pitchers = {}
        # Button
        self.buttons = self._setButtons()

        for team in ("away", "home"):
            self.pitcherSizer[team] = wx.BoxSizer(wx.HORIZONTAL)
            self.logos[team] = self._newLogo()
            self.abrvs[team] = self._newAbrv()
            self.pitchers[team] = self._newPitcher()

            self.pitcherSizer[team].Add(self.abrvs[team], 0, wx.RIGHT, 4)
            self.pitcherSizer[team].Add(self.pitchers[team], 1, wx.LEFT, 4)

        self.topSizer.Add(self.logos["away"], 1, wx.ALIGN_CENTER)
        self.topSizer.Add(vs, 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 15)
        self.topSizer.Add(self.logos["home"], 1, wx.ALIGN_CENTER)
        self.mainSizer.Add(self.topSizer, 1, wx.ALIGN_CENTER)
        self.mainSizer.Add(self.gameTime, 0, wx.ALIGN_CENTER)
        self.mainSizer.Add(self.pitcherSizer["away"], 0, wx.ALIGN_CENTER)
        self.mainSizer.Add(self.pitcherSizer["home"], 0, wx.ALIGN_CENTER)
        self.mainSizer.Add(self.buttons["lineup"], 0, wx.ALIGN_CENTER)
        self.mainSizer.Add(self.buttons["sim"], 0, wx.ALIGN_CENTER)

        self.SetSizer(self.mainSizer)


    def _setButtons(self):
        buttons = {}
        for key, label, enable in (("lineup", "Set Lineup", True),
                                    ("sim", "Run Simulation", False)):
            bttn = wx.Button(self, label=label)
            bttn.Enable(enable)
            buttons[key] = bttn
        return buttons


    def _newLogo(self):
        newLogo = wx.StaticBitmap(self, size=(50,50))
        newLogo.SetMinSize((50,50))
        return newLogo


    def _newAbrv(self):
        abrv = wx.StaticText(self)
        abrv.SetFont(wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        return abrv


    def _newPitcher(self):
        pitcher = wx.StaticText(self, label="TBD")
        pitcher.SetFont(wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        return pitcher


    def onSet(self):
        for team in ("home", "away"):
            teamId = self.logos[team].GetName()
            logo = wx.Image(ENV.getPath("logo", fileName=teamId), wx.BITMAP_TYPE_ANY).Scale(50, 50, wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
            self.logos[team].SetBitmap(logo)
        self.buttons["sim"].Enable()
        self.isSet = True

        self.Layout()


    def notify(self, info):
        self.gameTime.SetLabel(info["gameTime"])
        for homeAway in ("home", "away"):
            team = info["teams"][homeAway]
            if not self.isSet:
                logo = wx.Image(ENV.getPath("g-logo", fileName=team["teamId"]), wx.BITMAP_TYPE_ANY).Scale(50, 50, wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
                self.logos[homeAway].SetBitmap(logo)
                self.logos[homeAway].SetName(team["teamId"])
                self.abrvs[homeAway].SetLabel(team["info"]["abrv"])
            try:
                self.pitchers[homeAway].SetLabel("{}".format(team["starter"]["last_name"]))
            except KeyError:
                self.pitchers[homeAway].SetLabel("{}".format(team["starter"]["lastName"]))
            except TypeError:
                pass
        self.Layout()




################################################################################
################################################################################
