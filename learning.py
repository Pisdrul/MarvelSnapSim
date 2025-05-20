from stable_baselines3 import PPO
from env.SelfPlayWrapper import SinglePlayerAgent

env = SinglePlayerAgent(player="player_1", opponent_policy=None)

model = PPO.load("first_model", env=env)
model.learn(total_timesteps=60)

model.save("first_model")