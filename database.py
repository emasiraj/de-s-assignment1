import mysql.connector
import pandas as pd
import pdb

cnx = mysql.connector.connect(user='root', password='root',
                              host='127.0.0.1',
                              database='bigdata_assignment1',
                              auth_plugin='mysql_native_password')
cursor = cnx.cursor()

cursor.callproc('GetReviews')
queryResult = cursor.stored_results()
dataSetList = [item.fetchall() for item in queryResult]

dataSetListDF = []
for i in dataSetList[0]:
    positiveList = []
    negativeList = []
    positiveList.extend([i[0], i[2], 'positive'])
    negativeList.extend([i[0], i[1], 'negative'])

    if positiveList[1] != 'No Positive':
        dataSetListDF.append(positiveList)

    if negativeList[1] != 'No Negative':
        dataSetListDF.append(negativeList)



reviewDataframe = pd.DataFrame(dataSetListDF,
                               columns=['Review', 'Review_Consensus'])
reviewDataframe = reviewDataframe.iloc[:5000]
reviewDataframe.to_csv('reviewDataframe.csv')

cnx.close()

