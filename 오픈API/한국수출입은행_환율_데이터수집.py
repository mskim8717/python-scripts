import json
from bs4 import BeautifulSoup
from pandas import json_normalize
from urllib.request import urlopen

'''
한국수출입은행이 제공하는 환율정보입니다.
현재 환율을 실시간으로 제공합니다.
'''

'''
## Response Element ##
RESULT           Integer    조회 결과	1 : 성공, 2 : DATA코드 오류, 3 : 인증코드 오류, 4 : 일일제한횟수 마감
CUR_UNIT         String     통화코드	
CUR_NM           String     국가/통화명	
TTB              String     전신환(송금)받으실때	
TTS              String     전신환(송금)보내실때	
DEAL_BAS_R       String     매매 기준율	
BKPR             String     장부가격	
YY_EFEE_R        String     년환가료율	
TEN_DD_EFEE_R    String     10일환가료율	
KFTC_DEAL_BAS_R  String     서울외국환중개 매매기준율	
KFTC_BKPR        String     서울외국환중개 장부가격	
'''

AUTH_KEY = 'aeyc8vNJUGalrFSQVWxUjAnP8pfUu9lQ'
search_date = '20211026'

url = 'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey=' + AUTH_KEY +'&searchdate=' + search_date + '&data=AP01'

html = urlopen(url)
bsObj = BeautifulSoup(html, "html.parser")

jsonObject = json.loads(bsObj.text)
df = json_normalize(jsonObject)

print(df[df['cur_unit']=='USD']['ttb'])