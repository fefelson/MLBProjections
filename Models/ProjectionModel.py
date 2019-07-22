import copy
import datetime
import json
import os
import queue
from threading import Thread
from urllib.error import HTTPError

import MLBProjections.MLBProjections.Models.Matchup as MA
import MLBProjections.MLBProjections.DB.MLB as DB
from MLBProjections.MLBProjections.Managers.DownloadManager import DownloadManager
from MLBProjections.MLBProjections.Managers.DatabaseManager import DatabaseManager
from MLBProjections.MLBProjections.Managers.GameManager import GameManager
from MLBProjections.MLBProjections.Managers.CollectionManager import CollectionManager

from pprint import pprint

################################################################################
################################################################################





################################################################################
################################################################################


class MLBProjections:

    def __init__(self, gameDate=None):

        if not gameDate:
            gameDate = datetime.date.today()

        self.gameDate = gameDate
        self.downloadManager = DownloadManager()
        self.databaseManager = DatabaseManager(DB.MLBDatabase())
        self.gameManager = GameManager(self)
        self.collectionManager = CollectionManager()
        self.matchups = {}
        self.runUpdate()
        self.createMatchups()


    def gameDBExists(self, index):
        return self.databaseManager.gameDBExists(index)


    def newGameDB(self, matchup):
        return self.databaseManager.cloneDB(matchup)


    def createMatchups(self):
        for info in self._matchups():
            matchup = MA.Matchup(info)
            matchup.setLeague(self.databaseManager.getLeague(info["home"]["teamId"]))
            for homeAway in ("home", "away"):
                matchup.setTeamInfo(homeAway, "info", self._infoFile("team", info[homeAway]["teamId"]))
                try:
                    # Sometimes a starter isn't set
                    # The playerId is -1
                    # Looking for playerId -1 in Yahoo creates HTTPError 301
                    matchup.setTeamInfo(homeAway, "starter", self._infoFile("player", info[homeAway]["starter"]))
                except HTTPError:
                    pass
                # TODO: date check in downloads
                matchup.setTeamInfo(homeAway, "roster", self._infoFile("roster", info[homeAway]["teamId"]))
                matchup.setTeamInfo(homeAway, "lineup", self.databaseManager.getRecentLineup(info[homeAway]["teamId"]))
            #####
            for playerId in matchup.getPlayerIds():
                if not self.databaseManager.findPlayer(playerId):
                    self.databaseManager.addPlayerToDB(self._infoFile("player", playerId))
            gameId = matchup.getGameId()
            self.matchups[gameId] = matchup


    def _infoFile(self, key, fileName, force=False):
        # Collect matchup info from downladed matchupFiles
        infoFile = self.collectionManager.getSingleFile(key, fileName)
        # If they don't exist or a force download is requested
        if force or not infoFile:
            self.downloadManager.getFiles(key, fileName, force)
            # Try again, doing Recursivly seemed unnecesary
            infoFile = self.collectionManager.getSingleFile(key, fileName)
        return infoFile


    def _matchups(self, force=False):
        # Collect matchup info from downladed matchupFiles
        matchFiles = self.collectionManager.getMatchupFiles(self.gameDate)
        # If they don't exist or a force download is requested
        if force or not matchFiles:
            self.downloadManager.getMatchups(self.gameDate, force)
            # Try again, doing Recursivly seemed unnecesary
            matchFiles = self.collectionManager.getMatchupFiles(self.gameDate)
        return matchFiles


    def getMatchups(self, key=None):
        if key:
            return self.matchups.get(key, None)
        else:
            return self.matchups


    def runUpdate(self):
        self.downloadManager.update()
        self.databaseManager.update()
