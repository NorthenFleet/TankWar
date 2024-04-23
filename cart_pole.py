import gym
import pygame
from pygame.locals import *


def key_action():
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                return 0  # CartPole中，0代表向左移动
            elif event.key == K_RIGHT:
                return 1  # CartPole中，1代表向右移动
    return None


# 初始化pygame和gym环境
pygame.init()
# 经典控制和玩具文本
# Pendulum-v0, MountainCar-v0, Acrobot-v1, CartPole-v1
# Atari 游戏
# Pong: 'Pong-v0', 'Pong-v4'
# Breakout: 'Breakout-v0', 'Breakout-v4'
# SpaceInvaders: 'SpaceInvaders-v0', 'SpaceInvaders-v4'
# Seaquest: 'Seaquest-v0', 'Seaquest-v4'
# MsPacman: 'MsPacman-v0', 'MsPacman-v4'
env = gym.make("Seaquest-v0", render_mode="human")

env.reset()

done = False
while not done:
    # env.render()  # 渲染环境的一帧到屏幕上
    action = key_action()  # 获取键盘操作对应的动作
    if action is not None:
        _, _, done, _, _ = env.step(action)  # 执行动作并获取环境的反馈


env.close()
