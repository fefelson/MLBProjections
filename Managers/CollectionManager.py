import os

import MLBProjections.MLBProjections.Environ as ENV

################################################################################
################################################################################





################################################################################
################################################################################


class CollectionManager:


    def getMatchupFiles(self, gameDate):
        matchFiles = []
        filePath = "/".join(ENV.getPath("matchup", gameDate=gameDate).split("/")[:-1])
        if os.path.exists(filePath):
            for fileName in [filePath+"/"+fileName for fileName in os.listdir(filePath) if "M" in fileName]:
                matchFiles.append(ENV.getJsonInfo(fileName))
        return matchFiles


    def getSingleFile(self, key, fileName):
        info = {}
        filePath = ENV.getPath(key, fileName=fileName)
        if os.path.exists(filePath):
            info = ENV.getJsonInfo(filePath)
        return info


################################################################################
################################################################################
