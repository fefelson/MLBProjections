import os
import sqlite3

from abc import ABCMeta, abstractmethod
from pprint import pprint

################################################################################
################################################################################



insertCmd = "INSERT INTO {0[tableName]} VALUES( {0[qMarks]} )"
checkTableCmd = "SELECT * FROM sqlite_master"


################################################################################
################################################################################


class Database(metaclass=ABCMeta):
    """
        INPUTS ARE NOT VALIDATED HERE
    """

    def __init__(self, filePath):

        self.filePath = filePath

        self.conn = None
        self.curs = None
        self.isOpen = False


    def openDB(self):
        if not os.path.exists("/".join(self.filePath.split("/")[:-1])):
            os.makedirs("/".join(self.filePath.split("/")[:-1]))
        self.conn = sqlite3.connect(self.filePath)
        self.curs = self.conn.cursor()

        # If there are no tables
        if not self.fetchOne(checkTableCmd):
            # Create tables
            for table in self.getTableList():
                self.executeCmd(table.createTableCmd())
                for indexCmd in table.createIndexCmds():
                    self.executeCmd(indexCmd)
            self.seed()
            self.commit()


    @abstractmethod
    def seed(self):
        pass


    def closeDB(self):
        self.conn.close()


    def commit(self):
        self.conn.commit()


    def executeCmd(self, cmd, values=[]):
        #TODO: catch errors here?

        self.curs.execute(cmd, values)


    def fetchOne(self, cmd, values=[]):
        self.executeCmd(cmd, values)
        return self.curs.fetchone()


    def fetchAll(self, cmd, values=[]):
        self.executeCmd(cmd, values)
        return self.curs.fetchall()


    def insert(self, table, *, info=None, values=None):
        if not info and not values:
            raise AssertionError("info dict or values list/tuple must be provided")
        if not values:
            values = [info.get(key, None) for key in table.getCols()]
        qMarks = ",".join(["?" for col in table.getCols()])
        self.executeCmd(insertCmd.format({"qMarks": qMarks, "tableName": table.getName()}), values)


    def nextKey(self, table):
        keyCmd = "SELECT MAX({}) FROM {}".format(table.getPk(), table.getName())
        try:
            key = int(self.fetchOne(keyCmd)[0]) + 1
        except TypeError:
            key = 0
        return key


    def getKey(self, table, **kwargs):
        whereCmd = " AND ".join(["{}={}".format(key,value) for key, value in kwargs.items()])
        keyCmd = "SELECT {} FROM {} WHERE {}".format(table.getPk(), table.getName(), whereCmd)
        try:
            key = self.fetchOne(keyCmd)[0]
        except TypeError:
            key = self.nextKey(table)
            kwargs[table.getPk()] = key
            self.insert(table, info=kwargs)
        return key



################################################################################
################################################################################
