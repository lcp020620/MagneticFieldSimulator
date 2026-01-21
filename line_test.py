import numpy as np
import plotly.graph_objects as go
from scipy.interpolate import griddata

# 1. 데이터 로드 (x, y, z, Bx, By, Bz)
n = 1000
data = np.random.uniform(-10, 10, (n, 6))
x, y, z = data[:, 0], data[:, 1], data[:, 2]
bx, by, bz = data[:, 3], data[:, 4], data[:, 5]

# 2. 정규 격자 생성 (보간을 위해 필요)
grid_res = 15j  # 격자 밀도 (너무 높으면 속도가 느려질 수 있음)
xi, yi, zi = np.mgrid[x.min():x.max():grid_res, 
                      y.min():y.max():grid_res, 
                      z.min():z.max():grid_res]

# 3. 불규칙한 데이터를 격자 데이터로 보간
grid_bx = griddata((x, y, z), bx, (xi, yi, zi), method='linear', fill_value=0)
grid_by = griddata((x, y, z), by, (xi, yi, zi), method='linear', fill_value=0)
grid_bz = griddata((x, y, z), bz, (xi, yi, zi), method='linear', fill_value=0)

# 4. Plotly Streamtube를 이용한 시각화
fig = go.Figure(data=go.Streamtube(
    x=xi.flatten(),
    y=yi.flatten(),
    z=zi.flatten(),
    u=grid_bx.flatten(),
    v=grid_by.flatten(),
    w=grid_bz.flatten(),
    sizeref=0.5,             # 튜브 두께 조절
    colorscale='Viridis',    # 색상 테마
    showscale=True,
    maxpoints=1000,          # 계산할 점의 최대 개수
    starts=dict(             # 자기력선이 시작되는 지점들 정의
        x=np.random.uniform(x.min(), x.max(), 20),
        y=np.random.uniform(y.min(), y.max(), 20),
        z=np.random.uniform(z.min(), z.max(), 20)
    )
))

fig.update_layout(
    title='3D Magnetic Field Lines (Plotly)',
    scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z'),
    margin=dict(l=0, r=0, b=0, t=40)
)

fig.show()
