from env.snapEnv import SnapEnv
import gymnasium as gym
import numpy as np
import torch
import random 
class SinglePlayerAgent(gym.Env):
    def __init__(self,opponent_model):
        self.raw_env = SnapEnv()
        self.p1tracker =0
        self.p2tracker =0
        if random.randint(0,1) >=0.5:   
            self.player = "player_1"
            self.opponent = "player_2"
            self.p1tracker +=1
        else:
            self.player = "player_2"
            self.opponent = "player_1"
            self.p2tracker +=1
        self.raw_env.tracked_player = self.player
        self.opponent_model = opponent_model if opponent_model is not None else self.random_policy
        self.opponent_random = True if opponent_model is None else False
        self.action_space = self.raw_env.action_spaces[self.player]
        self.observation_space = gym.spaces.Box(low=-np.inf, high=np.inf, shape=(140,), dtype=np.float32)
        self.action_space = gym.spaces.Discrete(22)

    def random_policy(self, obs):
        return self.raw_env.action_spaces[self.opponent].sample()

    
    def reset(self, seed=None, options=None):
        if random.randint(0,1) >=0.5:
            self.player = "player_1"
            self.opponent = "player_2"
            self.p1tracker +=1
        else:
            self.player = "player_2"
            self.opponent = "player_1"
            self.p2tracker +=1
        self.raw_env.tracked_player = self.player
        raw_obs = self.raw_env.reset(seed=seed, options=options)
        obs = raw_obs[self.player]
        info = {}  
        flat_obs = self.raw_env.flatten_obs(obs)
        return flat_obs, info

    def step(self, action):
        opponent_obs = self.raw_env.observe(self.opponent)
        opponent_obs = self.raw_env.flatten_obs(opponent_obs, self.opponent)
        if not self.opponent_random and self.opponent_model is not None:
            # Usa predict del modello per scegliere l'azione avversaria
            opponent_action, _ = self.opponent_model.predict(opponent_obs, deterministic=False)
        else:
            # Se è random, chiama la policy random
            opponent_action = self.opponent_model(opponent_obs) if callable(self.opponent_model) else self.raw_env.action_spaces[self.opponent].sample()
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