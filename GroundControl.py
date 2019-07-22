import datetime
import queue
import wx

from MLBProjections.MLBProjections.Models.ProjectionModel import MLBProjections
from MLBProjections.MLBProjections.Controllers.MatchupDisplay import MatchupDisplayController

from pprint import pprint

################################################################################
################################################################################





################################################################################
################################################################################


class GroundControl:


    def __init__(self, model):

        self.model = model
        self.frame = MainFrame(None)
        self.components = (MatchupDisplayController(self),
                            )
        self.frame.Show()


    def getMainPanel(self):
        return self.frame.getMainPanel()


    def addToMainSizer(self, panel):
        self.frame.addToMainSizer(panel)


    def addToButtonSizer(self, bttn):
        self.frame.addToButtonSizer(bttn)
        bttn.Bind(wx.EVT_BUTTON, self.onShow)


    def onShow(self, event):
        pass


    def getMatchups(self, key=None):
        return self.model.getMatchups(key)


    def runSimulation(self, index, info):
        print(index)
        pprint(info)


    def setModelLineup(self, index, info):
        matchup = self.getMatchups(index)
        matchup.newLineup(info)

        if not self.model.gameDBExists(index):
            gameDB = self.model.newGameDB(matchup)
            matchup.registerChangeObserver(gameDB)
            matchup.notifyOnSet()


################################################################################
################################################################################


class MainFrame(wx.Frame):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, size=(1100,700), title="FEFelson", *args, **kwargs)

        self.panel = wx.Panel(self)
        self.panelSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.mainSizer = wx.BoxSizer()
        self.buttonSizer = wx.BoxSizer(wx.VERTICAL)
        self.buttonSizer.SetMinSize(100,-1)

        self.panelSizer.Add(self.mainSizer, 1, wx.EXPAND)
        self.panelSizer.Add(self.buttonSizer, 0, wx.EXPAND)
        self.panel.SetSizer(self.panelSizer)


    def getMainPanel(self):
        return self.panel


    def addToMainSizer(self, view):
        self.mainSizer.Add(view, 1, wx.EXPAND)


    def addToButtonSizer(self, bttn):
        self.buttonSizer.Add(bttn)



################################################################################
################################################################################

if __name__ == "__main__":

    app = wx.App()
    model = MLBProjections()
    control = GroundControl(model)
    app.MainLoop()
