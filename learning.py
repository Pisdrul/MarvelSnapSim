from env.snapEnv import SnapEnv
import numpy as np

env = SnapEnv()
observations = env.reset()

done = {agent: False for agent in env.agents}

while not all(done.values()):
    actions = {}
    for agent in env.agents:
        action_space = env.action_space(agent)
        actions[agent] = action_space.sample()
        
    observations, rewards, terminations, truncations, infos = env.step(actions)
    done = terminations 