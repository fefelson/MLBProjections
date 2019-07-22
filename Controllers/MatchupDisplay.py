import wx

from MLBProjections.MLBProjections.Views.MatchupDisplay import MatchupDisplay, MatchupPanel
from MLBProjections.MLBProjections.LineupSetter import LineupSetter
from MLBProjections.MLBProjections.SimulationSetter import SimulationSetter

################################################################################
################################################################################





################################################################################
################################################################################


class MatchupDisplayController:

    def __init__(self, groundControl):

        self.groundControl = groundControl
        self.displayView = MatchupDisplay(groundControl.getMainPanel())
        button = wx.Button(groundControl.getMainPanel(), label="Main")
        groundControl.addToMainSizer(self.displayView)
        groundControl.addToButtonSizer(button)

        for key, matchup in groundControl.getMatchups().items():
            print(key)
            newPanel = MatchupPanel(self.displayView.getMainPanel())

            newPanel.buttons["lineup"].SetName("{}".format(key))
            newPanel.buttons["lineup"].Bind(wx.EVT_BUTTON, self.setLineups)
            newPanel.buttons["sim"].SetName("{}".format(key))
            newPanel.buttons["sim"].Bind(wx.EVT_BUTTON, self.runSim)
            self.displayView.addMatchupPanel(newPanel)
            matchup.registerChangeObserver(newPanel)
            matchup.registerOnSetObserver(newPanel)


    def setLineups(self, event):
        gameId = event.GetEventObject().GetName()
        lineupSetter = LineupSetter(self.groundControl)
        matchup = self.groundControl.getMatchups(gameId)
        lineupSetter.setView(matchup.getInfo())
        lineupSetter.show()

    def runSim(self, event):
        object = event.GetEventObject()
        simSetter = SimulationSetter(self.groundControl, object.GetName())
        simSetter.show()


################################################################################
################################################################################
