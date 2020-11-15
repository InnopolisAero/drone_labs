import sim as vrep
import time
import math
import numpy as np

def navigate_local(x, y, z, speed, clientID, QuadricopterT):
    speed = speed*0.1
    x_time = math.fabs(x / speed)
    y_time = math.fabs(y / speed)
    z_time = math.fabs(z / speed)
    x_k = 0
    y_k = 0
    z_k = 0
    m = x_timenavigate_local
    x_m = 0
    y_m = 0
    z_m = 0
    if m < y_time:
        m = y_time
    if m < z_time:
        m = z_time
    if m != 0:
        x_m = x_time/m
        y_m = y_time/m
        z_m = z_time/m
    x_sign = 1
    y_sign = 1
    z_sign = 1
    if x!= 0:
        x_sign = x / math.fabs(x)
    if y!= 0:
        y_sign = y/math.fabs(y)
    if z!=0:
        z_sign = z / math.fabs(z)
    while True:
        if ((x_k < m) and (y_k < m) and (z_k < m)):
            err = vrep.simxSetObjectPosition(clientID, QuadricopterT, QuadricopterT, (speed*x_sign*x_m, speed*y_sign*y_m, speed*z_sign*z_m),
                                             vrep.simx_opmode_oneshot)
            time.sleep(0.1)
            x_k += 1
            y_k += 1
            z_k += 1
        elif ((x_k < m) and (y_k < m) and (z_k == z_time)):
            err = vrep.simxSetObjectPosition(clientID, QuadricopterT, QuadricopterT, (speed*x_sign*x_m, speed*y_sign*y_m, 0.00),
                                             vrep.simx_opmode_oneshot)
            time.sleep(0.1)
            x_k += 1
            y_k += 1
        elif ((x_k < x_time) and (y_k == y_time) and (z_k == z_time)):
            err = vrep.simxSetObjectPosition(clientID, QuadricopterT, QuadricopterT, (speed*x_sign, 0.00, 0.00),
                                             vrep.simx_opmode_oneshot)
            x_k += 1
            time.sleep(0.1)
        elif ((x_k == x_time) and (y_k < y_time) and (z_k == z_time)):
            err = vrep.simxSetObjectPosition(clientID, QuadricopterT, QuadricopterT, (0.00, speed*y_sign, 0.00),
                                             vrep.simx_opmode_oneshot)
            y_k += 1
            time.sleep(0.1)
        elif ((x_k == x_time) and (y_k == y_time) and (z_k < z_time)):
            err = vrep.simxSetObjectPosition(clientID, QuadricopterT, QuadricopterT, (0.00, 0.00, speed*z_sign),
                                             vrep.simx_opmode_oneshot)
            z_k += 1
            time.sleep(0.1)
        elif ((x_k == x_time) and (y_k < m) and (z_k < m)):
            err = vrep.simxSetObjectPosition(clientID, QuadricopterT, QuadricopterT, (0.00, speed*y_sign*y_m, speed*z_sign*z_m),
                                             vrep.simx_opmode_oneshot)
            y_k += 1
            z_k += 1
            time.sleep(0.1)
        elif ((x_k < m) and (y_k == y_time) and (z_k < m)):
            err = vrep.simxSetObjectPosition(clientID, QuadricopterT, QuadricopterT, (speed*x_sign*x_m, 0.00, speed*z_sign*z_m),
                                             vrep.simx_opmode_oneshot)
            time.sleep(0.1)
            x_k += 1
            z_k += 1
        else:
            break

def navigate_map(x, y, z, speed, clientID, QuadricopterT):
    err, pos = vrep.simxGetObjectPosition(
        clientID, QuadricopterT, -1, vrep.simx_opmode_oneshot_wait)
    det_x = x - pos[0]
    det_y = y - pos[1]
    det_z = z - pos[2]
    navigate_local(round(det_x, 1), round(det_y, 1), round(det_z, 1), speed, clientID, QuadricopterT)

def get_pos(clientID, QuadricopterT):
    err, position = vrep.simxGetObjectPosition(clientID, QuadricopterT, -1, vrep.simx_opmode_oneshot_wait)
    return position

def get_rot(clientID, QuadricopterT):
    err, orientation = vrep.simxGetObjectOrientation(clientID, QuadricopterT, -1, vrep.simx_opmode_oneshot_wait)
    return orientation
