from stable_baselines3 import PPO
from env.SelfPlayWrapper import SinglePlayerAgent
from callback import CustomTensorboardCallback

def linear_schedule(initial_value):
    def schedule(progress_remaining):
        return initial_value * progress_remaining
    return schedule

#DA FARE: creare due modelli diversi, uno che impara giocando il random e uno che impara giocando contro se stesso
#veere poi come entrambi sono contro il bot random
callback = CustomTensorboardCallback()

env = SinglePlayerAgent(player="player_1", opponent_model= None)
model = PPO(
    "MlpPolicy",
    env,
    learning_rate=linear_schedule(3e-4),
    verbose=1,
    tensorboard_log="./ppo_selfplay_tensorboard/"
)

model.set_env(env)

model.learn(total_timesteps=1000000, tb_log_name="run_random_1", callback=callback)
model.save("first_model")

selfmodel = PPO.load("first_model")
env = SinglePlayerAgent(player="player_1", opponent_model= selfmodel)
model = PPO(
    "MlpPolicy",
    env,
    learning_rate=linear_schedule(3e-4),
    verbose=1,
    tensorboard_log="./ppo_selfplay_tensorboard/"
)

model.set_parameters("first_model")
env.opponent_model = model
model.set_env(env)



model.learn(total_timesteps=1000000, tb_log_name="run_1", callback=callback)
model.save("first_model")

