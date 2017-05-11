import pymysql
import csv

mydb = pymysql.connect(host='localhost',
            user='root',
            passwd='28031994Alex',
            db='knowledge')
cursor = mydb.cursor()

csv_data = csv.reader(file('C:/BookTest.csv'))
for row in csv_data:
    print row
    cursor.execute('INSERT INTO infection (Date, newCasesAdult, newCasesChild, \
                newCasesAllPeople, newCasesAIDSAdult, newCasesAIDSChild, newCasesAIDSAllPeople, newCasesDeathAdult, newCasesDeathChild, \
                newCasesDeathAllPeople, allCasesHIVAdult, allCasesHIVChild, allCasesHIVAllPeople, allCasesAIDSAdult, allCasesAIDSChild, \
                allCasesAIDSAllPeople, allCasesDeathAdult, allCasesDeathChild, allCasesDeathAllPeople, newCasesHIVSIN, allCasesAIDSSIN, allPeople, SINpercent) \
                VALUES(%s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',row)

rawData = cursor.fetchall()
#close the connection to the database.
mydb.commit()
cursor.close()
