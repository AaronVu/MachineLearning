# -*- coding:utf-8 -*-
import time
import pandas as pd
import numpy as np


'''
Initialize Q arbitrarily //随机初始化Q值
Repeat (for each episode): //每一次循环是一个episode
    Initialize S //S为初始的状态
    Repeat (for each step of episode):
        根据当前Q和位置S，使用一种策略，得到动作A //这个策略可以是ε-greedy等
        做了动作A，小鸟到达新的位置S'，并获得奖励R 
        Q(S,A) ← (1-α)*Q(S,A) + α*[R + γ*maxQ(S',a)] //在Q中更新S
        S ← S'
    until S is terminal //结束
'''
N_STATES = 6  # 总的步数
ACTIONS = ['left', 'right']  # 只能左右走
EPSILON = 0.9  # greedy police 90%选择最优，10%随机
ALPHA = 0.1   # 学习效率
LAMBDA = 0.9  # 衰减度
MAX_EPISODES = 13   # 总训练次数
FRESH_TIME = 0.3    # 走一步花多久


def build_q_table(n_states, actions):
    table = pd.DataFrame(np.zeros((n_states, len(actions))), columns=actions)
    return table


def choose_action(state, q_table):
    state_actions = q_table.iloc[state, :]
    if np.random.uniform() > EPSILON or state_actions.all() == 0:
        action_name = np.random.choice(ACTIONS)
    else:
        action_name = state_actions.argmax()
    return action_name


def get_env_feedback(S, A):
    if A == 'right':
        if S == N_STATES - 2:
            S_ = 'terminal'
            R = 1
        else:
            S_ = S + 1
            R = 0
    else:
        R = 0
        if S == 0:
            S_ = S
        else:
            S_ = S - 1
    return S_, R


def update_env(S, episode, step_counter):
    env_list = ['-']*(N_STATES - 1)+['T']
    if S == 'terminal':
        interaction = 'Episode %s: total_steps == %s' % (episode+1, step_counter)
        print('\r{}'.format(interaction), end='')
        time.sleep(2)
        print('\r                                         ', end='')
    else:
        env_list[S] = 'o'
        interaction = ''.join(env_list)
        print('\r{}'.format(interaction), end='')
        time.sleep(FRESH_TIME)


def rl():
    q_table = build_q_table(N_STATES, ACTIONS)
    for episode in range(MAX_EPISODES):
        step_counter = 0
        S = 0
        is_terminated = False
        update_env(S, episode, step_counter)
        while not is_terminated:
            A = choose_action(S, q_table)
            S_, R = get_env_feedback(S, A)
            q_predict = q_table.ix[S, A]
            if S_ != 'terminal':
                q_target = R + LAMBDA*q_table.iloc[S_, :].max()
            else:
                q_target = R
                is_terminated = True
            q_table.ix[S, A] += ALPHA * (q_target - q_predict)
            S = S_
            update_env(S, episode, step_counter+1)
            step_counter += 1
    return q_table

rl()