import csv
import sys
import pymysql
import numpy as np
from PyQt4 import QtGui
from PyQt4.QtCore import Qt

class Table(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Table, self).__init__(parent)
        layout = QtGui.QGridLayout()
        self.table = QtGui.QTableWidget()
        layout.addWidget(self.table, 1, 0)

        self.fillQTable(self.table)
        self.setLayout(layout)

    def getData(self):
        mydb = pymysql.connect(host='localhost',
            user='root',
            passwd='28031994Alex',
            db='knowledge')
        cursor = mydb.cursor()

        csv_data = csv.reader(file('C:/testDB.csv'))
        # for row in csv_data:
        #     print row
            # cursor.execute('INSERT INTO infection (Date, newCasesAdult, newCasesChild, \
            #     newCasesSIN, newCasesAIDSAdult, newCasesAIDSChild, newCasesAIDSSIN, newCasesDeathAdult, newCasesDeathChild, newCasesDeathSIN) \
            #     VALUES(%s, %s, %s, %s, %s,%s, %s, %s, %s, %s)',row)
        cursor.execute('Select newCasesAdult, newCasesChild, newCasesSIN  from infection')
        rawData = cursor.fetchall()
        #close the connection to the database.
        mydb.commit()
        cursor.close()
        return rawData

    def fillQTable(self, table):
        #data = [('1','2','3','4'),('5','6','7','8')] #this is from database
        data = self.getData()
        print data
        rowCount = len(data)
        colCount = 3
        table.setRowCount(rowCount)
        table.setColumnCount(colCount)

        testData = np.zeros((rowCount,3))
        for i, row in enumerate(data):
            for j, col in enumerate(row):
                testData[i,j] = col

        print testData

        for i, row in enumerate(data):
            for j, col in enumerate(row):
                item = QtGui.QTableWidgetItem()
                item.setData(Qt.EditRole, col)
                table.setItem(i, j, item)

app = QtGui.QApplication(sys.argv)
t = Table()
t.show()
sys.exit(app.exec_())