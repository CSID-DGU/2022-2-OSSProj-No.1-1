import pymysql
import sqlite3
import bcrypt
import pygame
import os

#pygame.mixer.init()
main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')
#커서는 한 번만 부르..
class Database(object):
    path = os.path.join(data_dir, 'hiScores.db')
    def __init__(self):
        self.score_db = pymysql.connect( # 데이터베이스와 연동
            user='root',
            password='ossproj1',
            host='no-1-db.cfzoiqvsstra.ap-northeast-2.rds.amazonaws.com',
            db='No_1_mysql',
            charset='utf8'
        )
        self.numScores=10
        

    def id_not_exists(self,input_id): # 아이디가 데이터베이스에 존재하는지 확인
        curs = self.score_db.cursor(pymysql.cursors.DictCursor) # cursor : sql문을 실행할 수 있는 작업환경을 제공하는 객체
        sql = "SELECT * FROM users WHERE user_id=%s" # sql문 정의
        curs.execute(sql, input_id) # sql문 실행 
        data = curs.fetchone() # 해당 줄만 읽음 
        curs.close()
        if data:
            return False
        else:
            return True


    def compare_data(self, id_text, pw_text): # 데이터베이스의 아이디와 비밀번호 비교
       # 불러 오기
        input_password=pw_text.encode('utf-8') # 입력비번 -> bytes형으로 변환
        curs = self.score_db.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * FROM users WHERE user_id=%s"
        curs.execute(sql,id_text)
        data = curs.fetchone()
        curs.close()
        check_password=bcrypt.checkpw(input_password,data['user_password'].encode('utf-8')) 

        return check_password


    def add_id_data(self,user_id): # 아이디 추가
        #추가하기
        curs = self.score_db.cursor()
        sql = "INSERT INTO users (user_id) VALUES (%s)"
        curs.execute(sql, user_id)
        self.score_db.commit()  #서버로 추가 사항 보내기
        curs.close()


    def add_password_data(self,user_password,user_id): # 비밀번호 추가
        # 회원가입시 초기 coin값은 0으로 설정
        #추가하기
        initial_coin=0
        new_salt=bcrypt.gensalt() 
        new_password=user_password.encode('utf-8') # 입력받은 비번을 bytes형으로 바꿔줌 
        hashed_password=bcrypt.hashpw(new_password,new_salt) # hashing된 비밀번호
        decode_hash_pw=hashed_password.decode('utf-8') # 데이터베이스에 저장하기 위해 bytes-> string형으로 바꿈 
    
        curs = self.score_db.cursor()
        # pw 저장
        sql = "UPDATE users SET user_password= %s WHERE user_id=%s"
        curs.execute(sql,(decode_hash_pw,user_id))
        self.score_db.commit()  #commit으로 데이터베이스에 반영
        # coin initialize
        curs = self.score_db.cursor()
        sql = "UPDATE user_info SET user_coin= %s WHERE user_id=%s"
        curs.execute(sql, (initial_coin, user_id))
        self.score_db.commit()
        curs.close()


    
    # 게임 종료 시 데이터베이스에 점수 추가
    def add_score_data(self,game_mode,user_id,score):
        curs=self.score_db.cursor()
        if game_mode == 'single':
            sql='INSERT INTO single_score(user_id,score) VALUES (%s,%s)'
        elif game_mode =='two':
            sql='INSERT INTO two_score(user_id,score) VALUES (%s,%s)'
        curs.execute(sql,(user_id,score))
        self.score_db.commit()
        curs.close()

    # 상위 10개 점수 불러오기
    
    def getScores(self):

        curs=self.score_db.cursor()
        sql='SELECT * FROM single_score ORDER BY user_score DESC'
        curs.execute(sql)
        data=curs.fetchall()
        if len(data)>self.numScores:
            data=[data[i] for i in range(self.numScores)]
        
        return data
        curs.close()
    # 
    
    def setScore(self,user_id,score): # 기존에 저장되어 있던 점수랑 비교해야될듯 user_id가 pk라서 같은 아이디가 중복 저장되지x
        # data가 null일때랑 아닐때
        curs=self.score_db.cursor()
        sql="SELECT * FROM single_score WHERE user_id=%s"
        curs.execute(sql,user_id)
        data=curs.fetchone()
        if data:
            if score > data[1]:
                curs=self.score_db.cursor()
                sql="UPDATE single_score SET user_score=%s WHERE user_id=%s"
                curs.execute(sql,(score,user_id))
                self.score_db.commit()
            else:
                curs.close()
                return
        else:
            curs=self.score_db.cursor()
            sql = "INSERT INTO single_score (user_id, user_score) VALUES (%s, %s)"
            curs.execute(sql,(user_id,score))
            self.score_db.commit()
            

        curs.close()
    # extreme score
    def getScores_extreme(self):

        curs=self.score_db.cursor()
        sql='SELECT * FROM extreme_score ORDER BY user_score DESC'
        curs.execute(sql)
        data=curs.fetchall()
        if len(data)>self.numScores:
            data=[data[i] for i in range(self.numScores)]
        
        return data
        curs.close()
    # 
    
    def setScore_extreme(self,user_id,score): # 기존에 저장되어 있던 점수랑 비교해야될듯 user_id가 pk라서 같은 아이디가 중복 저장되지x
        # data가 null일때랑 아닐때
        curs=self.score_db.cursor()
        sql="SELECT * FROM extreme_score WHERE user_id=%s"
        curs.execute(sql,user_id)
        data=curs.fetchone()
        if data:
            if score > data[1]:
                curs=self.score_db.cursor()
                sql="UPDATE extreme_score SET user_score=%s WHERE user_id=%s"
                curs.execute(sql,(score,user_id))
                self.score_db.commit()
            else:
                curs.close()
                return
        else:
            curs=self.score_db.cursor()
            sql = "INSERT INTO extreme_score (user_id, user_score) VALUES (%s, %s)"
            curs.execute(sql,(user_id,score))
            self.score_db.commit()
            

        curs.close()


    def getSound(music=False):
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
    def setSound(setting, music=False):
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

    def setCoins(self,user_id,score):
        newcoins=0
        curs=self.score_db.cursor()
        sql="SELECT * FROM user_info WHERE user_id=%s"
        curs.execute(sql,user_id)
        data=curs.fetchone()
        newcoins=data[1]+score
        sql="UPDATE user_info SET user_coin=%s WHERE user_id=%s"
        curs.execute(sql,(newcoins,user_id))
        self.score_db.commit()

        curs.close()


    def load_coin(self,user_id):
        curs=self.score_db.cursor()
        sql="SELECT * FROM user_info where user_id=%s"
        curs.execute(sql,user_id)
        data=curs.fetchone()
        curs.close()
        return data[1]
    
    def buy_char(self,user_id,price):
        curs=self.score_db.cursor()
        sql="select * from user_info where user_id=%s"
        curs.execute(sql,user_id)
        data=curs.fetchone()
        result=data[1]-price
        
        #바뀐 코인으로 업데이트
        sql="update user_info set user_coin=%s where user_id=%s"
        curs.execute(sql,(result,user_id))
        self.score_db.commit()

        
        curs.close()
        return result
        
    
        
    def update_char_data(self,user_char,user_id): # 캐릭터 추가/변경
        curs = self.score_db.cursor()
        sql="SELECT * FROM user_info WHERE user_id=%s"
        curs.execute(sql,user_id)
        data=curs.fetchone()
        if data: # 이미 등록한 유저라면
            sql="UPDATE user_info SET user_character=%s WHERE user_id=%s"
            print("user_char>>>>>>>>> : ",user_char)
            curs.execute(sql,(user_char,user_id))
            self.score_db.commit()
        else:
            sql="INSERT INTO user_info(user_id,user_character) VALUES (%s,%s)"
            print("user_char>>>>>>>>> : ",user_char)
            curs.execute(sql,(user_id,user_char))
            self.score_db.commit()
        
        curs.close()

    def load_char_data(self,user_id): #캐릭터정보 불러오기
        curs = self.score_db.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * FROM user_info WHERE user_id=%s"
        curs.execute(sql, user_id)
        data = curs.fetchone()  # 리스트 안에 딕셔너리가 있는 형태
        curs.close()
        #print("ID : ",data['user_id'])
        
        #print("CHAR : ",data['user_character'])
        return data['user_character']

    

    def load_shipprice(self,name):
        curs=self.score_db.cursor(pymysql.cursors.DictCursor)
        sql="SELECT * FROM ship WHERE name=%s"
        curs.execute(sql,name)
        data=curs.fetchone()
        curs.close()

        return data['price']
        
    def update_char_have(self,user_id,type): #char_have 테이블 업데이트
        curs=self.score_db.cursor()
        sql='select * from char_have where user_id=%s'
        curs.execute(sql,user_id)
        data=curs.fetchone()
        if data: # update함
            sql='update char_have set {0}=1 where user_id=%s'.format(type)
            curs.execute(sql,user_id)
            self.score_db.commit()
            curs.close()
            
        else: # 처음일경우
            sql='insert into char_have(user_id,{0}) values(%s,1)'.format(type)
            curs.execute(sql,user_id)
            self.score_db.commit()
            curs.close()

    def check_char_have(self,user_id,ship_type): # 있으면 1
        curs=self.score_db.cursor(pymysql.cursors.DictCursor)
        sql='select * from char_have where user_id=%s'
        curs.execute(sql,user_id)
        data=curs.fetchone()
        data=data[ship_type]
        return data
        




        

                    


        
           
        

        

                    


        
           
        
 
   

    