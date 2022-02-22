from bs4 import BeautifulSoup
import requests
import sys
sys.path.append('.')
import openpyxl

def crowlmv():
    count=1 #영화 인덱스
    wb=openpyxl.Workbook() #workbook 활성화
    sheet = wb.active #sheet 활성화

    url='https://movie.naver.com/movie/sdb/browsing/bmovie.naver?genre=' #영화 정보를 가져올 주소. genre 뒤엔 장르의 번호가 들어가게됨
    raw = requests.get(url) #request를 보내서 raw정보를 가져옴.
    html = BeautifulSoup(raw.text,'html.parser')#raw정보를 html로 변환

    n = html.select('#old_content td.next') #html에서 next(다음)버튼을 찾아감
    j=1 #j는 페이지 번호 index
    while n != []: #next버튼이 없다면 마지막페이지. 즉 마지막 페이지까지 검색을 실행함.
        url0=url+'&page='+str(j) #기존의 url에 page정보를 추가.
        raw0 = requests.get(url0) #url0로 request를 보내 raw정보를 가져옴
        html0 = BeautifulSoup(raw0.text,'html.parser') 
        n = html0.select('#old_content td.next') #10번째 줄처럼 next정보를 읽어옴
        titles = html0.select('#old_content > ul > li') #title정보가 들어있는 list를 찾아감
        for title in titles: #list의 갯수만큼 실행
            lik = title.select_one('a')['href'] #각 영화 세부 정보 사이트로 접근하기위한 a-href링크를 얻어옴
            al='' #actor_list
            count+=1
            lk=('https://movie.naver.com/'+lik).replace('basic','detail') #각 영화의 세부정보로 접근하기위한 링크 변수. basic정보가아닌 detail로 변경
            raw1 = requests.get(lk)
            html1 = BeautifulSoup(raw1.text,'html.parser')
            tit = html1.select_one('#content > div.article > div.mv_info_area > div.mv_info > h3 > a') #영화의 세부정보 html에서 title을 가져옴
            if tit is None: #title,genre,director,actor변수가 없을 경우 예외처리
                t = 'no_info'
            else:
                t = tit.get_text()
                t = t.replace('\'','\\\'') #escape문자 처리
            g = html1.select_one('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p > span:nth-child(1) > a')
            if g is None:
                gen = 'no_info'
            else:
                gen = g.get_text()
                gen = gen.replace('\'','\\\'')
            d  = html1.select_one('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(4) > p > a')
            if d is None:
                director = 'no_info'
            else:
                director = d.get_text()
                director = director.replace('\'','\\\'')
            ul1 = html1.select_one('#content > div.article > div.section_group.section_group_frst > div.obj_section.noline > div > div.lst_people_area.height100 > ul')
            if ul1 is None:
                al='no_info'
            else:
                for k in range(1,4): #배우는 4명까지 검색하도록 실행.
                    tag = 'ul > li:nth-child('+str(k)+') > div > a'
                    actor = ul1.select_one(tag)
                    if actor is None:
                        break
                    else:
                        al+=actor.get_text()+', '
                al = al.replace('\'','\\\'')
            try: #가져온 정보를 sheet에 저장
                sheet.append([count,t,gen,director,al])
            except: #에러 발생시 error문구를 기입
                sheet.cell(row=count,column=1).value='error'
        j+=1 #다음페이지로 전환
    wb.save('C:/dev/3rd_test/movie_info.xlsx') #정보를 저장
crowlmv()