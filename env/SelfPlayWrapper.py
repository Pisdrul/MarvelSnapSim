from env.snapEnv import SnapEnv
import gymnasium as gym
import numpy as np

class SinglePlayerAgent(gym.Env):
    def __init__(self, player="player_1", opponent_policy=None):
        self.raw_env = SnapEnv()
        self.player = player
        self.opponent = "player_2" if player == "player_1" else "player_1"
        self.opponent_policy = opponent_policy if opponent_policy is not None else self.random_policy
        self.action_space = self.raw_env.action_spaces[self.player]
        self.observation_space = gym.spaces.Box(low=-np.inf, high=np.inf, shape=(140,), dtype=np.float32)
        self.action_space = gym.spaces.Discrete(22)

    def random_policy(self, obs):
        return self.raw_env.action_spaces[self.opponent].sample()

    
    def reset(self, seed=None, options=None):
        raw_obs = self.raw_env.reset(seed=seed, options=options)
        obs = raw_obs["player_1"]
        info = {}  
        flat_obs = self.raw_env.flatten_obs(obs)
        return flat_obs, info

    def step(self, action):
        opponent_obs = self.raw_env.observe(self.opponent)
        opponent_action = self.opponent_policy(opponent_obs)

        actions = {
            self.player: action,
            self.opponent: opponent_action
        }

        obs, rewards, dones, truncations, infos = self.raw_env.step(actions)
        dones = all(dones.values())
        truncations = all(truncations.values())
        obs = self.raw_env.flatten_obs(obs[self.player], self.player)
        return (
            obs,
            rewards[self.player],
            dones,
            truncations,
            infos[self.player]
        )