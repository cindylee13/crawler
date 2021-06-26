#!/usr/bin/env python
# coding: utf-8
import requests
from bs4 import BeautifulSoup
import re
import random
import time
from urllib.parse import quote
import csv
import pandas as pd
from tqdm import tqdm, trange
from datetime import date
from IPython.display import clear_output
import os,os.path
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def get_todate():
    return date.today()

def selenium_get_Code_104(url):
    chrome_options = webdriver.ChromeOptions() 
    chrome_options.add_argument('--headless') 
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    save = driver.page_source
    driver.quit()#關閉瀏覽器
    soup = BeautifulSoup(save, "html.parser")
    page = soup.select('.page-select.js-paging-select.gtm-paging-top')[0].find_all('option')[-1].get('value')
    return page

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

def csv_column_104(path_csv): #建立行標題
    with open(path_csv + '.csv', mode='a+', newline='', encoding='utf-8') as employee_file: 
        employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        employee_writer.writerow(['日期','公司名稱', '文章編號', '工作網址'])

def find_title_104(key_txt):
    #路徑組合
    today = get_todate()
    path_csv = "%s" % os.getcwd() + '/' + 'jobs_csv/'+ str(today) +  '_104人力銀行'
    if not os.path.isdir('jobs_csv'): # 確認是否有jobs_csv資料夾  沒有則返回Ture
        os.mkdir('jobs_csv') # 建立jobs_csv資料夾
        print('建立jobs_csv資料夾完成')
    csv_column_104(path_csv) #建立行標題
    key = quote(key_txt)
    #  104 api searchTempExclude=2  -> 設定排除派遣
    find_page_url = 'https://www.104.com.tw/jobs/search/?ro=0&kwop=7&keyword={0}&order=15&asc=0&page=1&mode=s&jobsource=2018indexpoc&searchTempExclude=2'.format(key)
    get_sum_page = int(selenium_get_Code_104(find_page_url))
    print('共有：' + str(get_sum_page) + ' 頁')
    for i in tqdm(range(1, get_sum_page+1)):  #set page 1 to find all max page ,tqdm讀取進度條
        url = 'https://www.104.com.tw/jobs/search/?ro=0&kwop=7&keyword={0}&order=15&asc=0&page={1}&mode=s&jobsource=2018indexpoc&searchTempExclude=2'.format(key, i) 
        #time.sleep(random.randint(2,10)) #隨機等待
        soup = read_url(url) #讀取網頁
        print('目前爬取頁面是：' + url)
        for title_1 in soup.select('.b-block__left'):
            #有三個資料是無資料的，遇到無資料就跳過這個迴圈
            if title_1.select('.b-list-inline.b-clearfix.job-list-item__company') != soup.select('.b-block__left')[0].select('.b-list-inline.b-clearfix.job-list-item__company'):
                #日期
                try:
                    #正常代表找到 讚 廣告 (業主買廣告)，發生異常代表找不到 讚，執行except找日期 
                    date_match__ = title_1.select('.b-icon--gray.b-icon--w18')[0].select('use')[0]
                    date = '廣告'
                except:
                    date = title_1.select('.b-tit__date')[0].get_text().replace('\n','').replace(' ','')
                #公司名
                company_name = title_1.select('li')[1].find('a').get('title').split('\n')[0][4:]
                #工作網址
                title_url = title_1.select('.js-job-link')[0].get('href')[2:]
                #get 文章編號
                title_str = title_url.split('?')[0].split('/')[-1] #get 文章編號


                with open(path_csv + '.csv', mode='a+', newline='', encoding='utf-8') as employee_file: #w
                    employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    employee_writer.writerow([date,company_name, title_str, title_url])
            else:
                continue
    return print('求職網頁資料爬取完成')


sel = '104'
if sel == '104':
    input_str = '富邦人壽'
    find_title_104(input_str)
else:
    print('error')

file = 'jobs_csv/' +  str(get_todate()) + '_104人力銀行.csv'
data_104 = pd.read_csv(file)
mask1 = data_104.公司名稱.str.contains('富邦人壽')
data_masked = data_104.loc[(mask1)]
web_number = data_masked['文章編號']

# 檢查函式
#確認*公司名稱*是否有不符規定
def check_CompanyName(check_data):
    regex = re.compile(r'110A01') #正規
    if (regex == None):
        reason = '公司名稱'
    else:
        reason = ''
    return reason

#確認*職務名稱*是否有不符規定
def check_jobName(check_data):
    key_word = ['行銷專員CA', '行銷專員', '⾏銷專員CA(正職)', '行銷專員CA(正職)', '行銷專員', '行銷專員CA(正職)']
    if ((key_word[0]  not in check_data) and (key_word[1]  not in check_data)and (key_word[2]  not in check_data)):
        reason = '職務名稱'
    else:
        reason = ''
    return reason

#確認*薪資待遇*是否有不符規定
def check_salary(check_data):
    regex = re.compile(r'160') #正規
    match = regex.search(str(check_data))
    if match == None:
        reason = '薪資待遇'
    else:
        reason = ''
    return reason

# #確認*工作性質*是否有不符規定
# def check_jobType(check_data, check_jobType_reason_list):
#   check_jobType_reason_list = []
#   regex1 = re.compile(r'全職') #正規
#   regex2 = re.compile(r'正職') #正規
#   # print(match)
#   check_jobType_list = []
#   for i in check_data['工作性質']:
#     match = (regex1.search(str(i)) or regex2.search(str(i)))
#     if match == None:
#       check_jobType_list.append('False')
#       check_jobType_reason_list.append('工作性質')
#     else:
#       check_jobType_list.append('')
#       check_jobType_reason_list.append('')
#   return check_jobType_reason_list

# #確認*上班地點*是否有不符規定
# def check_jobPlace(check_data, check_jobPlace_reason_list):
#   check_jobPlace_reason_list = []
#   key_word = ['通訊處', '分處', '展業處']
#   # print(match)
#   check_jobPlace_list = []
#   for i in check_data['上班地點']:
#     if (key_word[0]  not in str(i)) and (key_word[1]  not in str(i)):
#       check_jobPlace_list.append('False')
#       check_jobPlace_reason_list.append('上班地點')
#     else:
#       check_jobPlace_list.append('')
#       check_jobPlace_reason_list.append('')
#   return check_jobPlace_reason_list

#確認*學歷要求*是否有不符規定
def check_jobEducation(check_data):
    key_word = ['高中職', '高中', '高中(職)', '高中(職)以上']
    if ((key_word[0]  not in check_data) and (key_word[1]  not in check_data) and (key_word[2]  not in check_data) and (key_word[3]  not in check_data)):
        reason = '學歷要求'
    else:
        reason = ''
    return reason

#確認*聯絡人*是否有不符規定
def check_contact(check_data):
    if check_data is None:
        reason = '聯絡人'
    else:
        reason = ''
    return reason

def csv_column_left(path_csv): #建立行標題
    with open(path_csv + '.csv', mode='a+', newline='', encoding='utf-8') as employee_file: 
        employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        employee_writer.writerow(['工作名稱', '公司名稱', '公司地址', '薪資', '工作內容', '學歷要求', '工作網址','工作性質','聯絡人','違規原因'])
path_csv1 = "%s" % os.getcwd() + '/' + 'jobs_csv/'+ str(get_todate()) + '_left_104人力銀行'
csv_column_left(path_csv1) #建立行標題

print('爬取單項資料及檢查資料')
for num in web_number:
  url = 'https://www.104.com.tw/job/ajax/content/' + num
  headers = {"Referer":"https://www.104.com.tw/job/" + num,}
  response = requests.get(url = url, headers = headers)
  storage = response.json()
  web_url = "https://www.104.com.tw/job/" + num
  title = storage['data']['header']['jobName'] #工作名稱
  reason = check_jobName(title) #檢查工作名稱
  company_name =  storage['data']['header']['custName'] #公司名稱
  reason = reason + check_CompanyName(company_name) #檢查公司名稱
  company_address = storage['data']['jobDetail']['addressRegion'] + storage['data']['jobDetail']['addressDetail'] #上班地點
  salary = storage['data']['jobDetail']['salary' ] #薪資
  reason = reason + check_salary(salary)#檢查薪資
  introduction = storage['data']['jobDetail']['jobDescription'] #工作內容
  education = storage['data']['condition']['edu'] #學歷要求
  reason = reason + check_jobEducation(education)#檢查學歷要求
  job_type = storage['data']['jobDetail']['jobType'] #工作類型
  contact_name = storage['data']['contact']['hrName']#聯絡人
  reason = reason + check_contact(contact_name)#檢查聯絡人
  with open(path_csv1 + '.csv', mode='a+', newline='', encoding='utf-8') as employee_file: #w
                    employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    employee_writer.writerow([title, company_name, company_address, salary, introduction, education, web_url, job_type, contact_name, reason])

file = 'jobs_csv/' +  str(get_todate()) + '_left_104人力銀行.csv'
data_left = pd.read_csv(file)
# 清資料
mask2 = data_left.薪資.str.contains('160')
data_left_masked = data_left.loc[(mask2)]
# 儲存成 csv格式檔
file_name =  str(get_todate()) + '_104人力銀行_檢查完成' #檔案名稱
data_left_masked.to_excel('jobs_csv/{}.xlsx'.format(file_name), index=False)
os.remove("%s" % os.getcwd() + '/' + 'jobs_csv/'+ str(get_todate()) +  '_104人力銀行.csv')
os.remove("%s" % os.getcwd() + '/' + 'jobs_csv/'+ str(get_todate()) +  '_left_104人力銀行.csv')
print("完成！請開啟檔案")



