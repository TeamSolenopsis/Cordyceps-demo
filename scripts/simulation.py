# export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libstdc++.so.6
import pygame
import math
import numpy as np
from constants import *
from environment import Environment
from controller import Controller
import time

robotImage = 'images/robot.png'
metersToPixels = 3779.52
robotwidthPixels = 50
robotWidth = robotwidthPixels / metersToPixels
R = robotWidth
env_width = 1920
env_height = 1080

vs_origin_x_init = -560
vs_origin_y_init = 380
leading_trail_length = 200


def Position(x, y):
    xOffset = env_width / 2
    yOffset = env_height / 2
    return (x + xOffset, y + yOffset)


def InitEnv():
    pygame.init()
    dims = (env_height, env_width)
    env = Environment(dims, 'images/demo_warehouse_2d.jpg')

    return env


def FourRobotsEnv():
    env = InitEnv()

    env.addRobot(Position(vs_origin_x_init + 50, vs_origin_y_init + 50), robotImage)
    env.addRobot(Position(vs_origin_x_init - 50, vs_origin_y_init + 50), robotImage)
    env.addRobot(Position(vs_origin_x_init - 50, vs_origin_y_init - 50), robotImage)
    env.addRobot(Position(vs_origin_x_init + 50, vs_origin_y_init - 50), robotImage)

    env.addBox(Position(-1000, vs_origin_y_init), 'images/box_1.png')

    return env


loop_delay_seconds = 1


def main(Poses, x, y, angle, vs_origin_x, vs_origin_y):
    time.sleep(loop_delay_seconds)
    env = FourRobotsEnv()

    # Loading animation
    env.clear_trail()
    target = Position(vs_origin_x_init, vs_origin_y_init)
    env.move_box(target)

    # Driving to goal
    for i in range(0, leading_trail_length):
        env.add_pose_to_trail(Poses[i])

    for pose_index, Pose in enumerate(Poses):
        env.setManualPose(Pose, (x[pose_index] + vs_origin_x,
                          y[pose_index] + vs_origin_y), angle[pose_index])

        if pose_index + leading_trail_length < len(Poses):
            env.add_pose_to_trail(Poses[pose_index + leading_trail_length])

    env.clear_trail()
    target = Position(1200, -vs_origin_y_init)
    env.move_box(target)

    # some trickery to make the robots drive back to their original positions
    # ================================================================
    flipped_Poses = np.flip(Poses, 0)

    # invert the angle
    for poses in flipped_Poses:
        for robot_pose in poses:
            robot_pose[2] = robot_pose[2] + math.pi

    offset_robot = [900, 600, 150, 0]   # [r0, r1, r2, r3]

    for pose_index in range(len(flipped_Poses) + sum(offset_robot) + leading_trail_length):
        if pose_index > len(flipped_Poses) - 1:
            pose_index_3 = 4748
        else:
            pose_index_3 = pose_index

        pose_index_0 = max(pose_index - offset_robot[0], 0)
        pose_index_1 = max(pose_index - offset_robot[1], 0)
        pose_index_2 = max(pose_index - offset_robot[2], 0)

        if pose_index >= len(flipped_Poses) + offset_robot[0]:
            pose_index_0 = 4748
        if pose_index >= len(flipped_Poses) + offset_robot[1]:
            pose_index_1 = 4748
        if pose_index >= len(flipped_Poses) + offset_robot[2]:
            pose_index_2 = 4748

        try:
            _poses = [flipped_Poses[pose_index_0][0], flipped_Poses[pose_index_1]
                      [1], flipped_Poses[pose_index_2][2], flipped_Poses[pose_index_3][3]]
        except:
            print(
                f'index: {pose_index}, index_0: {pose_index_0}, index_1: {pose_index_1}, index_2: {pose_index_2}, pose_index_3: {pose_index_3}')

        if pose_index % 2 == 0:
            env.setManualPose_robot(_poses)

       # add pose to the trail when the robots are driving back to their original positions
        if (pose_index + leading_trail_length < len(flipped_Poses) - 3):
            env.add_pose_to_trail([
                flipped_Poses[pose_index_3 + leading_trail_length][3],
                flipped_Poses[pose_index_2 + leading_trail_length][2],
                flipped_Poses[pose_index_1 + leading_trail_length][1],
                flipped_Poses[pose_index_0 + leading_trail_length][0]
            ])

        elif (pose_index_0 + leading_trail_length > len(flipped_Poses) - offset_robot[0] - 1 and pose_index_1 + leading_trail_length < len(flipped_Poses) - offset_robot[1] - 1 and pose_index_2 + leading_trail_length < len(flipped_Poses) - offset_robot[2] - 1):
            env.add_pose_to_trail([
                flipped_Poses[pose_index_3 + leading_trail_length - 1][3],
                flipped_Poses[pose_index_2 + leading_trail_length - 1][2],
                flipped_Poses[pose_index_1 + leading_trail_length - 1][1],
                flipped_Poses[pose_index_0 - 1][0]
            ])

        elif (pose_index_1 + leading_trail_length > len(flipped_Poses) - offset_robot[1] - 1 and pose_index_2 + leading_trail_length < len(flipped_Poses) - offset_robot[2] - 1):
            env.add_pose_to_trail([
                flipped_Poses[pose_index_3 + leading_trail_length - 1][3],
                flipped_Poses[pose_index_2 + leading_trail_length - 1][2],
                flipped_Poses[pose_index_1 - 1][1],
                flipped_Poses[pose_index_0][0]
            ])

        elif (pose_index_2 + leading_trail_length > len(flipped_Poses) - offset_robot[2] - 1 and pose_index_1 + leading_trail_length < len(flipped_Poses) - offset_robot[1] - 1 and pose_index_0 + leading_trail_length < len(flipped_Poses) - offset_robot[0] - 1):
            env.add_pose_to_trail([
                flipped_Poses[pose_index_3 + leading_trail_length - 1][3],
                flipped_Poses[pose_index_2 - 1][2],
                flipped_Poses[pose_index_1][1],
                flipped_Poses[pose_index_0][0]
            ])

        else:
            env.add_pose_to_trail([
                flipped_Poses[pose_index_3][3],
                flipped_Poses[pose_index_2][2],
                flipped_Poses[pose_index_1][1],
                flipped_Poses[pose_index_0][0]
            ])

    # ================================================================

    env.clear_trail()


if __name__ == "__main__":
    Poses, x, y, angle, vs_origin_x, vs_origin_y = Controller()
    running = True
    while (running):

        main(Poses, x, y, angle, vs_origin_x, vs_origin_y)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
