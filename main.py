#====imports for Magnetic Field calculation====
import cupy as cp
import numpy as np
import matplotlib.pyplot as plt
from currentgenerator import CurrentGen
from magneticfieldsimulator import MagneticFieldSimulator
from vectorgenerator import VectorGenerator
from vectorgenerator import row
#==============================================
#====imports for fastAPI communication=========
import pandas as pd
import io
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
#==============================================


#create a mesh
simulator = MagneticFieldSimulator()
meshDense = 30
width = 10
length = 10
height = 10
r = simulator.makeMesh(dense=meshDense, width=width, length=length, height=height)
activateROI = False
current = CurrentGen()  #make current polygon
#========examples of current generation========#
current.getLineCurrent(start=row(-10, 0, 0), end=row(10, 0, 0), I=1, dense=20)
current.getLineCurrent(start=row(0, 0, 0), end=row(0, -10, 0), I=1, dense=20)
# current.getCircleCurrent(origin=row(-8, 0, 0), face=row(1, 0, 0), radius=15, I=1, dense=50)
current.getCircleCurrent(origin=row(0, 0, 0), face=row(1, 0, 0), radius=5, I=1, dense=50)
dLArray = current.currentArr
#==============================================#


#execution of biotsavart law system
MF = simulator.makeMF(dLArray=dLArray)
#==============================================#


#filter only near ROI
vecgen = VectorGenerator()
vecgen.line(start=row(-10, 0, 0), end=row(10, 0, 0), dense=30)
# vecgen.circle(origin=row(0, 0, 0), face=row(1, 0, 0), radius=5, dense=30)
ROI = vecgen.vecArray
ROIIdx = simulator.isROI(space=r, ROI=ROI, range=2)
#==============================================#


#data preprocessing for fastAPI
grim = plt.figure().add_subplot(projection='3d')
if  activateROI:
    plotMF = cp.asnumpy(MF[ROIIdx, :])
    plotr = cp.asnumpy(r[ROIIdx, :])
else:
    plotMF = cp.asnumpy(MF)
    plotr = cp.asnumpy(r)
csvArray = np.concatenate([plotr[:, 0:3], plotMF[:, 0:3]], axis=1)
pdcsvArray = pd.DataFrame(csvArray, columns=['x', 'y', 'z', 'vx', 'vy', 'vz'])

#send data to fastAPI
pdcsvArray.to_csv('C:/[git]MagneticFieldSimulator/MFArray.csv', index=False)

# app = FastAPI()
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"]
# )
# @app.get("/", response_class=HTMLResponse)
# async def get_upload_form():
#     NotImplemented