from stable_baselines3.common.callbacks import BaseCallback
import numpy as np
import os, csv
class CustomTensorboardCallback(BaseCallback):
    def __init__(self, csv_path, log_tensorboard, save_freq = 10000, verbose=0, iteration = None):
        super().__init__(verbose)
        self.episode_rewards = []
        self.current_rewards = 0.0
        self.csv_path = csv_path
        self.save_freq = save_freq
        self.episode_rewards = []
        self.current_rewards = []
        self.last_save_step = 0
        self.log_buffer = []
        self.log_tensorboard = log_tensorboard
        self.data_to_write = []  # Lista per accumulare le righe da scrivere
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
        reward = self.locals["rewards"][0]
        done = self.locals["dones"][0]

        self.current_rewards.append(reward)

        if done:
            ep_reward = sum(self.current_rewards)
            self.episode_rewards.append(ep_reward)
            self.current_rewards = []

        if self.num_timesteps - self.last_save_step >= self.save_freq:
            self.last_save_step = self.num_timesteps

            env = self.training_env.envs[0].unwrapped
            raw_env = getattr(env, "raw_env", None)

            if raw_env:
                winrate = getattr(raw_env, "winrate", None)
                games = getattr(raw_env, "games", None)
                games_won = getattr(raw_env, "games_won", None)
                self.logger.record("custom/winrate", winrate)
                self.logger.record("custom/games", games)
                self.logger.record("custom/games_won", games_won)
            else:
                winrate = games = games_won = None

            ep_rew_mean = np.mean(self.episode_rewards)
            self.log_buffer.append([self.iteration,self.num_timesteps, winrate, games, games_won, ep_rew_mean])
            
            # Salva la riga nella lista temporanea
            self.data_to_write.append([
                self.iteration,
                self.num_timesteps,
                winrate if winrate is not None else "NA",
                games if games is not None else "NA",
                games_won if games_won is not None else "NA",
                ep_rew_mean if ep_rew_mean is not None else "NA"
            ])

        return True
    
    def _on_training_end(self) -> None:
        # Scrivi tutte le righe accumulate
        if self.data_to_write:
            with open(self.csv_path, mode='a', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(self.data_to_write)