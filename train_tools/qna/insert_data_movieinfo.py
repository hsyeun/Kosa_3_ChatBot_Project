from wsgiref.validate import WSGIWarning
import pymysql
import openpyxl
import os

from Config.DatabaseConfig import * # DB 접속 정보 불러오기


# 학습 데이터 초기화
def all_clear_train_data(db):
    # 기존 학습 데이터 삭제
    sql = '''
            delete from movie_data
        '''
    with db.cursor() as cursor:
        cursor.execute(sql)

    # auto increment 초기화
    sql = '''
    ALTER TABLE movie_data AUTO_INCREMENT=1
    '''
    with db.cursor() as cursor:
        cursor.execute(sql)


# db에 데이터 저장
def insert_data(db, xls_row):
    movie_title, genre, director, actor = xls_row

    sql = '''
        INSERT movie_data(movie_title, genre, director, actor) 
        values(
         '%s', '%s', '%s', '%s'
        )
    ''' % (movie_title.value, genre.value, director.value, actor.value)

    # 엑셀에서 불러온 cell에 데이터가 없는 경우, null 로 치환
    sql = sql.replace("'None'", "null")

    with db.cursor() as cursor:
        cursor.execute(sql)
        # print('{} 저장'.format(query.value))
        db.commit()


path = 'C:/dev/Project_chatbot/Kosa_3_ChatBot_Project/train_tools/qna/movie_info'
db = None
try:
    db = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        passwd=DB_PASSWORD,
        db=DB_NAME,
        charset='utf8'
    )

    # 기존 학습 데이터 초기화
    all_clear_train_data(db)


    # 엑셀 파일 여러개 db에 저장하기
    files = os.listdir(path)
    for file in files:
        wb = openpyxl.load_workbook(path + '/' + file)
        ws = wb.active

        for row in ws.iter_rows(min_row=2, min_col=2):  # 첫번째 열(번호)은 불러오지 않음
            # 데이터 저장
            insert_data(db, row)

    wb.close()
    print('insert 성공')

except Exception as e:
    print(e)

finally:
    if db is not None:
        db.close()

