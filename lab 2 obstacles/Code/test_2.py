import sim
import math
import flib
import time
from geometry_tools import *

rad = math.radians

targer_point = np.array([10, 0, 1])
speed = 0.01

c_rep = 0.1
r_field = 2.

drone_pose = []

def rep_force(dist_to_obs):
    # type of 1/х
    return c_rep / dist_to_obs - c_rep / r_field


def get_near_obst(current_pose, obst_array):
    """
    возвращаем координату до близжайшего препятсвия
    """

    near_dist = None
    near_pose = None

    for pose in obst_array:
        dist = np.linalg.norm([current_pose[0] - pose[0], current_pose[1] - pose[1]])
        if near_dist is None or dist < near_dist:
            near_dist = dist
            near_pose = pose
            continue

    return near_pose, dist


if __name__=="__main__":
    sim.simxFinish(-1)
    clientID = sim.simxStart('127.0.0.1', 19997, True, True, 5000, 5)

    if clientID != -1:
        print('Connected to remote API server')
    err, QuadricopterT = sim.simxGetObjectHandle(
        clientID, 'Quadricopter_target', sim.simx_opmode_blocking)
    if err == -1:
        print("No Quadricopter")
    err, Quadricopter = sim.simxGetObjectHandle(
        clientID, 'Quadricopter', sim.simx_opmode_blocking)
    if err == -1:
        print("No Quadricopter")

    sim.simxStartSimulation(clientID, sim.simx_opmode_blocking)

    obst_count = 14
    obst_list = []

    for i in range(obst_count):
        err, Obst = sim.simxGetObjectHandle(
            clientID, 'collum_'+str(i), sim.simx_opmode_blocking)
        obst_pose = flib.get_pos(clientID, Obst)
        obst_list.append(obst_pose)


    print("is conneted!!!")
    pose = flib.get_pos(clientID, QuadricopterT)
    rot = flib.get_rot(clientID, QuadricopterT)

    t = 0
    old_timer = time.time()

    while True:
        dt = time.time() - old_timer
        t += dt
        old_timer = time.time()
        if dt < 0.0001:
            continue


        drone_pose = flib.get_pos(clientID, Quadricopter)

        obst_pose, dist_to_obst = get_near_obst(drone_pose, obst_list)
        print("obst_pose", obst_pose, "dist_to_obst", dist_to_obst)


        pose = flib.get_pos(clientID, QuadricopterT)
        goal_vec = targer_point - pose
        goal_vec *= speed

        err = sim.simxSetObjectPosition(clientID, QuadricopterT, -1,
                                        (pose[0] + goal_vec[0], pose[1] + goal_vec[1], pose[2] + +goal_vec[2]),
                                        sim.simx_opmode_blocking)
        err = sim.simxSetObjectOrientation(clientID, QuadricopterT, -1, (0, 0, rad(0)), sim.simx_opmode_blocking)

        time.sleep(0.01)

    sim.simxFinish(clientID)
