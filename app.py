# pip install flask pandas flask-cors
from flask import Flask, make_response, render_template
import pandas as pd
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('newplot.html')

@app.route('/download-csv')
def download_csv():
    # 1. 데이터 생성
    df = pd.DataFrame({
        '이름': ['김철수', '이영희'],
        '나이': [20, 25]
    })
    # 2. 메모리 버퍼에 CSV 저장
    output = io.StringIO()
    df.to_csv(output, index=False, encoding='utf-8-sig')
    # 3. 응답 생성
    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=data.csv"
    response.headers["Content-type"] = "text/csv"
    return response

if __name__ == '__main__':
    app.run(port=5000)
