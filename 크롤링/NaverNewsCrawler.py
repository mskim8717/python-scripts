import sys
import urllib.request
from bs4 import BeautifulSoup
import time

client_id = "CLIENT_KEY"  # 애플리케이션 등록시 발급 받은 값 입력
client_secret = "SECRET_KEY"  # 애플리케이션 등록시 발급 받은 값 입력

def Search(text):
    time.sleep(0.02)
    print('\n=============== 기사 검색 결과 ================\n')
    try:
        encText = urllib.parse.quote(text)
        url = "https://search.naver.com/search.naver?&where=news&query=" + encText
        request = urllib.request.Request( url )
        request.add_header( "X-Naver-Client-Id", client_id )
        request.add_header( "X-Naver-Client-Secret", client_secret )
        response = urllib.request.urlopen( request )
        rescode = response.getcode()
        if (rescode == 200):
            response_body = response.read().decode('utf8')
            #print( response_body.decode( 'utf-8' ) )
        else:
            print( "Error Code:" + rescode )
        soup = BeautifulSoup(response_body, "lxml")

        # print(response_body)ㅣ
        for li in soup.find('ul', {'class':'list_news'}).findAll('li',{'class':'bx'}):
            # company = li.find('div', {'class': 'news_area'}).find('div', {'class': 'info_group'})
            # print(company)
            # print(company.text[0])
            link = li.find('div', {'class':'news_area'}).find('a', {'class':'news_tit'})
            print (link.text)
            print (link['href'])
            print('\n')

            # media = li.find('dd',{'class':'txt_inline'})
            # print (str(media.text).strip().split()[0], str(media.text).strip().split()[1] + '\n')

        print('\n=============== 기사 검색 끝 ================\n')

    except ValueError:
        return "검색 실패"
    except TypeError:
        return "검색 실패"
    except AttributeError:
        return "검색 실패"
    except:
        return "검색 실패"

while True:
    text = input("기사 제목을 입력 하세요(종료시 엔터) : ")
    if text == '':
        print ("기사 검색 종료")
        break
    else:
        Search(text)