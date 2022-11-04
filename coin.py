import os
import sqlite3


main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')


class CoinData(object):
    path = os.path.join(data_dir, 'coins.db')

    def setCoins(coin):
        conn = sqlite3.connect(CoinData.path)
        c = conn.cursor()
        c.execute("UPDATE safe SET balance = ? WHERE id = 1", (coin,))
        conn.commit()
        conn.close()

    def load():
        conn = sqlite3.connect(CoinData.path)
        c = conn.cursor()
        c.execute("CREATE TABLE if not exists safe (id integer, balance integer DEFAULT 0)")
        c.execute("SELECT COUNT(*) FROM safe")
        l = c.fetchall()
        if l[0][0] == 0 :
            c.execute("INSERT INTO safe VALUES (1, 0)")
        c.fetchall()
        c.execute("SELECT balance FROM safe WHERE id = 1")
        coins = c.fetchone()[0]
        conn.commit()
        conn.close()
        return coins
        
    def buy(price) :
        conn = sqlite3.connect(CoinData.path)
        c = conn.cursor()
        c.execute("SELECT balance FROM safe WHERE id = 1")
        balance = c.fetchone()[0]
        balance -= price
        CoinData.setCoins(balance)
        if price == 30 : id = 2
        elif price == 50 : id = 3
        elif price == 100 : id = 4
        ShipData.unlock(id)
        conn.close()

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
