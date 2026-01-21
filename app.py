from flask import Flask, render_template, redirect, url_for
from flask_socketio import SocketIO, emit
from flask_currentgenerator import CurrentGen
import cupy as cp
import numpy as np
import pandas as pd
from magneticfieldsimulator import MagneticFieldSimulator
from scipy.integrate import solve_ivp

app = Flask(__name__)
socketio = SocketIO(app)

current_elements = []
meshDense = 30
width = 10
length = 10
height = 10
MF = None
r = None

@app.route('/')
def index():
    return render_template('CurrentGen_Interface.html')

@socketio.on('define_meshgrid')
def defineMeshgrid(data):
    global meshDense
    global width
    global length
    global height
    try:
        meshDense = int(data['meshDense'])
        width = int(data['meshWidth'])
        length = int(data['meshLength'])
        height = int(data['meshHeight'])
    except Exception as e:
        emit('error', {'msg': str(e)})

@socketio.on('add_element')
def handle_add_element(data):
    try:
        shape = data['shape']
        intensity = data['intensity']
        dense = data['dense']
        
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

        new_element = CurrentGen(shape, dense, intensity, details)
        current_elements.append(new_element)
        print(f"Total {len(current_elements)} requests standby: {new_element}")
        
        # 클라이언트에 반영 완료 알림
        emit('add_success', {'count': len(current_elements)})
    except Exception as e:
        emit('error', {'msg': str(e)})

@socketio.on('remove_element')
def handle_remove_element(data):
    try:
        index = int(data['index'])
        if 0 <= index < len(current_elements):
            removed = current_elements.pop(index)
            print(f"Request Canceled: {removed}")
            emit('update_list', {'count': len(current_elements)})
    except Exception as e:
        emit('error', {'msg': str(e)})

#==========Simulation Start(vector plot)==========
@app.route('/vectorplot')
def vectorplot():
    global MF
    global r
    dLArray = cp.zeros((0, 7), dtype=cp.float32)
    #==========make current vector array==========
    for _ in current_elements:
        _.getCurrent()
        dLArray = cp.append(dLArray, _.getCurrent(), axis=0)
    
    #==========simulate magnetic field==========
    simulator = MagneticFieldSimulator()
    r = simulator.makeMesh(dense=meshDense, width=width, length=length, height=height)
    MF = simulator.makeMF(dLArray=dLArray)

    plotMF = cp.asnumpy(MF)
    plotr = cp.asnumpy(r)
    csvArray = np.concatenate([plotr[:, 0:3], plotMF[:, 0:3]], axis=1)
    csvArray.transpose()
    data_to_send = csvArray.tolist()
    return render_template('vectorplot.html', data=data_to_send)

#==========Simulation Start(line plot)==========
@app.route('/lineplot')
def lineplot():
    global MF
    global r
    dLArray = cp.zeros((0, 7), dtype=cp.float32)
    #==========make current vector array==========
    for _ in current_elements:
        _.getCurrent()
        dLArray = cp.append(dLArray, _.getCurrent(), axis=0)
    
    #==========simulate magnetic field==========
    simulator = MagneticFieldSimulator()
    r = simulator.makeMesh(dense=meshDense, width=width, length=length, height=height)
    MF = simulator.makeMF(dLArray=dLArray)

    plotMF = cp.asnumpy(MF)
    plotr = cp.asnumpy(r)
    csvArray = np.concatenate([plotr[:, 0:3], plotMF[:, 0:3]], axis=1)
    csvArray.transpose()
    data_to_send = csvArray.tolist()
    NotImplemented      #여기다가 자기력선 검출하는 프로그램을 scipy로 작성해야함
    return render_template('lineplot.html', data=data_to_send)

@app.route('/resetData', methods=['POST'])
def resetData():
    global MF
    global r
    global current_elements
    MF = None
    r = None
    current_elements = []
    print("reset!!!")
    return '', 204

if __name__ == '__main__':
    socketio.run(app, debug=True)
