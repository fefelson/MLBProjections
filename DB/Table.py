from itertools import chain

################################################################################
################################################################################

indexCmd = "CREATE INDEX idx_{} ON {} ({})"



################################################################################
################################################################################


class Table:

    def __init__(self, tableName):

        self.tableName = tableName
        self.pk = None
        self.tableCols = []
        self.tableCmds = []
        self.fk = []
        self.indexes = []


    def getName(self):
        return self.tableName


    def getPk(self):
        return self.pk


    def createIndexCmds(self):
        return [indexCmd.format(title,self.tableName,index) for title, index in self.indexes]


    def createTableCmd(self):
        colCmds = ", ".join(chain(self.tableCmds,self.fk))
        return "CREATE TABLE {} ( {} )".format(self.tableName, colCmds)


    def addPk(self, item, itemType):
        self.pk = item
        self.tableCmds.append("{} {} PRIMARY KEY".format(item, itemType))


    def getCols(self):
        return [self.pk, *self.tableCols]


    def addCol(self, item, itemType, allowNull=False):
        nullValue = "NOT NULL" if not allowNull else ""
        self.tableCols.append(item)
        self.tableCmds.append("{} {} {}".format(item, itemType, nullValue))


    def addFk(self, item, table, key):
        self.tableCols.append(item)
        self.tableCmds.append("{} INT NOT NULL".format(item))
        self.fk.append("FOREIGN KEY ({}) REFERENCES {} ({})".format(item, table, key))


    def addIndex(self, name, sequence):
        self.indexes.append((name, sequence))
