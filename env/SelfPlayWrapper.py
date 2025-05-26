from env.snapEnv import SnapEnv
import gymnasium as gym
import numpy as np

class SinglePlayerAgent(gym.Env):
    def __init__(self,opponent_model, player="player_1"):
        self.raw_env = SnapEnv()
        self.player = player
        self.opponent = "player_2" if player == "player_1" else "player_1"
        self.opponent_model = opponent_model if opponent_model is not None else self.random_policy
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
        opponent_obs = self.raw_env.flatten_obs(opponent_obs, self.opponent)
        opponent_action = int(self.opponent_model.predict(opponent_obs, deterministic=True)[0])

        actions = {
            self.player: action,
            self.opponent: opponent_action
        }

        obs, rewards, dones, truncations, infos = self.raw_env.step(actions)
        dones = all(dones.values())
        truncations = all(truncations.values())
        print("player obs")
        obs = self.raw_env.flatten_obs(obs[self.player], self.player)
        print(obs)
        return (
            obs,
            rewards[self.player],
            dones,
            truncations,
            infos[self.player]
        )