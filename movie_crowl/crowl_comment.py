from bs4 import BeautifulSoup
import requests
import sys
sys.path.append('.')
import openpyxl

def crowlmv():
    count=1
    wb=openpyxl.Workbook()
    sheet = wb.active

    url='https://movie.naver.com/movie/sdb/browsing/bmovie.naver?genre='
    raw = requests.get(url)
    html = BeautifulSoup(raw.text,'html.parser')

    n = html.select('#old_content td.next')
    j=1
    while n != []:
        url0=url+'&page='+str(j)
        raw0 = requests.get(url0)
        html0 = BeautifulSoup(raw0.text,'html.parser')
        n = html0.select('#old_content td.next')
        titles = html0.select('#old_content > ul > li')
        for title in titles:
            lik = title.select_one('a')['href']
            al=''
            count+=1
            lk=('https://movie.naver.com/'+lik).replace('basic','detail')
            raw1 = requests.get(lk)
            html1 = BeautifulSoup(raw1.text,'html.parser')
            tit = html1.select_one('#content > div.article > div.mv_info_area > div.mv_info > h3 > a')
            if tit is None:
                t = 'no_info'
            else:
                t = tit.get_text()
                t = t.replace('\'','\\\'')
            print(t)
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
                for k in range(1,4):
                    tag = 'ul > li:nth-child('+str(k)+') > div > a'
                    actor = ul1.select_one(tag)
                    if actor is None:
                        break
                    else:
                        al+=actor.get_text()+', '
                al = al.replace('\'','\\\'')
            try:
                sheet.append([count,t,gen,director,al])
            except:
                sheet.cell(row=count,column=1).value='error'
        j+=1
    wb.save('C:/dev/3rd_test/movie_info.xlsx')
crowlmv()