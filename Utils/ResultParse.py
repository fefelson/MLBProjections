import re

################################################################################
################################################################################

playerPattern = re.compile("mlb.p.(?P<playerId>\d*)")
parenPattern = re.compile("\(.*?\)")

outToPattern = re.compile("out to (?P<field>\w*)")
groundOutPattern = re.compile("(?P<throw>\w*) to (?P<field>\w*)")

outPattern = re.compile("\[(?P<playerId>\d*)?\] out")
toFirst = re.compile("\[(?P<playerId>\d*)?\] to first")
toSecond = re.compile("\[(?P<playerId>\d*)?\] to second")
toThird = re.compile("\[(?P<playerId>\d*)?\] to third")
threeRuns = re.compile("\[(?P<playerId>\d*)?\], \[(?P<playerId1>\d*)?\] and \[(?P<playerId2>\d*)?\] scored")
twoRuns = re.compile("\[(?P<playerId>\d*)?\] and \[(?P<playerId1>\d*)?\] scored")
oneRun = re.compile("\[(?P<playerId>\d*)?\] scored")




# In order of most common
batterPatterns = (("Ground Out", re.compile("grounded (bunt |\s?)out")),
                  ("Strike Out", re.compile("struck out")),
                  ("Single", re.compile("singled|reached on an infield single")),
                  ("Fly Out", re.compile("flied out")),
                  ("Walk", re.compile("walked")),
                  ("Line Out", re.compile("lined out")),
                  ("Double", re.compile("doubled|ground rule double")),
                  ("Pop Out", re.compile("popped out")),
                  ("Home Run", re.compile("homered|inside the park home run")),
                  ("Fielder's Choice", re.compile("fielder's choice")),
                  ("Double Play", re.compile("double play")),
                  ("Fouled Out", re.compile("fouled out")),
                  ("Hit by Pitch", re.compile("hit by pitch")),
                  ("Reached on Error", re.compile("reached on 's (fielding|throwing) error")),
                  ("Sacrifice", re.compile("sacrificed|sacrifice fly")),
                  ("Triple", re.compile("tripled")),
                  ("Reached on Interference", re.compile("reached on catcher's interference")),
                  ("Triple Play", re.compile("triple play")),
                  ("Out on Interference", re.compile("out on batter's interference")),
                  ("Out of Order", re.compile("batted out of order")))


runnerPatterns = (("Stolen Base", re.compile("stole")),
                  ("Wild Pitch", re.compile("wild pitch")),
                  ("Caught Stealing", re.compile("caught stealing")),
                  ("Passed Ball", re.compile("passed ball")),
                  ("Fielder's Indifference", re.compile("fielder's indifference")),
                  ("Picked Off", re.compile("picked off")),
                  ("Advanced on Error", re.compile("(fielding|throwing) error")),
                  ("Balk", re.compile("balk")),
                  ("Out Advancing", re.compile("out advancing on throw")))


managerPatterns = (("Pitching Change", re.compile("pitching")),
                   ("Fielding Change", re.compile("(catching|first|second|third|shortstop|left|right|center|designated)")),
                   ("Pinch Hitter", re.compile("pinch hitter")),
                   ("Pinch Runner", re.compile("pinch runner")))


positions = {"pitcher":1, "catcher":2, "first":3, "second":4, "third":5,
             "shortstop":6, "left":7, "center":8, "right":9}



def searchAction(text, patterns):
    # Default if no matches
    resultLabel = "Label Error"
    for label, pattern in patterns:
        if pattern.search(text):
            resultLabel = label
            break
    return resultLabel



def runnerAction(text):
    text = re.sub("\[.*?\]","", text)
    return searchAction(text, runnerPatterns)


def runnerMovement(actions):
    if isinstance(actions, str):
        actions = (actions,)
    movements = []
    info = {"scored":[], "thirdBase":[], "secondBase":[], "out":[] }

    for text in actions:
        # Runs scored
        for runPattern in (threeRuns, twoRuns, oneRun):
            match = runPattern.search(text)
            if match:
                for player in ("playerId", "playerId1", "playerId2"):
                    try:
                        info["scored"].append(match.group(player))
                    except IndexError:
                        pass
                break
        # base move
        for baseKey, basePattern in (("secondBase", toSecond), ("thirdBase", toThird)):
            match = basePattern.search(text)
            if match:
                info[baseKey].append(match.group("playerId"))

        # out
        match = outPattern.search(text)
        if match:
            info["out"].append(match.group("playerId"))

    return info




def batterAction(text):

    text = re.sub("\[.*?\]","", text)
    text = text.split(",")[0]

    return searchAction(text, batterPatterns)


def managerAction(text):
    text = re.sub("\[.*?\]","", text)
    return searchAction(text, managerPatterns)


def cleanPlayerIds(text):
    for playerId in playerPattern.findall(text):
        text = playerPattern.sub(playerId, text, count=1)
    text = parenPattern.sub("", text)
    return text


def parseAtBat(text):
    text = cleanPlayerIds(text)
    action = batterAction(text)
    mainAction, *secondaryAction = text.split(".")
    mainMovement = runnerMovement(mainAction)
    secondaryMovement = runnerMovement(secondaryAction)
    return (action, mainMovement, secondaryMovement)




################################################################################
################################################################################
