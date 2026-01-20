from flask import Flask, render_template, redirect, url_for
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

# 전류 정보를 저장할 리스트 (메모리 내 저장)
current_elements = []

class CurrentGen:
    def __init__(self, shape, intensity, details):
        self.shape = shape
        self.intensity = float(intensity)
        self.details = details  # 직선: [v1, v2], 원: [v1, v2, radius]

    def __repr__(self):
        return f"<CurrentGen {self.shape} | 세기: {self.intensity} | 정보: {self.details}>"

@app.route('/')
def index():
    return render_template('test.html')

@app.route('/newplot')
def newplot():
    # 저장된 모든 전류 정보를 시뮬레이션 페이지로 넘김
    return render_template('newplot.html', data=current_elements)

@socketio.on('add_element')
def handle_add_element(data):
    try:
        shape = data['shape']
        intensity = data['intensity']
        
        # 상세 정보 파싱
        v1 = tuple(map(float, data['v1']))
        v2 = tuple(map(float, data['v2']))
        
        if shape == 'straight':
            details = [v1, v2]
        elif shape == 'circle':
            radius = float(data['radius'])
            details = [v1, v2, radius]
        else:
            details = []

        # 클래스 생성 및 리스트 추가
        new_element = CurrentGen(shape, intensity, details)
        current_elements.append(new_element)
        
        print(f"현재 총 {len(current_elements)}개 요소 저장됨: {new_element}")
        
        # 클라이언트에 반영 완료 알림
        emit('add_success', {'count': len(current_elements)})
    except Exception as e:
        emit('error', {'msg': str(e)})

if __name__ == '__main__':
    socketio.run(app, debug=True)
