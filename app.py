from vpython import *
import pandas as pd

def run_simulation_and_save_data(output_filename='simulation_data.csv'):
    # VPython 시뮬레이션 설정
    scene = canvas(visible=False) # 시뮬레이션 자체를 화면에 표시하지 않도록 설정
    scene.range = 5
    scene.background = color.white

    ball = sphere(pos=vector(0,0,0), radius=0.5, color=color.red)

    t = 0
    dt = 0.01
    max_time = 10 # 시뮬레이션 시간

    data = {'time': [], 'x': [], 'y': [], 'z': []}

    # 시뮬레이션 루프
    while t <= max_time:
        rate(100) # 화면에 표시하지 않으므로 rate는 성능에 큰 영향을 주지 않지만, 시뮬레이션 속도 조절에 사용될 수 있음
        t = t + dt
        ball.pos = vector(3*cos(t), 3*sin(t), 0)

        # 데이터 기록
        data['time'].append(t)
        data['x'].append(ball.pos.x)
        data['y'].append(ball.pos.y)
        data['z'].append(ball.pos.z)

    # 데이터 저장
    df = pd.DataFrame(data)
    df.to_csv(output_filename, index=False)
    print(f"Simulation data saved to {output_filename}")

if __name__ == "__main__":
    run_simulation_and_save_data()
