import numpy as np
import pyvista as pv
from scipy.interpolate import griddata

# 1. 데이터 로드 (예시: 6개 열, n개 행)
# data[:, 0:3] = x, y, z | data[:, 3:6] = Bx, By, Bz
n = 1000
data = np.random.uniform(-10, 10, (n, 6)) 
points = data[:, :3]  # 위치 (x, y, z)
vectors = data[:, 3:] # 자기장 벡터 (Bx, By, Bz)

# 2. 정규 격자(Grid) 생성 
# griddata를 통해 이산 데이터를 3차원 볼륨 데이터로 변환합니다.
grid_x, grid_y, grid_z = np.mgrid[-10:10:20j, -10:10:20j, -10:10:20j]
grid_bx = griddata(points, vectors[:, 0], (grid_x, grid_y, grid_z), method='linear')
grid_by = griddata(points, vectors[:, 1], (grid_x, grid_y, grid_z), method='linear')
grid_bz = griddata(points, vectors[:, 2], (grid_x, grid_y, grid_z), method='linear')

# 결측치(NaN)를 0으로 채움
grid_bx = np.nan_to_num(grid_bx)
grid_by = np.nan_to_num(grid_by)
grid_bz = np.nan_to_num(grid_bz)

# 3. PyVista 격자 객체 생성
mesh = pv.StructuredGrid(grid_x, grid_y, grid_z)
mesh["B_Field"] = np.c_[grid_bx.ravel(), grid_by.ravel(), grid_bz.ravel()]

# 4. 자기력선(Streamlines) 생성
# 특정 영역(예: 구체 형태)에서 시작하는 자기력선들을 추적합니다.
streamlines = mesh.streamlines(
    vectors="B_Field",
    source_radius=5.0, # 선이 시작될 범위
    n_points=50,       # 생성할 선의 개수
    integration_direction='both'
)

# 5. 시각화
plotter = pv.Plotter()
plotter.add_mesh(streamlines.tube(radius=0.1), scalars="B_Field", cmap="viridis")
plotter.add_axes()
plotter.show()

# 6. (선택사항) 가공된 자기력선 좌표 데이터 추출
# streamlines.points에 각 선을 구성하는 x, y, z 좌표들이 순서대로 들어있습니다.
line_data = streamlines.points 