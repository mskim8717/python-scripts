import pandas as pd

# 네이버 증권 종목분석 리포트 주소
url = "https://finance.naver.com/research/company_list.nhn?&page=1"

# read_html 테이블 읽어오기
df = pd.read_html(url, encoding='cp949')[0]

# 특정열 삭제
df.drop(columns=['첨부','조회수'], inplace=True)

# '종목명' 열에서 결측치 포함시 해당 행 삭제
df = df[df['종목명'].notna()]

# CSV 파일 생성
df.to_csv('naver_finanace.csv', encoding='cp949')