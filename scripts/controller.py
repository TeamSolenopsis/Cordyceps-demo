import numpy as np
import matplotlib.pyplot as plt


def Controller():
    RESOLUTION = 500  # The amount of points in which the paths will be split.
    MAX_SPEED = 20  # Maximum allowed speed from a robot.
    
    
    # r = 200
    # i = np.linspace(0.0,2*np.pi,RESOLUTION)
    # x = np.cos(i)*r
    # y = np.sin(i)*r

    vs_origin_x = 400 / 2  # pixels
    vs_origin_y = (920) / 2 # pixels

    x = [vs_origin_x]
    y = [vs_origin_y]

    # up
    x = np.append(x, np.linspace(x[-1], x[-1], RESOLUTION))
    y = np.append(y, np.linspace(y[-1],y[-1] - (180 ) , RESOLUTION))

    # turn right
    r = 200
    i = np.linspace(1.0*np.pi, 1.5*np.pi, RESOLUTION * 2)
    x = np.append(x, (x[-1] + r) + np.cos(i)*r)
    y = np.append(y, (y[-1]) + np.sin(i)*r)

    # path right
    x = np.append(x, np.linspace(x[-1], x[-1] + 730, int(RESOLUTION * 3.5)))
    y = np.append(y, np.linspace(y[-1], y[-1], int(RESOLUTION *3.5)))

    # turn left
    r = 200
    i = np.linspace(0.0, 0.5*np.pi, RESOLUTION * 2)
    x = np.append(x, (x[-1]) + np.flip(np.cos(i)*r))
    y = np.append(y, (y[-1]- r) + np.flip(np.sin(i)*r))


    # path up
    x = np.append(x, np.linspace(x[-1], x[-1], RESOLUTION))
    y = np.append(y, np.linspace(y[-1],y[-1] - 180 ,RESOLUTION))
   
    # # path right
    # x = np.append(x, np.linspace(x[-1], x[-1] + 100, RESOLUTION))
    # y = np.append(y, np.linspace(y[-1], y[-1], RESOLUTION))

    # # path left
    # x = np.append(x, np.linspace(x[-1], x[-1] - 100,RESOLUTION))
    # y = np.append(y, np.linspace(y[-1], y[-1], RESOLUTION))

    # # path up
    # x = np.append(x, np.linspace(x[-1], x[-1], RESOLUTION))
    # y = np.append(y, np.linspace(y[-1],y[-1] - 100 ,RESOLUTION))

    # # path down
    # x = np.append(x, np.linspace(x[-1], x[-1], RESOLUTION))
    # y = np.append(y, np.linspace(y[-1], y[-1] + 100, RESOLUTION))

    # # rotate CW
    # r = 200
    # i = np.linspace(0.0, 2*np.pi, RESOLUTION * 4)
    # x = np.append(x, (x[-1] - r) + np.cos(i)*r)
    # y = np.append(y, (y[-1]) + np.sin(i)*r))
    # plt.show()

    angle = 0.0  # rad
    angle_list = []

    vs_path = list(zip(x, y))  # Path of the VS.
    vs_angles = []  # Angles of the VS.
    for pose, next_pose in zip(vs_path, vs_path[1:]):
        dx = next_pose[0] - pose[0]
        dy = next_pose[1] - pose[1]
        vs_angles.append(-np.arctan2(dy, dx))

    """
    Transformation matrix for x y components:
    x   cos(θ) -sin(θ)  dX x
    y   sin(θ) cos(θ)   dY y
    1   0      0        1  1 
    """   

    path = []  # Path
    for i in range(len(x) - 1):
        # mag_vel = np.sqrt(np.square(x[i+1]-x[i]) + np.square(y[i+1]-y[i]))
        x_goal = x[i + 1] - x[i]
        y_goal = y[i + 1] - y[i]

        angle = np.arctan(y_goal / x_goal)
        
        if y_goal < 0 and x_goal < 0:
                angle += np.pi
        if y_goal > 0 and x_goal < 0:
                angle -= np.pi
        #if y_goal < 0:  # check if the angle is above pi.
        #    angle += np.pi

        tf_matrix = np.array(
            [
                [np.cos(angle), -np.sin(angle), x[i]],
                [np.sin(angle), np.cos(angle), y[i]],
                [0, 0, 1],
            ]
        )  # transformation matrix template.

        # Robot coordinates.
        bot_0_xy = np.array([50, -50, 1])
        bot_1_xy = np.array([50, 50, 1])
        bot_2_xy = np.array([-50, 50, 1])
        bot_3_xy = np.array([-50, -50, 1])

        # Calculation for pose of every robot in the VS.
        trans_0 = tf_matrix.dot(bot_0_xy)
        trans_1 = tf_matrix.dot(bot_1_xy)
        trans_2 = tf_matrix.dot(bot_2_xy)
        trans_3 = tf_matrix.dot(bot_3_xy)

        # Calculated path for every robot in the VS.
        path.append(
            (
                ([trans_0[0] + vs_origin_x, trans_0[1] + vs_origin_y, angle]),
                ([trans_1[0] + vs_origin_x, trans_1[1] + vs_origin_y, angle]),
                ([trans_2[0] + vs_origin_x, trans_2[1] + vs_origin_y, angle]),
                ([trans_3[0] + vs_origin_x, trans_3[1] + vs_origin_y, angle]),
            )
        )

    # Calculating the deltas for every individual robot (the x and y delta, also the theta).
    for vs_pose_id, vs_pose in enumerate(path):

        x_delta = 0

        for bot_pose_id, bot_pose in enumerate(vs_pose):
            try:
                yy = path[vs_pose_id + 1][bot_pose_id][1] - bot_pose[1]
                xx = path[vs_pose_id + 1][bot_pose_id][0] - bot_pose[0]
            except:
                alpha = alpha
            alpha = -np.arctan(yy/xx)

            if yy < 0 and xx < 0:
                alpha += np.pi
            if yy > 0 and xx < 0:
                alpha -= np.pi

            # Calculation for the speed in the magnitude direction x
            
            # tf_matrix = np.array(
            # [
            #     [np.cos(alpha), -np.sin(angle), 0],
            #     [np.sin(alpha), np.cos(angle), 0],
            #     [0, 0, 1],
            # ])
            # bot_pose = tf_matrix.dot(bot_pose)

            bot_pose[2] = alpha
            
    return path, x, y, vs_angles, vs_origin_x, vs_origin_y
