from stable_baselines3.common.callbacks import BaseCallback
import numpy as np
import os, csv
class CustomTensorboardCallback(BaseCallback):
    def __init__(self, csv_path, save_freq = 10000, verbose=0, iteration = None):
        super().__init__(verbose)
        self.episode_rewards = []
        self.current_rewards = 0.0
        self.csv_path = csv_path
        self.save_freq = save_freq
        self.last_save_step = 0
         # Se il file non esiste, crea header
        if not os.path.exists(self.csv_path):
            with open(self.csv_path, mode='w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["iteration", "timesteps", "winrate", "games", "games_won", "avg_reward"])
            self.iteration = 1
        else:
            # Se iteration è None, la calcoliamo
            if iteration is None:
                try:
                    with open(self.csv_path, mode='r') as f:
                        reader = csv.DictReader(f)
                        iterations = [int(row["iteration"]) for row in reader if row["iteration"].isdigit()]
                        self.iteration = max(iterations) + 1 if iterations else 1
                except Exception as e:
                    print(f"[Callback Warning] Errore nella lettura del CSV: {e}")
                    self.iteration = 1
            else:
                self.iteration = iteration

    def _on_step(self) -> bool:
        # Scarta tutti i wrapper
        env = self.training_env.envs[0].unwrapped
        reward = self.locals["rewards"]
        if isinstance(reward, (list, np.ndarray)):
            reward = reward[0]  # o l'indice corretto
        self.current_rewards += reward
        done = self.locals["dones"]  # idem, può essere array
        if isinstance(done, (list, np.ndarray)):
            done = done[0]
        if done:
            self.episode_rewards.append(self.current_rewards)
            self.current_rewards = 0.0
        if len(self.episode_rewards) > 0:
            ep_rew_mean = np.mean(self.episode_rewards)
        else:
            ep_rew_mean = 0.0
        # Accedi a raw_env se esiste
        raw_env = getattr(env, "raw_env", None)

        if raw_env is not None:
            winrate = getattr(raw_env, "winrate", None)
            games = getattr(raw_env, "games", None)
            games_won = getattr(raw_env, "games_won", None)
            ep_rew_mean = self.logger.record("custom/ep_rew_mean", ep_rew_mean)

            if winrate is not None:
                self.logger.record("custom/winrate", winrate)
            if games is not None:
                self.logger.record("custom/games", games)
            if games_won is not None:
                self.logger.record("custom/games_won", games_won)
            if ep_rew_mean is not None:
                self.logger.record("custom/ep_rew_mean", ep_rew_mean)
            # Scrittura su CSV
            if self.num_timesteps - self.last_save_step >= self.save_freq:
                self._save_metrics(winrate,games,games_won, ep_rew_mean)
                self.last_save_step = self.num_timesteps

        return True
    
    def _save_metrics(self,winrate,games,games_won, ep_rew_mean):
        if winrate is not None and games is not None and games_won is not None:
                with open(self.csv_path, mode='a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([self.iteration, self.num_timesteps, winrate, games, games_won, ep_rew_mean])