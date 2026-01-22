from flask import Flask, render_template, redirect, url_for
from flask_socketio import SocketIO, emit
from flask_currentgenerator import CurrentGen
import cupy as cp
import numpy as np
from magneticfieldsimulator import MagneticFieldSimulator
from threading import Timer
import os
import signal

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

@app.route('/resetData', methods=['POST'])
def resetData():
    global MF
    global r
    global current_elements
    MF = None
    r = None
    current_elements = []
    return '', 204

@app.route('/shutdown', methods=['POST'])
def shutdown():
    print("shutdown recieved")
    os.kill(os.getpid(), signal.SIGINT)
    return render_template('goodbye.html')

def open_browser():
    # webbrowser.open_new("http://127.0.0.1:5000")
    url = 'http://127.0.0.1:5000'
    os.system(f'start chrome --app={url}')

if __name__ == '__main__':
    Timer(1, open_browser).start()
    socketio.run(app, port=5000)
