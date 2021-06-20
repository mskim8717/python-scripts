import sys
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import time
import getpass
from datetime import datetime, time
from time import sleep
from selenium import webdriver

''' 사전예약 가능시간 : 09시~17시 '''
now = datetime.now().time()
if now < time(9,0,0) or now > time(17,0,0):
    print('자동 예약가능한 시간이 아닙니다. 프로그램을 종료합니다.')
    sys.exit()

'''
국립세종도서관 자동로그인  
'''
options = webdriver.ChromeOptions()

# headless 옵션 설정 : 개발환경이 리눅스라면 아래 두가지는 포함
options.add_argument('headless')
options.add_argument("no-sandbox")

# 브라우저 사이즈 : 현재 창을 열지 않는 방식으로 구현
# options.add_argument('window-size=800,600')

''' 1. 자동로그인 제어 '''
user_id = input('아이디를 입력하세요: ')
user_pw = getpass.getpass('비밀번호를 입력하세요: ')

# 드라이버 위치 경로 입력
driver = webdriver.Chrome()

# url을 이용하여 브라우저로 접속
driver.get('https://sejong.nl.go.kr/html/c7/c701.jsp')

# 대기시간 부여
driver.implicitly_wait(3)

driver.find_element_by_id('u_id').send_keys(user_id)
driver.find_element_by_id('pword').send_keys(user_pw)
driver.find_element_by_xpath('//*[@id="contentDrt"]/div[1]/div/form[4]/div/div/div[1]/div[2]/ul/li[4]/input').click()

# 로그인 된 화면 캡처
driver.get_screenshot_as_file('capture.png')

# 대기시간 부여
driver.implicitly_wait(5)


''' 2. 사전예약 자동제어 '''
''' 2.1 로그인 성공 팝업 제어 '''
while True:
    try:
        sleep(5)
        popup = driver.switch_to.alert.accept()
        if popup is None:
            break
    except Exception as e:
        raise

''' 2.2 사전예약 화면으로 이동 후 예약가능 확인 및 예약제어 실행 '''
visit_resv_url = 'https://sejong.nl.go.kr/visitResv/visitList.do?menuId=O510&upperMenuId=O500'
driver.get(visit_resv_url)
while True:
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    request = Request(visit_resv_url, headers=headers)
    response = urlopen(request)
    rescode = response.getcode()
    response_body = None
    if rescode == 200:
        response_body = response.read().decode('utf-8')
    else:
        print("response Error")

    soup = BeautifulSoup(response_body, "html.parser")
    div = soup.find('div', {'class':'btnC mT40'})
    print(datetime.now(), str(div.find('a').text).replace(' ', ''))
    if div.find('a').text != "예약마감":
        driver.find_element_by_xpath("""//*[@id="q1_1"]""").click()
        driver.find_element_by_xpath("""//*[@id="q2_1"]""").click()
        driver.find_element_by_xpath("""//*[@id="contentDrt"]/div/form/div[4]/div/a""").click()
        break
    sleep(0.5)

# 자동제어 종료
driver.quit()
