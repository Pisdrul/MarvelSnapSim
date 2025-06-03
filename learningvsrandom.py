from stable_baselines3 import PPO
from env.SelfPlayWrapper import SinglePlayerAgent
from callback import CustomTensorboardCallback
from stable_baselines3.common.logger import configure

def linear_schedule(initial_value):
    def schedule(progress_remaining):
        return initial_value * progress_remaining
    return schedule

#DA FARE: creare due modelli diversi, uno che impara giocando il random e uno che impara giocando contro se stesso
#veere poi come entrambi sono contro il bot random
callback = CustomTensorboardCallback(csv_path="./checkpoints data/learning_vs_random.csv", log_tensorboard=True)
env = SinglePlayerAgent(opponent_model= None)
model = PPO("MlpPolicy", env, verbose=1, learning_rate=linear_schedule(0.0001))
model.set_env(env)
model.learn(total_timesteps=1000000, tb_log_name="run_random_1", callback=callback)
model.save("model vs random V2")