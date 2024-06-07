#!/usr/bin/env python3
import sys

from robobo_interface import SimulationRobobo, HardwareRobobo
from learning_machines import run_all_actions
import numpy as np
import time


def move_and_avoid_obstacles(rob) -> None:
    if isinstance(rob, SimulationRobobo):
        rob.play_simulation()
    lists_sensors = []
    while True:
        irs = rob.read_irs()
        front_ir_threshold = 20

        irs = np.array(irs)
        irs[np.isinf(irs)] = np.nan

        print(irs[7], irs[2], irs[4], irs[3], irs[5])
        list_sensors = [irs[7], irs[2], irs[4], irs[3], irs[5]]
        lists_sensors.append(list_sensors)

        if irs[2] is not None and irs[2] > front_ir_threshold:  # Check FrontL sensor
            # Obstacle detected, turn right
            print("turn right")
            rob.move_blocking(50, -50, 620)  # Turn right for 500 ms
            rob.move_blocking(20, 20, 3000)
            break

        else:
            # No obstacle, move forward
            rob.move_blocking(50, 50, 100)  # Move forward for 100 ms

        duration = 20
        start_time = time.time()
        current_time = time.time()

        # 检查是否超过了设定的持续时间
        if current_time - start_time > duration:
            print("Time's up! Exiting the loop.")
            break

    if isinstance(rob, SimulationRobobo):
        rob.stop_simulation()



def move_and_avoid_obstacles_back(rob) -> None:

    if isinstance(rob, SimulationRobobo):
        rob.play_simulation()

    while True:
        irs = rob.read_irs()
        front_ir_threshold = 1000

        irs = np.array(irs)
        irs[np.isinf(irs)] = np.nan
        print(irs[7], irs[2], irs[4], irs[3], irs[5])

        if irs[4] is not None and irs[4] > front_ir_threshold:
            # 检测到障碍物，后退
            rob.move_blocking(-50, -50, 99000)  # 后退 500 毫秒
            break
        else:
            # 无障碍物，向前移动
            rob.move_blocking(40, 40, 100)  # 向前移动 100 毫秒


    if isinstance(rob, SimulationRobobo):
        rob.stop_simulation()
if __name__ == "__main__":
    # You can do better argument parsing than this!
    print(sys.argv[1],"----------------------")
    if len(sys.argv) < 2:
        raise ValueError(
            """To run, we need to know if we are running on hardware of simulation
            Pass `--hardware` or `--simulation` to specify."""
        )
    elif sys.argv[1] == "--hardware":
        rob = HardwareRobobo(camera=True)
    elif sys.argv[1] == "--simulation":
        rob = SimulationRobobo()
    else:
        raise ValueError(f"{sys.argv[1]} is not a valid argument.")

    move_and_avoid_obstacles_back(rob)
    # move_and_avoid_obstacles(rob)