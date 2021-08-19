import urllib.request
from urllib.parse import urlencode, quote_plus
import pandas as pd
from bs4 import BeautifulSoup

# 기관명
inst = '인천교통공사'
url = "https://www.data.go.kr/tcs/dss/selectDataSetList.do?dType=FILE&detailKeyword=&publicDataPk=&recmSe=N&detailText=&relatedKeyword=&commaNotInData=&commaAndData=&commaOrData=&must_not=&tabId=&dataSetCoreTf=&coreDataNm=&sort=&relRadio=&orgFullName=&orgFilter=&org=&orgSearch=&currentPage=1&perPage=1000&brm=&instt=&svcType=&kwrdArray=&extsn=&coreDataNmArray=&pblonsipScopeCode=&" + urlencode({quote_plus('keyword'):inst}, encoding='UTF-8')


request = urllib.request.Request(url)
response = urllib.request.urlopen(request)
rescode = response.getcode()
if (rescode == 200):
    response_body = response.read().decode('utf8')
else:
    print("Error Code:" + rescode)
soup = BeautifulSoup(response_body, "lxml")

div = soup.find('div', {'class':'result-list'})

info = []
df = pd.DataFrame()
for li in div.findAll('li'):
    title = li.find('span', {'class': 'title'}).text.strip()

    span = li.findAll('span', {'class': 'data'})

    institute = span[0].text.strip()
    if inst == institute:
        modify_date = span[1].text.strip()
        hits_count = span[2].text.strip()
        # print(title, institute, modify_date, hits_count)
        info.append([title, institute, modify_date, hits_count])

df = pd.DataFrame(info, columns=['공공데이터명','제공기관','수정일','조회수'])
df.to_excel(inst + '_공공데이터개방현황.xlsx')