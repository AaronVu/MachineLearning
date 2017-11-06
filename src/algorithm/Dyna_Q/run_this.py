# -*- coding:utf-8 -*-

from algorithm.Dyna_Q.maze_env import Maze
from algorithm.Dyna_Q.RL_brain import QLearningTable, EnvModel


def update():
    for episode in range(40):
        s = env.reset()
        while True:
            env.render()
            a = RL.choose_action(str(s))
            s_, r, done = env.step(a)
            RL.learn(str(s), a, r, str(s_))

            # use a model to output (r, s_) by inputting (s, a)
            # the model in dyna Q version is just like a memory replay buffer
            env_model.store_transition(str(s), a, r, s_)
            for n in range(10):     # learn 10 more times using the env_model
                ms, ma = env_model.sample_s_a()  # ms in here is a str
                mr, ms_ = env_model.get_r_s_(ms, ma)
                RL.learn(ms, ma, mr, str(ms_))

            s = s_
            if done:
                break

    # end of game
    print('game over')
    env.destroy()


if __name__ == "__main__":
    env = Maze()
    RL = QLearningTable(actions=list(range(env.n_actions)))
    env_model = EnvModel(actions=list(range(env.n_actions)))

    env.after(0, update)
    env.mainloop()