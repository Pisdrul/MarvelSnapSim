from stable_baselines3 import PPO
from env.SelfPlayWrapper import SinglePlayerAgent
from callback import CustomTensorboardCallback
from stable_baselines3.common.callbacks import CallbackList
from modelCallback import OpponentUpdateCallback
def linear_schedule(initial_value):
    def schedule(progress_remaining):
        return initial_value * progress_remaining
    return schedule

#DA FARE: creare due modelli diversi, uno che impara giocando il random e uno che impara giocando contro se stesso
#veere poi come entrambi sono contro il bot random

env = SinglePlayerAgent(opponent_model=None)
callback = CallbackList([
    CustomTensorboardCallback(csv_path="./checkpoints data/learning_vs_itself.csv"),
    OpponentUpdateCallback(env, update_freq=10000)
    ])

model = PPO.load("model vs self", env=env)

PPO.save(model, "temp_model")
env.opponent_model = PPO.load("temp_model", env=env)
env.opponent_random = False
model.set_env(env)

model.learn(total_timesteps=1000000, tb_log_name="run_vs_self_1", callback=callback)
model.save("model vs self")

