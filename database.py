import pymysql
import sqlite3
import os

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')


class Database(object):
    path = os.path.join(data_dir, 'hiScores.db')
    numScores = 15

    @staticmethod
    def getSound(music=False): # 사운드를 데이터베이스에서 불러오는 함수
        conn = sqlite3.connect(Database.path)

        c = conn.cursor()
        if music:
            c.execute("CREATE TABLE if not exists music (setting integer)")
            c.execute("SELECT * FROM music")
        else:
            c.execute("CREATE TABLE if not exists sound (setting integer)")
            c.execute("SELECT * FROM sound")
        setting = c.fetchall()
        conn.close()
        return bool(setting[0][0]) if len(setting) > 0 else False

    @staticmethod
    def setSound(setting, music=False): # 사운드를 설정하는 함수
        conn = sqlite3.connect(Database.path)

        c = conn.cursor()
        if music:
            c.execute("DELETE FROM music")
            c.execute("INSERT INTO music VALUES (?)", (setting,))
        else:
            c.execute("DELETE FROM sound")
            c.execute("INSERT INTO sound VALUES (?)", (setting,))
        conn.commit()
        conn.close()

    @staticmethod
    def getScores(): # 점수를 데이터베이스에서 불러오는 함수
        conn = pymysql.connect(host='localhost', user='root',
                            password='0000', db='hiScores', charset='utf8')
        c = conn.cursor()
        c.execute('''CREATE TABLE if not exists scores
                     (name text, score integer, accuracy real)''')
        c.execute("SELECT * FROM scores ORDER BY score DESC")
        hiScores = c.fetchall()
        conn.close()
        return hiScores

    @staticmethod
    def setScore(hiScores, entry): # 점수를 데이터베이스에 저장하는 함수
        conn = pymysql.connect(host='localhost', user='root',
                               password='00000000', db='hiScores', charset='utf8')
        c = conn.cursor()
        if len(hiScores) == Database.numScores:
            lowScoreName = hiScores[-1][0]
            lowScore = hiScores[-1][1]
            c.execute("DELETE FROM scores WHERE (name = %s AND score = %s)",
                      (lowScoreName, lowScore))
        c.execute("INSERT INTO scores VALUES (%s,%s,%s)", entry)
        conn.commit()
        conn.close()


    


