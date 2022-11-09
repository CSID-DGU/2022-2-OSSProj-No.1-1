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


    def compare_data(self, id_text, pw_text): # 데이터베이스의 아이디와 비밀번호 비교교
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


    


    


