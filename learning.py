from stable_baselines3 import PPO
from env.SelfPlayWrapper import SinglePlayerAgent

env = SinglePlayerAgent(player="player_1", opponent_policy=None)

model = PPO.load("first_model", env=env)
model.learn(total_timesteps=1)
print(env.raw_env.games)
print(env.raw_env.games_won)
print(env.raw_env.winrate)
model.save("first_model")