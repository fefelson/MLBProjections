import os
import sqlite3

from abc import ABCMeta, abstractmethod
from pprint import pprint

################################################################################
################################################################################


createTableCmd = "CREATE TABLE {0[tableName]} ( {0[tableCmd]} )"
insertCmd = "INSERT INTO {0[tableName]} {0[colCmd]} VALUES( {0[qMarks]} )"
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
        if not self.fetchOne(checkTableCmd):
            for table in self.getTableList():
                self.executeCmd(createTableCmd.format(table))
                if table.get("index", None):
                    indexCmd = "CREATE INDEX idx_{0[name]} ON {0[tableName]} (" + table["index"] + ")"
                    self.executeCmd(indexCmd.format({"name":table["tableName"], "tableName":table["tableName"]}))
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


    def insert(self, table, values, cols=[]):
        colCmd = ""+", ".join([col for col in cols])
        qMarks = ",".join(["?" for col in table["tableCols"]])
        self.executeCmd(insertCmd.format({"qMarks": qMarks, "tableName": table["tableName"], "colCmd": colCmd}), values)



################################################################################
################################################################################
