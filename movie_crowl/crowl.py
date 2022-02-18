from concurrent.futures import ThreadPoolExecutor
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import pandas as pd
import requests
import sys
sys.path.append('.')
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import openpyxl

from multiprocessing import Pool

def toprating(n):
    raw = requests.get("http://www.cgv.co.kr/movies/?lt=1&ft=0")
    html = BeautifulSoup(raw.text,"html.parser")

    mvtitle = html.select('strong.title')
    for i in range(n):
        print(str(i+1) + '위 : ' + mvtitle[i].text)

def allmv():
    raw = requests.get("http://ticket.cgv.co.kr/Reservation/Reservation.aspx?MOVIE_CD=&MOVIE_CD_GROUP=&PLAY_YMD=&THEATER_CD=&PLAY_NUM=&PLAY_START_TM=&AREA_CD=&SCREEN_CD=&THIRD_ITEM=#")
    html = BeautifulSoup(raw.text,"html.parser")

    mvtitle = html.select_one('div#movie_list')
    print(mvtitle)


def ifr():
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get("http://ticket.cgv.co.kr/Reservation/Reservation.aspx?MOVIE_CD=&MOVIE_CD_GROUP=&PLAY_YMD=&THEATER_CD=&PLAY_NUM=&PLAY_START_TM=&AREA_CD=&SCREEN_CD=&THIRD_ITEM=")
    r = driver.page_source
    soup = BeautifulSoup(r, "html.parser")

    #print(soup.select('div#movie_list > ul.content'))
    print(soup.select('#movie_list > ul'))
    #print(soup.select('span.text'))
    #print(soup.select('div.movie-select > div#movie_list > ul.content > a'))
    driver.close()

def categorymv():
    count=0
    mvt=[]
    for i in range(12,13):
        fname = 'movie_'+str(i)+'_info.xlsx'
        f=open(fname,'w',newline='',encoding='cp949')
        wr = csv.writer(f)
        url='https://movie.naver.com/movie/sdb/browsing/bmovie.naver?genre='+str(i)
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
                print(t)
                g = html1.select_one('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p > span:nth-child(1) > a')
                if g is None:
                    gen = 'no_info'
                else:
                    gen = g.get_text()
                d  = html1.select_one('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(4) > p > a')
                if d is None:
                    director = 'no_info'
                else:
                    director = d.get_text()
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
                try:
                    wr.writerow([count,t,gen,director,al])
                except:
                    wr.writerow(['encode_error'])
            j+=1
    f.close()

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