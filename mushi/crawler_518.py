#!/usr/bin/env python
# coding: utf-8
import requests
from bs4 import BeautifulSoup
import re
import random
import time
from urllib.parse import quote
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import pandas as pd
from datetime import date
from IPython.display import clear_output
import os,os.path

def get_todate():
    return date.today()

def read_url(url):
    USER_AGENT_LIST = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
        "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        ]
    USER_AGENT = random.choice(USER_AGENT_LIST)
    headers = {'user-agent': USER_AGENT}
    s = requests.Session()
    req = s.get(url, headers = headers)
    soup = BeautifulSoup(req.text, "html.parser")
    return soup

def csv_column_518(path_csv): #建立行標題
    with open(path_csv + '.csv', mode='a+', newline='', encoding='utf-8') as employee_file: 
        employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        employee_writer.writerow(['網址','公司名稱', '工作名稱', '工作內容', '薪資', '上班地點', '工作性質', '學歷要求', '聯絡人'])

web_list_518 = []
url_list = ['https://www.518.com.tw/job-index-P-1.html?ai=0&ad=%E5%AF%8C%E9%82%A6%E4%BA%BA%E5%A3%BD&ai=0&ai=0', 'https://www.518.com.tw/job-index-P-2.html?ai=0&ad=%E5%AF%8C%E9%82%A6%E4%BA%BA%E5%A3%BD&ai=0']
for url in url_list:
  soup = read_url(url) #讀取網頁
  for title_1 in soup.select('.title')[2:]:
    web_url = title_1.select('a')[0].get('href')
    web_list_518.append(web_url) #兩頁共51筆
print("共" + str(len(web_list_518)) + "筆資料")

path_csv = "%s" % os.getcwd() + '/' + 'jobs_csv/'+ str(get_todate())+'_518人力銀行'
if not os.path.isdir('jobs_csv'): # 確認是否有jobs_csv資料夾  沒有則返回Ture
    os.mkdir('jobs_csv') # 建立jobs_csv資料夾
    print('建立jobs_csv資料夾完成')
csv_column_518(path_csv) #建立行標題

# company_name
# job_title
# job_description
# job_salary
# job_place
# job_type
# edu_title
# contact
for i in web_list_518:
    soup = read_url(i) 
    web = i
    company_name = soup.find_all('span')[2].get_text()#公司名稱
    job_title = soup.select('.job-title')[0].get_text() #工作名稱
    job_description = soup.select('.JobDescription')[0].find('p').get_text() #工作內容
    job_salary = soup.select('.jobItem')[0].find_all('li')[0].find('span').get_text() #薪資
    job_salary = job_salary.replace('時薪 160 元', '160')
    job_place = soup.select('.jobItem')[0].find_all('li')[1].find('span').get_text() #上班地點
    job_type = soup.select('.condition')[0].find('ul').find_all('li')[0].find('span').get_text() #工作類型
    edu_title = soup.find_all('li')[16].get_text() #學歷要求
    if str(edu_title[:4]) == '工作經驗':
        edu_title = soup.find_all('li')[17].find('span').get_text()
    else:
        edu_title = soup.find_all('li')[16].find('span').get_text()
    contact = soup.select('.contact_info')[0].find_all('li')[0].find('span').get_text() #聯絡人
    with open(path_csv + '.csv', mode='a+', newline='', encoding='utf-8') as employee_file: #w
                    employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    employee_writer.writerow([web, company_name, job_title, job_description, job_salary, job_place, job_type, edu_title, contact])

file= 'jobs_csv/' + str(get_todate()) + '_518人力銀行.csv'
data_518 = pd.read_csv(file)
file_name =  str(get_todate()) + '_518人力銀行' #檔案名稱
data_518.to_excel('jobs_csv/{}.xlsx'.format(file_name), index=False)
os.remove("%s" % os.getcwd() + '/' + 'jobs_csv/'+ str(get_todate()) +  '_518人力銀行.csv')
print("爬蟲完成！")