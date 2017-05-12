import pymysql
import numpy as np

def getData(query, columns):
    mydb = pymysql.connect(host='localhost',
                user='root',
                passwd='28031994Alex',
                db='knowledge')
    cursor = mydb.cursor()
    cursor.execute(query)
    rawData = cursor.fetchall()

    #close the connection to the database.
    mydb.commit()
    cursor.close()
    return convertDBrowsToArray(rawData, columns)

def convertDBrowsToArray(data, columns):
    testData = np.zeros((len(data), columns))
    for i, row in enumerate(data):
        for j, col in enumerate(row):
            testData[i, j] = col

    return testData