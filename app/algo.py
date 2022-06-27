import ast
from copy import deepcopy
import threading
import time
from app import db
from app.algo_helpers import invertPath, mergePaths
from app.models import Boxes
from config import Config


def fetchPath(start_pos: list[int], end_pos: list[int], lift_pos: list[int], carrying: bool, Path2LiftTable=None):
    if carrying == True:
        if end_pos[:-1] == lift_pos[:-1]:
            path = Path2LiftTable[f"{start_pos[0]}:{start_pos[1]} to {end_pos[0]}:{end_pos[1]}"]
        elif start_pos[:-1] == lift_pos[:-1]:
            path = invertPath(fetchPath(end_pos, start_pos, lift_pos, carrying, Path2LiftTable))
        else:  # Start-Target-combination is not included in the dictionary
            # In this case a new path will be obtained by merging the paths from start to Lift and from Lift to the arget location
            pathseg1 = deepcopy(fetchPath(start_pos, lift_pos, lift_pos, carrying, Path2LiftTable))
            pathseg2 = deepcopy(fetchPath(lift_pos, end_pos, lift_pos, carrying, Path2LiftTable))
            path = mergePaths(pathseg1, pathseg2)
        # print("Path-merging Done", flush=True)

    else:  # carrying = False -->  Roboter drives without box

        # NOTE this logic is layout dependant if general movement is needed use Algo directly
        #                       Y-Axis
        #                        0   1
        #                    ___________
        #                    |
        #               0    |   4
        #               1    |   1   2
        #     X-Axis    2    |   1   2
        #               3    |   3
        #                    |

        path = []
        if start_pos[1] == 1 and start_pos[1] != end_pos[1]:
            if start_pos[1] > end_pos[1]:
                path.append(["l", 1, abs(end_pos[1] - start_pos[1])])
            else:
                path.append(["r", 1, abs(end_pos[1] - start_pos[1])])
        if end_pos[0] != start_pos[0]:
            if start_pos[0] > end_pos[0]:
                path.append(["u", 1, abs(end_pos[0] - start_pos[0])])
            else:
                path.append(["d", 1, abs(end_pos[0] - start_pos[0])])
        if end_pos[1] == 1 and start_pos[1] != end_pos[1]:
            if start_pos[1] > end_pos[1]:
                path.append(["l", 1, abs(end_pos[1] - start_pos[1])])
            else:
                path.append(["r", 1, abs(end_pos[1] - start_pos[1])])
    if not (path == [] and path == None):
        return path
    else:
        return None


def readPath():
    with open("path_table.txt", "r") as file:
        return ast.literal_eval(file.read())


def bring_box_fn(job_list, robots_list, lift_list):
    Path2LiftTable = readPath()

    job = job_list[0]

    box_pos = find_box_pos(job.box_num)

    selected_robot = find_robot(robots_list)
    robot_pos = [selected_robot.pos_x, selected_robot.pos_y, selected_robot.pos_z]

    selected_elevator = find_lift(lift_list)
    elevator_pos = [selected_elevator.pos_x, selected_elevator.pos_y, selected_elevator.current_floor]

    hold_pos = [elevator_pos[0], elevator_pos[1], elevator_pos[2]]

    terminal_pos = [3, 0, 1]
    carrying = False
    if robot_pos[2] == box_pos[2]:
        path2box = fetchPath(robot_pos, box_pos, elevator_pos, False, Path2LiftTable)
        sendCommand2Robot(selected_robot, path2box, carrying)
    else:
        pass
        path2Lift = fetchPath(robot_pos, elevator_pos, elevator_pos, False, Path2LiftTable)
        sendCommand2Robot(selected_robot, path2Lift, carrying)
        wait4robot([selected_elevator.pos_x, selected_elevator.pos_y, selected_elevator.current_floor], robots_list)

        sendLift2Floor_with_Clearance(selected_elevator, box_pos[2], selected_robot)
        setNewRobotPos([selected_elevator.pos_x, selected_elevator.pos_y, box_pos[2]], robots_list)

        path2Box = fetchPath(elevator_pos, box_pos, elevator_pos, False, Path2LiftTable)
        sendCommand2Robot(selected_robot, path2Box, carrying)

    wait4robot([box_pos[0], box_pos[1], box_pos[2]], robots_list)

    carrying = True
    # box to terminal
    if box_pos[2] == terminal_pos[2]:
        path2terminal = fetchPath(box_pos, terminal_pos, elevator_pos, False, Path2LiftTable)
        sendCommand2Robot(selected_robot, path2terminal, carrying)

    else:
        path2Lift = fetchPath(box_pos, elevator_pos, elevator_pos, False, Path2LiftTable)
        sendCommand2Robot(selected_robot, path2Lift, carrying)
        wait4robot([selected_elevator.pos_x, selected_elevator.pos_y, selected_elevator.current_floor], robots_list)

        sendLift2Floor_with_Clearance(selected_elevator, terminal_pos[2], selected_robot)
        print(f"--> Lift goes to Level: {terminal_pos[2]}", flush=True)

        setNewRobotPos([selected_elevator.pos_x, selected_elevator.pos_y, terminal_pos[2]], robots_list)

        path2terminal = fetchPath(elevator_pos, terminal_pos, elevator_pos, False, Path2LiftTable)
        sendCommand2Robot(selected_robot, path2terminal, carrying)

    wait4robot(terminal_pos, robots_list)
    print("The robot is in the terminal. ", flush=True)

def send_box_back_fn(job_list, robots_list, lift_list):
    Path2LiftTable = readPath()

    job = job_list[0]

    box_pos = find_box_pos(job.box_num)

    selected_robot = find_robot(robots_list)
    robot_pos = [selected_robot.pos_x, selected_robot.pos_y, selected_robot.pos_z]

    selected_elevator = find_lift(lift_list)
    elevator_pos = [selected_elevator.pos_x, selected_elevator.pos_y, selected_elevator.current_floor]

    terminal_pos = [3, 0, 1]


    carrying = True

    # STATUS: robot should be underneath the selected box -> Carry=on
    if box_pos[2] == terminal_pos[2]:
        path2boxpos = fetchPath(terminal_pos, box_pos, elevator_pos, carrying, Path2LiftTable)
        sendCommand2Robot(selected_robot, path2boxpos, carrying)
    else:
        path2Lift = fetchPath(terminal_pos, elevator_pos, elevator_pos, carrying, Path2LiftTable)
        sendCommand2Robot(selected_robot, path2Lift, carrying)
        wait4robot([selected_elevator.pos_x, selected_elevator.pos_y, selected_elevator.current_floor], robots_list)

        sendLift2Floor_with_Clearance(selected_elevator, box_pos[2], selected_robot)
        print(f"--> Lift goes to Level: {box_pos[2]}", flush=True)

        setNewRobotPos([selected_elevator.pos_x, selected_elevator.pos_y, box_pos[2]], robots_list)
        path2Boxpos = fetchPath(elevator_pos, box_pos, elevator_pos, carrying, Path2LiftTable)
        sendCommand2Robot(selected_robot, path2Boxpos, carrying)

    wait4robot(box_pos, robots_list)
    # Robot to hold pos
    carrying = False
    hold_pos = [elevator_pos[0], elevator_pos[1], selected_elevator.current_floor]
    path2holdpos = fetchPath(box_pos, hold_pos, elevator_pos, carrying, Path2LiftTable)
    sendCommand2Robot(selected_robot, path2holdpos, carrying)
    wait4robot(hold_pos, robots_list)
    print("\nRobot is in hold position.", flush=True)


def sendCommand2Robot(robot, path, carrying):
    if path == []:
        return
    if Config.EMULATOR_MODE:
        th = threading.Thread(target=emuRobotFn, args=(robot, path, carrying))
        th.start()
    else:
        # Logic for sending message to robot
        pass
    print(f"Robot travels {path}", flush=True)

def emuRobotFn(robot, path, carrying):
    etr = sum([ele[2]*1 for ele in path])
    print(f"ETR: {etr}", flush=True)
    time.sleep(etr)
    for ele in path:
        if ele[0]=="u":
            robot.pos_x -= ele[2]
        elif ele[0]=="d":
            robot.pos_x += ele[2]
        elif ele[0]=="l":
            robot.pos_y -= ele[2]
        elif ele[0]=="r":
            robot.pos_y += ele[2]
    print(f"Robot is now at [{robot.pos_x}, {robot.pos_y}, {robot.pos_z}]", flush=True)
    

def find_box_pos(box_num):
    box = Boxes.query.filter_by(box_num=box_num).first()
    return [box.x, box.y, box.z]


def find_robot(robots_list):
    # currently fixed to a single robot
    return robots_list[0]


def find_lift(lift_list):
    # currently fixed to a single elevator
    return lift_list[0]


def sendLift2Floor_with_Clearance(lift, floor, robot):
    sendCommand2Lift(lift, floor)
    wait4Lift(lift, floor)


def sendCommand2Lift(lift, floor):
    if Config.EMULATOR_MODE:
        print(f"Lift goes to Level: {floor}", flush=True)
    else:
        # Logic for sending message to lift
        pass


def wait4Lift(lift, floor):
    if Config.EMULATOR_MODE:
        time.sleep(3)
        lift.current_floor = floor
    else:
        while True:
            if lift.current_floor == floor:
                break
            else:
                time.sleep(1)


def setNewRobotPos(new_pos, robots_list):
    robots_list[0].pos_x = new_pos[0]
    robots_list[0].pos_y = new_pos[1]
    robots_list[0].pos_z = new_pos[2]

    print(f"Robot is now at {new_pos}", flush=True)


def wait4robot(pos, robots_list):
    while True:
        if pos[0] == robots_list[0].pos_x and pos[1] == robots_list[0].pos_y and pos[2] == robots_list[0].pos_z:
            break
        time.sleep(0.2)
