from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

# 데이터 전처리
try:
    df = pd.read_csv('기업소개자료_업데이트_250904.csv')
except UnicodeDecodeError:
    df = pd.read_csv('기업소개자료_업데이트_250904.csv', encoding='euc-kr')

# 불필요한 열과 행 제거
df.dropna(axis=1, how='all', inplace=True)
df.dropna(axis=0, how='all', inplace=True)

# '설립년도'를 정수형으로 변환 (결측치는 빈 문자열로 처리)
df['설립년도'] = df['설립년도'].fillna(0).astype(int).astype(str).replace('0', '')


# 메인 페이지: 산업 분야 선택
@app.route('/')
def index():
    sectors = df['산업 분야(6종)'].unique()
    return render_template('index.html', sectors=sectors)

# 기업 선택 페이지
@app.route('/sector/<sector>')
def select_company(sector):
    companies = df[df['산업 분야(6종)'] == sector]['기업명'].tolist()
    return render_template('select_company.html', sector=sector, companies=companies)

# 기업 상세 정보 페이지
@app.route('/company/<company_name>')
def company_details(company_name):
    company_info = df[df['기업명'] == company_name].iloc[0].to_dict()
    return render_template('company_details.html', company_info=company_info)

if __name__ == '__main__':
    app.run(debug=True)