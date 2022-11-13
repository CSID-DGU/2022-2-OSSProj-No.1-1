import pymysql



class Database(object):

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
        sql = "UPDATE users SET user_coin= %s WHERE user_id=%s"
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
    
    def getScores():
        curs=self.score_db.cursor()
        sql='SELECT * FROM single_score ORDER BY score DESC'
        curs.execute(sql)
        data=curs.fetchall()
        return data
        curs.close()
    # 
    def setScore(self,hiScores,user_id,score):
        curs=self.score_db.cursor()
        sql="SELECT * FROM single_score WHERE user_id=%s"
        curs.execute(sql,user_id)
        data=curs.fetchone()
        
        if data: # 이미 user 점수가 랭킹 보드에 있을 경우 -> 기존 점수 vs 새 점수
            if data['score']>score:
                curs.close()
                return 
            else:
                sql='UPDATE single_score SET score=%s WHERE user_id=%s' #대체하기
                curs.execute(sql,(score,user_id))
                self.score_db.commit()
                #curs.close()
        else:
            if len(hiScores) >= self.numScores: # 랭킹보드가 꽉 찼으면
                lowScoreid = hiScores[-1][0]
                lowScore = hiScores[-1][1]
                if lowScore <score:
                    sql="DELETE FROM single_score WHERE (user_id = %s AND score = %s)"
                    curs.execute(sql,(lowScoreid, lowScore))
                    self.score_db.commit()
                    sql="INSERT INTO single_score VALUES (%s,%s)"
                    curs.execute(sql,(user_id, score))
                    self.score_db.commit()
            else :
                sql="INSERT INTO single_score VALUES (%s,%s)"
                curs.execute(sql,(user_id, score))
                self.score_db.commit()

        curs.close()


                    


        
           
        
 
   

    


