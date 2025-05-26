from stable_baselines3.common.callbacks import BaseCallback
import numpy as np

class CustomTensorboardCallback(BaseCallback):
    def __init__(self, verbose=0):
        super().__init__(verbose)

    def _on_step(self) -> bool:
        # Scarta tutti i wrapper
        env = self.training_env.envs[0].unwrapped

        # Accedi a raw_env se esiste
        raw_env = getattr(env, "raw_env", None)

        if raw_env is not None:
            winrate = getattr(raw_env, "winrate", None)
            games = getattr(raw_env, "games", None)
            games_won = getattr(raw_env, "games_won", None)

            if winrate is not None:
                self.logger.record("custom/winrate", winrate)
            if games is not None:
                self.logger.record("custom/games", games)
            if games_won is not None:
                self.logger.record("custom/games_won", games_won)

        return True