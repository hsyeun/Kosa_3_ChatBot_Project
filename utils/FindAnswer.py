class FindAnswer:
    def __init__(self, db):
        self.db = db

    # 검색 쿼리 생성
    def _make_query(self, intent_name, ner_tags):
        sql = "select * from chatbot_qna_data"
        if intent_name != None and ner_tags == None:
            sql = sql + " where intent='{}' ".format(intent_name)

        elif intent_name != None and ner_tags != None:
            where = ' where intent="%s" ' % intent_name
            if (len(ner_tags) > 0):
                where += 'and ('
                for ne in ner_tags:
                    where += " ner like '%{}%' or ".format(ne)
                where = where[:-3] + ')'
            sql = sql + where

        # 동일한 답변이 2개 이상인 경우, 랜덤으로 선택
        sql = sql + " order by rand() limit 1"
        print(sql)
        return sql

    # 답변 검색
    def search(self, intent_name, ner_tags):
        # 의도명, 개체명으로 답변 검색
        sql = self._make_query(intent_name, ner_tags)
        answer = self.db.select_one(sql)

        # 검색되는 답변이 없으면 의도명만 검색
        if answer is None:
            sql = self._make_query(intent_name, None)
            answer = self.db.select_one(sql)
        return answer['answer']

    # NER 태그를 실제 입력된 단어로 변환
    def tag_to_word(self, ner_predicts, answer):
        for word, tag in ner_predicts:

            # 변환해야하는 태그가 있는 경우 추가
            if tag == 'B_MWK' or tag == 'B_THR' or tag == 'B_LOC' or tag == 'B_GEN' or tag == 'B_TER':
                answer = answer.replace(tag, word)
   
        answer = answer.replace('{', '')
        answer = answer.replace('}', '')
        return answer
    
    def find_mvw_info(self, mvw):
        sql = f"select * from movie_data where movie_title='{mvw}'"
        print(sql)
        ans = self.db.select_one(sql)
        if ans is None:
            return '찾으시는 영화정보가 없습니다.'
        else:
            return [ans['movie_title'],ans['genre'],ans['director'],ans['actor']]

    def find_thr_info(self,thr):
        loc_do = input('찾으시는 지역(도)을 알려주세요.\n>>>')
        loc_si = input('찾으시는 지역(시)을 알려주세요.\n>>>')
        if thr =='영화관':
            sql_do = f"select * from theater_data where do='{loc_do}' and si='{loc_si}'"
        else:
            sql_do = f"select * from theater_data where do='{loc_do}' and si='{loc_si}'"
        print(sql_do)
        thr_list = self.db.select_all(sql_do)
        if thr_list is None:
            print('검색결과가 없습니다.')
        else:
            print('찾으시는 영화관 정보입니다.\n====================')
            result = []
            for i in thr_list:
                print(i['theater_name'])
