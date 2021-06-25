#!/usr/bin/env python
# coding: utf-8

import sys
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import re
import random
import time
from urllib.parse import quote
import csv
import pandas as pd
from datetime import date
from IPython.display import clear_output
import os,os.path
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# pip install webdriver-manager

url = "https://www.yes123.com.tw/admin/index.asp"
driver.get(url)
# 設定搜尋關鍵字
element = driver.find_element_by_class_name("keyword")
element.send_keys("富邦人壽")
# 點搜尋鍵
button = driver.find_element_by_class_name('bt_search')
button.click()
URL_total=[] #initialize

#第一頁
def print_URL():
    save = driver.page_source
    soup = BeautifulSoup(save, "html.parser")
    results = soup.find_all('div', attrs={'class':'box_detail_list'})
    url_list = []
    real_url_pre = "https://www.yes123.com.tw/admin/"
    for u in results:
        url_result = u.find('ul').find_all('li')[2].find('a').get('href') #工作網址
        if str(url_result) != "None":
            real_url = real_url_pre + str(url_result)
            url_list.append(real_url)
    return url_list

URL_total = print_URL()
del URL_total[6] #第六個會是廣告刪掉
# 點第二頁
page_list = driver.find_element_by_class_name("pagenumber")
page_list.find_element_by_link_text("2").click()
# 第二頁
for i in print_URL():
    URL_total.append(i)
# 點第三頁
page_list = driver.find_element_by_class_name("pagenumber")
page_list.find_element_by_link_text("3").click()
# 印第三頁
for i in print_URL():
    URL_total.append(i)
# 點第四頁
page_list = driver.find_element_by_class_name("pagenumber")
page_list.find_element_by_link_text("4").click()
# 印第四頁
for i in print_URL():
    URL_total.append(i)
# 點第五頁
page_list = driver.find_element_by_class_name("pagenumber")
page_list.find_element_by_link_text("5").click()
# 印第五頁
for i in print_URL():
    URL_total.append(i)
driver.quit()#關閉瀏覽器
# #總共多少頁
# len(URL_total)

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
def get_todate():
    return date.today()

def csv_column_yes123(path_csv): #建立行標題
    with open(path_csv + '.csv', mode='a+', newline='', encoding='utf-8') as employee_file: 
        employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        employee_writer.writerow(['網址', '工作名稱', '工作內容', '薪資', '上班地點', '工作性質', '學歷要求', '聯絡人'])

web_list_yes123 = URL_total
web= ''
job_title= '' 
job_description= ''
job_salary= ''
job_place= ''
job_type= ''
education = ''
contact = ''

today = get_todate()
path_csv = "%s" % os.getcwd() + '/' + 'jobs_csv/'+ str(today) + '_yes123'
if not os.path.isdir('jobs_csv'): # 確認是否有jobs_csv資料夾  沒有則返回Ture
    os.mkdir('jobs_csv') # 建立jobs_csv資料夾
    print('建立jobs_csv資料夾完成')
csv_column_yes123(path_csv) #建立行標題

for j in web_list_yes123:
    soup = read_url(j) 
    print("正在讀取的網址為：" + j)
    web = j
    col_title = soup.select('.tt')
    num = len(col_title) #欄位數量
    job_title = soup.select('.jobname_title')[0].find('h1').get_text() #工作名稱
    # print(job_title)
    job_description = soup.select('.rr_box')[0].get_text() #工作內容
    # print(job_description)
    for i in range(0, num):
        try:
            web_col_title = col_title[i].get_text() #哪個欄位
            if web_col_title == '薪資待遇 ： ':
                job_salary = (str(soup.select('.rr')[i].get_text()).strip('每月薪資行情表我要申訴'))
            if web_col_title == '工作地點 ： ':
                job_place = (soup.select('.rr')[i].get_text())#上班地點 
                junk = (soup.select('.map')[0].get_text())#垃雞字
                job_place = job_place.strip(junk)

            if web_col_title == '工作性質 ： ':
                job_type = soup.select('.rr')[i].get_text()#工作類型
            # print(job_type)
            if web_col_title == '學歷要求 ： ':
                education = soup.select('.rr')[i].get_text() #學歷要求
            # print(education)
            col_title1 = soup.find_all('li')
            num1 = len(col_title1) #欄位數量
        except Exception as e:
            pass
    for i in range(0, num1):
        try:
            if soup.find_all('li')[i].select('.tt')[0].get_text() == '連絡人 ： ':
                contact = soup.find_all('li')[i].select('.rr')[0].get_text() #聯絡人
            # print(contact)
        except Exception as e:
            pass
    with open(path_csv + '.csv', mode='a+', newline='', encoding='utf-8') as employee_file: #w
                      employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                      employee_writer.writerow([web, job_title, job_description, job_salary, job_place, job_type, education, contact])


file= 'jobs_csv/' + str(get_todate()) + '_yes123.csv'
data_123 = pd.read_csv(file)
mask2 = data_123['薪資'].str.contains('160')
data_123_masked = data_123.loc[(mask2)]
#儲存成 csv格式檔
file_name =  str(get_todate()) + '_yes123人力銀行' #檔案名稱
# data_123_masked.to_csv('jobs_csv/{}.csv'.format(file_name), index=False)
data_123_masked.to_excel('jobs_csv/{}.xlsx'.format(file_name), index=False)
os.remove("%s" % os.getcwd() + '/' + 'jobs_csv/'+ str(get_todate()) +  '_yes123.csv')
print("爬蟲完成")

