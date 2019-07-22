import itertools
import wx
import wx.lib.agw.shapedbutton as wxsb

################################################################################
################################################################################


defaultValue = 75

timeFrameChoices = ("All", "Season", "3Months", "1Month")
outcomeChoices = ("Random", "Probable")


################################################################################
################################################################################


class SimulationFrame(wx.Frame):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.SetSize((400,600))

        self.panel = wx.Panel(self)

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.totalSizer = wx.BoxSizer(wx.VERTICAL)
        self.dateSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.outcomeSizer = wx.BoxSizer(wx.VERTICAL)
        self.buttonSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.simulationText = wx.StaticText(self.panel, label="Simulations")
        self.simulationText.SetFont(wx.Font(20, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.simulationTotal = wx.TextCtrl(self.panel, value=str(defaultValue), size=(40,40), style=wx.TE_PROCESS_ENTER)
        self.slider = wx.Slider(self.panel, value=75, minValue=30, maxValue=200, size=(150,50))
        #
        self.totalSizer.Add(self.simulationText, 0, wx.ALIGN_CENTER)
        self.totalSizer.Add(self.simulationTotal, 0, wx.ALIGN_CENTER)
        self.totalSizer.Add(self.slider, 0, wx.ALIGN_CENTER | wx.BOTTOM, 20)

        okBitmap =  wx.Image("/home/ededub/Downloads/ok.png", wx.BITMAP_TYPE_ANY).Scale(50, 50, wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
        cancelBitmap =  wx.Image("/home/ededub/Downloads/cancel.png", wx.BITMAP_TYPE_ANY).Scale(50, 50, wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
        self.okButton = wxsb.SBitmapButton(self.panel, id=wx.ID_APPLY, bitmap=okBitmap)
        self.cancelButton = wxsb.SBitmapButton(self.panel, id=wx.ID_CANCEL, bitmap=cancelBitmap)
        ##
        self.buttonSizer.Add(self.okButton, 1, wx.ALIGN_CENTER)
        self.buttonSizer.Add(self.cancelButton, 1, wx.ALIGN_CENTER)


        self.dateTitles = {}
        self.dateUpArrows = {}
        self.dateDownArrows = {}
        self.dateNumBox = {}

        upBitmap = wx.Image("/home/ededub/Downloads/arrow.png", wx.BITMAP_TYPE_ANY).Scale(15, 15, wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
        downBitmap = wx.Image("/home/ededub/Downloads/arrow.png", wx.BITMAP_TYPE_ANY).Scale(15, 15, wx.IMAGE_QUALITY_HIGH).Rotate180().ConvertToBitmap()

        for i, timeFrame in enumerate(timeFrameChoices):
            timeFrameSizer = wx.BoxSizer(wx.VERTICAL)
            self.dateTitles[timeFrame] = wx.StaticText(self.panel, label=timeFrame)
            self.dateUpArrows[timeFrame] = wx.BitmapButton(self.panel, id=wx.ID_UP, bitmap=upBitmap, name=timeFrame)
            self.dateDownArrows[timeFrame] = wx.BitmapButton(self.panel, id=wx.ID_DOWN, bitmap=downBitmap, name=timeFrame)
            self.dateNumBox[timeFrame] = wx.TextCtrl(self.panel, value=str(int(defaultValue/len(timeFrameChoices)) + int(defaultValue%len(timeFrameChoices) > i)), size=(40,40))

            timeFrameSizer.Add(self.dateTitles[timeFrame])
            timeFrameSizer.Add(self.dateUpArrows[timeFrame])
            timeFrameSizer.Add(self.dateNumBox[timeFrame])
            timeFrameSizer.Add(self.dateDownArrows[timeFrame])
            self.dateSizer.Add(timeFrameSizer, 1, wx.EXPAND | wx.ALIGN_CENTER)

        self.outcomeTitles = {}
        self.outcomeUpArrows = {}
        self.outcomeDownArrows = {}
        self.outcomeNumBox = {}

        for i, outcome in enumerate(outcomeChoices):
            newOutcomeSizer = wx.BoxSizer(wx.HORIZONTAL)
            self.outcomeTitles[outcome] = wx.StaticText(self.panel, label=outcome)
            self.outcomeUpArrows[outcome] = wx.BitmapButton(self.panel, id=wx.ID_UP, bitmap=upBitmap, name=outcome)
            self.outcomeDownArrows[outcome] = wx.BitmapButton(self.panel, id=wx.ID_DOWN, bitmap=downBitmap, name=outcome)
            self.outcomeNumBox[outcome] = wx.TextCtrl(self.panel, value=str(int(defaultValue/len(outcomeChoices)) + int(defaultValue%len(outcomeChoices) > i)), size=(40,40))
            newOutcomeSizer.Add(self.outcomeTitles[outcome], 1, wx.ALIGN_RIGHT | wx.RIGHT, 20)
            newOutcomeSizer.Add(self.outcomeUpArrows[outcome], 0)
            newOutcomeSizer.Add(self.outcomeNumBox[outcome], 0)
            newOutcomeSizer.Add(self.outcomeDownArrows[outcome], 0)
            self.outcomeSizer.Add(newOutcomeSizer, 1, wx.EXPAND)


        self.mainSizer.Add(self.totalSizer, 1, wx.EXPAND | wx.TOP, 30)
        self.mainSizer.Add(self.dateSizer, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 20)
        self.mainSizer.Add(self.outcomeSizer, 1, wx.ALL, 20)
        self.mainSizer.Add(self.buttonSizer, 0, wx.EXPAND | wx.BOTTOM, 15)

        self.panel.SetSizer(self.mainSizer)


################################################################################
################################################################################


class SimulationModel:

    def __init__(self, gameId):

        self.gameId = gameId
        self.simulationTotal = defaultValue
        self.dateValues = {}
        self.outcomeValues = {}

        for i, timeFrame in enumerate(timeFrameChoices):
            self.dateValues[timeFrame] = int(defaultValue/len(timeFrameChoices)) + int(defaultValue%len(timeFrameChoices) > i)

        for i, outcome in enumerate(outcomeChoices):
            self.outcomeValues[outcome] = int(defaultValue/len(outcomeChoices)) + int(defaultValue%len(outcomeChoices) > i)


    def getGameId(self):
        return self.gameId


    def getTotalValue(self):
        return self.simulationTotal


    def setTotalValue(self, value):
        self.simulationTotal = value


    def setDateValue(self, key, value):
        self.dateValues[key] = value


    def setOutcomeValue(self, key, value):
        self.outcomeValues[key] = value


    def getDateValue(self, key):
        return self.dateValues[key]


    def getOutcomeValue(self, key):
        return self.outcomeValues[key]




################################################################################
################################################################################


class SimulationSetter:

    def __init__(self, groundControl, gameId):

        self.groundControl = groundControl
        self.model = SimulationModel(gameId)
        # for testing and debugging
        # TODO: Learn to test things properly
        # self.frame = SimulationFrame(None)
        self.frame = SimulationFrame(groundControl.frame)

        # Bind Controls
        self.frame.simulationTotal.Bind(wx.EVT_TEXT_ENTER, self.onSimTotal)
        self.frame.slider.Bind(wx.EVT_SLIDER, self.onSlider)
        self.frame.okButton.Bind(wx.EVT_BUTTON, self.onOk)
        self.frame.cancelButton.Bind(wx.EVT_BUTTON, self.onCancel)

        for arrow in itertools.chain(self.frame.dateUpArrows.values(),
                                    self.frame.dateDownArrows.values(),
                                    self.frame.outcomeUpArrows.values(),
                                    self.frame.outcomeDownArrows.values()):

                                    arrow.Bind(wx.EVT_BUTTON, self.onArrow)

        for textCtrl in itertools.chain(self.frame.dateNumBox.values(),
                                        self.frame.outcomeNumBox.values()):

                                        textCtrl.Bind(wx.EVT_TEXT_ENTER, self.onItemTotal)


    def show(self):
        self.frame.Show()


    def onSimTotal(self, event):
        object = event.GetEventObject()
        try:
            value = int(object.GetValue())
            if value >= self.frame.slider.GetMin() and value <= self.frame.slider.GetMax():
                self.model.setTotalValue(value)
                object.SetValue(str(value))
                self.frame.slider.SetValue(value)

                for i, timeFrame in enumerate(timeFrameChoices):
                    dateValue = int(value/len(timeFrameChoices)) + int(value%len(timeFrameChoices) > i)
                    self.model.setDateValue(timeFrame, dateValue)
                    self.frame.dateNumBox[timeFrame].SetValue(str(dateValue))

                for i, outcome in enumerate(outcomeChoices):
                    outcomeValue = int(value/len(outcomeChoices)) + int(value%len(outcomeChoices) > i)
                    self.model.setOutcomeValue(outcome, outcomeValue)
                    self.frame.outcomeNumBox[outcome].SetValue(str(outcomeValue))



            else:
                object.SetValue(str(self.model.getTotalValue()))
        except ValueError:
            object.SetValue(str(self.model.getTotalValue()))

        self.frame.Layout()


    def onSlider(self, event):
        value = event.GetEventObject().GetValue()

        self.model.setTotalValue(value)
        self.frame.simulationTotal.SetValue(str(value))

        for i, timeFrame in enumerate(timeFrameChoices):
            dateValue = int(value/len(timeFrameChoices)) + int(value%len(timeFrameChoices) > i)
            self.model.setDateValue(timeFrame, dateValue)
            self.frame.dateNumBox[timeFrame].SetValue(str(dateValue))

        for i, outcome in enumerate(outcomeChoices):
            outcomeValue = int(value/len(outcomeChoices)) + int(value%len(outcomeChoices) > i)
            self.model.setOutcomeValue(outcome, outcomeValue)
            self.frame.outcomeNumBox[outcome].SetValue(str(outcomeValue))

        self.frame.Layout()


    def onItemTotal(self, event):
        pass


    def onArrow(self, event):
        pass


    def onOk(self, event):
        info = {}
        info["total"] = self.model.getTotalValue()
        info["dateValues"] = [(timeFrame, self.model.getDateValue(timeFrame)) for timeFrame in timeFrameChoices]
        info["outcomeValues"] = [(outcome, self.model.getOutcomeValue(outcome)) for outcome in outcomeChoices]
        self.frame.Close()
        self.groundControl.runSimulation(self.model.getGameId(), info)


    def onCancel(self, event):
        self.frame.Close()




################################################################################
################################################################################

if __name__ == "__main__":

    app = wx.App()
    frame = SimulationSetter(None)
    frame.show()
    app.MainLoop()
