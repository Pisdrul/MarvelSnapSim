from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3 import PPO

class OpponentUpdateCallback(BaseCallback):
    def __init__(self, env, update_freq, verbose=0):
        super().__init__(verbose)
        self.env = env
        self.update_freq = update_freq
        self.last_update = 0

    def _on_step(self) -> bool:
        if self.num_timesteps - self.last_update >= self.update_freq:
            self.last_update = self.num_timesteps

            # Salva e ricarica il modello come nuovo avversario
            self.model.save("temp_model.zip")
            opponent_model = PPO.load("temp_model.zip", env=self.env)
            self.env.opponent_model = opponent_model

        return True