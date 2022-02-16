import pymysql
from config.DatabaseConfig import *

db = None
try:
    db = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        passwd=DB_PASSWORD,
        db=DB_NAME,
        charset='utf8'
    )

    # 테이블 생성 sql 정의
    # sql = '''
    #   CREATE TABLE IF NOT EXISTS `chatbot_qna_data` (
    #   `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    #   `intent` VARCHAR(45) NULL,
    #   `ner` VARCHAR(1024) NULL,
    #   `query` TEXT NULL,
    #   `answer` TEXT NOT NULL,
    #   PRIMARY KEY (`id`))
    # ENGINE = InnoDB DEFAULT CHARSET=utf8
    # '''

    # sql_mv = '''
    #   CREATE TABLE IF NOT EXISTS `movie_data` (
    #   `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    #   `intent` VARCHAR(45) NULL,
    #   `ner` VARCHAR(1024) NULL,
    #   `query` TEXT NULL,
    #   `answer` TEXT NOT NULL,
    #   PRIMARY KEY (`id`))
    # ENGINE = InnoDB DEFAULT CHARSET=utf8
    # '''

    sql_th = '''
      CREATE TABLE IF NOT EXISTS `theater_data` (
      `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
      `do` VARCHAR(10) NOT NULL,
      `si` VARCHAR(10) NOT NULL,
      `theater_name` TEXT NOT NULL,
      `address` TEXT NOT NULL,
      `tell` VARCHAR(15) NULL,
      PRIMARY KEY (`id`))
    ENGINE = InnoDB DEFAULT CHARSET=utf8
    '''

    # 테이블 생성
    with db.cursor() as cursor:
        cursor.execute(sql_th)

except Exception as e:
    print(e)

finally:
    if db is not None:
        db.close()

