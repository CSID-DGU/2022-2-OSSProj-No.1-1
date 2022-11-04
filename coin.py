import os
import pymysql
import sqlite3


main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')


class CoinData(object):
    path = os.path.join(data_dir, 'coins.db')

    def __init__(self):
        self.coin_db = pymysql.connect( # 데이터베이스와 연동
            user='root',
            password='ossproj1',
            host='no-1-db.cfzoiqvsstra.ap-northeast-2.rds.amazonaws.com',
            db='No_1_mysql',
            charset='utf8'
        )

    # 게임 종료 후 coin값 update시키기
    def setCoins(self,user_id,coin):
        curs = self.coin_db.cursor(pymysql.cursors.DictCursor)
        sql="UPDATE users SET user_coin= %s WHERE user_id=%s"
        curs.execute(sql,(coin,user_id))
        self.coin_db.commit()
        curs.close()
        
    # 현재 갖고 있는 coin값 반환 
    def load(self,user_id):
        curs = self.coin_db.cursor(pymysql.cursors.DictCursor)
        sql="SELECT user_coin FROM users WHERE user_id=%s"
        curs.execute(sql,user_id)
        data=curs.fetchone()
        curs.close()
        coins=data['user_coin']
        return coins

    # price만큼 구입하고, users (user_coin 업데이트), user_ship(ship_id 업데이트)  
    def buy(self,user_id,ship_id):
        curs = self.coin_db.cursor(pymysql.cursors.DictCursor)
        sql="SELECT ship_price FROM ship_data WHERE ship_id=%s"
        curs.execute(sql,ship_id)
        data=curs.fetchone()
        price=data['ship_price']
        sql="UPDATE users SET user_coin=user_coin-price WHERE user_id=%s"
        curs.execute(sql,user_id)
        sql="UPDATE user_ship SET ship_id=%s WHERE user_id=%s"
        curs.execute(sql,user_id)
        curs.close()
        

# 상점모드 구현
#user_ship (user_id,ship_id)
#ship_data(ship_id,ship_design,ship_price)
#unlock이면 어쩌자는건데.. -> main파일에서 unlock일때 어떻게 디자인 적용되는지ㅠㅠ보기
#sprites.py에서 Ship() ship 이미지, ship 기능등등 정의하는 듯
class ShipData(object) :
    path = os.path.join(data_dir, 'ship.db')

    def load_unlock(id) :
        conn = sqlite3.connect(ShipData.path)
        c = conn.cursor()
        c.execute("CREATE TABLE if not exists ship_status (id integer, unlock integer)")
        c.execute("SELECT COUNT(*) FROM ship_status")
        l = c.fetchall()
        if l[0][0] == 0 :
            c.execute("INSERT INTO ship_status VALUES(1, 1)")
            c.execute("INSERT INTO ship_status VALUES(2, 0)")
            c.execute("INSERT INTO ship_status VALUES(3, 0)")
            c.execute("INSERT INTO ship_status VALUES(4, 0)")
        c.fetchall()
        c.execute("SELECT unlock FROM ship_status WHERE id = ? ", (id, ))
        unlock = c.fetchone()[0]
        conn.commit()
        conn.close()
        if unlock == 0 : return False
        elif unlock == 1 : return True
    
    def unlock(id) :
        conn = sqlite3.connect(ShipData.path)
        c = conn.cursor()
        c.execute("UPDATE ship_status SET unlock = 1 WHERE id = ? ", (id, ))
        conn.commit()
        conn.close()
