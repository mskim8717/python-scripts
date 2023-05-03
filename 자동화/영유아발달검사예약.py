from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import time
import ctypes
from datetime import datetime
import pandas as pd
import requests
import getpass
import json
from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()

# headless 옵션 설정
# options.add_argument('headless')
options.add_argument("no-sandbox")
options.add_argument('window-size=800,600')

# 사람처럼 보이게 하는 옵션들
options.add_argument("disable-gpu")   # 가속 사용 x
options.add_argument("lang=ko_KR")    # 가짜 플러그인 탑재
options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')  # user-agent 이름 설정

user_id = input('아이디를 입력하세요: ')
user_pw = getpass.getpass('비밀번호를 입력하세요: ')

# 드라이버 위치 경로 입력
driver = webdriver.Chrome(options=options)

# url을 이용하여 브라우저로 접속
driver.get('http://www.sjsmped.com/bbs/login.php?url=%2F')

driver.implicitly_wait(3)

driver.find_element(By.ID, 'login_id').send_keys(user_id)
driver.find_element(By.ID, 'login_pw').send_keys(user_pw)
driver.find_element(By.XPATH, '//*[@id="login_fs"]/button').click()

# 로그인 된 화면 캡처
# driver.get_screenshot_as_file('capture.png')

driver.implicitly_wait(5)

df_orig = pd.DataFrame(columns=['date','time','name'])
df_update = pd.DataFrame(columns=['date','time','name'])

flag = False
slack_msg_flag = False


def post_message(channel, text):
    SLACK_BOT_TOKEN = "TOKEN_VALUE"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + SLACK_BOT_TOKEN
        }
    payload = {
        'channel': channel,
        'text': text
    }
    r = requests.post('https://slack.com/api/chat.postMessage',
        headers=headers,
        data=json.dumps(payload)
    )


while True:
    try:
        tempList = []
        for i in range(5, 6):
            try:
                print(str(i) + '월 데이터 조회 중....')
                url = 'http://www.sjsmped.com/bbs/board.php?bo_table=yb_board03&year=2023&month=' + str('{0:02d}'.format(i))
                print(url)
                driver.get(url)

                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
                request = Request(url, headers=headers)
                response = urlopen(request)
                rescode = response.getcode()
                # print("status", rescode)
                response_body = None
                if rescode == 200:
                    response_body = response.read().decode('utf-8')
                else:
                    print("response Error")

                html = driver.page_source  ## 페이지의 elements모두 가져오기
                soup = BeautifulSoup(html, 'html.parser')

                table = soup.find('table', {'class': 'wrap_calendar'})
                # print(table)

                div = table.find_all('div', {'class': 'U_month_rsv_list'})
                driver.implicitly_wait(1)
                for idx, d in enumerate(div):
                    try:
                        for li in d.find_all('li'):
                            try:
                                status = 'Occupy'
                                a = li.find_all('a')
                                # print(str(datetime.now().date().year) + str('{0:02d}'.format(i)) + str('{0:02d}'.format(idx)), a[0].text, a[1].text, len(a[1].text), status)
                                tempList.append([str(datetime.now().date().year) + str('{0:02d}'.format(i)) + str('{0:02d}'.format(idx+1)), a[0].text, str(a[1].text)])
                            except:
                                pass
                    except:
                        ctypes.windll.user32.MessageBoxW(0, 'Exception occur')
                time.sleep(2)
            except Exception as e:
                ctypes.windll.user32.MessageBoxW(0, str(e) + '프로그램이 종료되었습니다.')
                print(e)

        try:
            if flag is False:
                print('최초등록')
                df_orig = pd.DataFrame(tempList, columns=['date', 'time', 'name'])
                # df_orig.to_csv('df_orig.csv', encoding='euc-kr')
                flag = True
            else:
                df_update = pd.DataFrame(tempList, columns=['date', 'time', 'name'])
                # df_update.to_csv('df_update.csv', encoding='euc-kr')
                if df_orig.equals(df_update) is False:
                    status = 'Empty'
                    df_merge = df_orig.merge(df_update, how='outer', on=['date', 'name'], indicator=True)
                    msg = str(df_merge.loc[df_merge['_merge']=='left_only'][['date','time_x']].values[0])
                    # ctypes.windll.user32.MessageBoxW(0, msg)
                    print(msg)
                    if slack_msg_flag is False:
                        post_message("#autobot", msg)
                        slack_msg_flag = True
        except Exception as e:
            print('comp exception', str(e))
    except Exception as e:
        print('main exception', str(e))

driver.quit()