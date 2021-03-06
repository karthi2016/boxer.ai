import cortipy
import os
import mysql.connector as msc
import time

# Init API client
apiKey = os.environ.get('CORTICAL_API_KEY')
client = cortipy.CorticalClient(apiKey)


MYSQL_GSJ_USER = 'root'
MYSQL_GSJ_PASSWORD = 'nycdsa1!'
MYSQL_GSJ_HOST = '173.194.225.231'
MYSQL_GSJ_DB = 'test'

config = {
   'user': 'root',
   'password': 'uLFZ2WoB',
   'host': '130.211.154.93',
   'database': 'test',
   'charset': 'utf8'
}

#Need to put this into an infinite loop
while 1:
    con = msc.connect(**config)
    cur = con.cursor()
    #con.autocommit(True)
    time.sleep(5)

    cur.execute("select siteurl, text from startups where cortical_io is null limit 1")
    test = cur.fetchall()

    siteurl = str(test[0][0])
    text = str(test[0][1])
    #programmingCategory = client.createClassification(categoryName, pos, neg)

    if(text == ''):
        continue

    termKeyWords = client.extractKeywords(text)
    termBitmap = client.getTextBitmap(text)['fingerprint']['positions']

    MySqlKeyWordDat = (','.join(termKeyWords), siteurl)
    MySqlBitMapDat = (str(termBitmap), siteurl)
    
    MySqlKeyWordDatQ = """UPDATE startups SET cortical_io_keywords = %s WHERE siteurl = %s"""
    MySqlBitMapDatQ = """UPDATE startups SET cortical_io = %s WHERE siteurl = %s"""

    #upload keywords and bitmap to database
    cur.execute(MySqlKeyWordDatQ, MySqlKeyWordDat)
    cur.execute(MySqlBitMapDatQ, MySqlBitMapDat)
    con.commit()

    con.close()

#bitmapTerms = client.bitmapToTerms(termBitmap['fingerprint'])






######  sample code bleow.
# Evaluate how close a new term is to the category.
#termBitmap = client.getBitmap("Python")['fingerprint']['positions']
#distances = client.compare(termBitmap, programmingCategory['positions'])
#print distances['euclideanDistance']

# Try a block of text.
#textBitmap = client.getTextBitmap("The Zen of Python >>>import this")['fingerprint']['positions']
#distances = client.compare(textBitmap, programmingCategory['positions'])
#print distances['euclideanDistance']
