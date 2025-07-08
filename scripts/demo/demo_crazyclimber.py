# appends parent path to syspath to make ocatarashii importable
# like it would have been installed as a package
import sys
import random
import matplotlib.pyplot as plt

sys.path.insert(0, "../../")  # noqa

from ocatarashii.core import OCAtari
from ocatarashii.vision.utils import mark_bb, make_darker
from ocatarashii.utils import load_agent, parser
import pickle
import numpy as np


game_name = "CrazyClimberNoFrameskip"
MODE = "vision"
MODE = "revised"
HUD = True
env = OCAtari(game_name, mode=MODE, hud=HUD, render_mode="rgb_array")
observation, info = env.reset()

opts = parser.parse_args()

if opts.path:
    agent = load_agent(opts, env.action_space.n)

# snapshot = pickle.load(open("save_al.pickle", "rb"))
# env._env.env.env.ale.restoreState(snapshot)


action2 = 1
rs = 0

for i in range(1000000):
    # for i in range(8):
    #     env._env.unwrapped.ale.setRAM(95+i, 0)
    if opts.path is not None:
        action = agent.draw_action(env.dqn_obs)
    else:
        action = 0
    if i % 20 == 0:
        if action2 == 1:
            action2 = 4
        elif action2 == 4:
            action2 = 1
    obs, reward, terminated, truncated, info = env.step(action2)

    # if i > 300:
    #     action2 = 3

    if i % 100 == 0 and i > 400:
        # action2 = 4
        # with open('save_al.pickle', 'wb') as handle:
        #     pickle.dump(env._env.env.env.ale.cloneState(), handle, protocol=pickle.HIGHEST_PROTOCOL)
        # if i <= 2100:
        #     env._env.unwrapped.ale.setRAM(85, 83)
        #     env._env.unwrapped.ale.setRAM(26, 46)
        print(env.objects)
        ram = env._env.unwrapped.ale.getRAM()
        # print(ram[65], ram[78])
        # print(format(int(ram[65]), 'b').zfill(8))

        for obj in env.objects:
            x, y = obj.xy
            if x < 160 and y < 210:
                opos = obj.xywh
                ocol = obj.rgb
                sur_col = make_darker(ocol)
                mark_bb(obs, opos, color=sur_col)
        _, ax = plt.subplots(1, 1, figsize=(6, 8))
        ax.imshow(obs)
        plt.show()
    if terminated or truncated:
        observation, info = env.reset()
env.close()
