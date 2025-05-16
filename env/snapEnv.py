from pettingzoo import ParallelEnv
from gymnasium import spaces
import numpy as np
from gameManager import GameState
import random

class SnapEnv(ParallelEnv):
    metadata = {"render.modes": ["human"], "name":"marvel_snap_v0"}

    def __init__(self):
        super().__init__()
        self.possible_agents = ["player_1", "player_2"]
        self.agents = self.possible_agents[:]
        self.gm = GameState()
        self.gm.reset()
        self.card_names = [

        "Agent 13",
        "America Chavez",
        "Angel",
        "Antman",
        "Apocalypse",
        "Armor",
        "Bishop",
        "Blade",
        "Blue Marvel",
        "Bucky Barnes",
        "Winter Soldier",
        "Cable",
        "Captain America",
        "Carnage",
        "Cloak",
        "Coleen Wing",
        "Colossus",
        "Cosmo",
        "Death",
        "Deathlok",
        "Devil Dinosaur",
        "Doctor Strange",
        "Ebony Maw",
        "Elektra",
        "Enchantress",
        "Forge",
        "Gamora",
        "Groot",
        "Hawkeye",
        "Heimdall",
        "Hobgoblin",
        "Hulk Buster",
        "Iceman",
        "The Infinaut",
        "Iron Fist",
        "Iron Man",
        "Jessica Jones",
        "Jubilee",
        "Kazar",
        "Killmonger",
        "Klaw",
        "Knull",
        "Korg",
        "Kraven",
        "Lady Sif",
        "Lizard",
        "Magik",
        "Mantis",
        "Medusa",
        "Mister Sinister",
        "Sinister Clone",
        "Namor",
        "Nightcrawler",
        "Onslaught",
        "Punisher",
        "Modok",
        "Moongirl",
        "Morbius",
        "Morph",
        "Mr Fantastic",
        "Multiple Man",
        "Nakia",
        "Nova",
        "Odin",
        "Okoye",
        "Professor X",
        "Psylocke",
        "Rhino",
        "Rocket Racoon",
        "Sabretooth",
        "Scarlet Witch",
        "Scorpion",
        "Sentinel",
        "Shang-Chi",
        "Squirrel Girl",
        "Squirrel",
        "Star Lord",
        "Storm",
        "Strong Guy",
        "Sunspot",
        "Swarm",
        "Sword Master",
        "Uatu The Watcher",
        "Vision",
        "Vulture",
        "Warpath",
        "White Queen",
        "White Tiger",
        "Tiger",
        "Wolfsbane",
        "Wolvering",
        "Yondu"
        ]
        self.CARD_NAME_TO_ID = {name: idx for idx, name in enumerate(self.card_names)}
        self.location_names = [
            "Revealing Location in 1 turns",
            "Revealing Location in 2 turns",
            "Revealing Location in 3 turns",
            "Altar of Death",
            "Asgard",
            "Asteroid M",
            "Atlantis",
            "Bar with no name",
            "Castle Blackstone",
            "Crimson Cosmos",
            "Crown City",
            "Elysium",
            "Fisk Tower",
            "Hellfire Club",
            "Jotunheim",
            "Kamar-Taj",
            "Kyln",
            "Lake Heldas",
            "Limbo",
            "Milano",
            "Mojo World",
            "Necrosha",
            "Negative Zone",
            "New York",
            "Nidavellir",
            "Onslaught Citadel",
            "Plunder Castle",
            "Project Pegasus",
            "Sanctum Sanctorum",
            "Sewer System",
            "Wakanda"
        ]
        self.LOCATION_NAME_TO_ID = {name: idx for idx, name in enumerate(self.location_names)}
        max_cards = len(self.card_names)
        max_hand_size = 7
        num_location = 3
        max_turns = 7
        
        card_space = spaces.Dict({
            "id": spaces.Discrete(max_cards),
            "cost": spaces.Box(low=0, high= 15, shape=(), dtype=np.int32),
            "power": spaces.Box(low= -np.inf, high=np.inf, shape=(), dtype=np.int32),
        })

        location_card_space = spaces.Dict({
            "id": spaces.Discrete(max_cards),
            "cost": spaces.Box(low=0, high= 15, shape=(), dtype=np.int32),
            "power": spaces.Box(low= -np.inf, high=np.inf, shape=(), dtype=np.int32),
        })

        location_space = spaces.Dict({
            "id": spaces.Discrete(len(self.location_names)),
            "ally_power": spaces.Box(low= -np.inf, high=np.inf, shape=(), dtype=np.int32),
            "enemy_power": spaces.Box(low= -np.inf, high=np.inf, shape=(), dtype=np.int32),
            "ally_cards": spaces.Sequence(location_card_space),
            "ally_cards_pre_reveal": spaces.Sequence(location_card_space),
            "enemy_cards": spaces.Sequence(location_card_space),
        })

        self._observation_space = spaces.Dict({
            "hand": spaces.Sequence(card_space),
            "energy": spaces.Box(low=0, high= np.inf, shape=(), dtype=np.int32),
            "turn": spaces.Discrete(max_turns+1),
            "locations": spaces.Dict({
                "location1": location_space,
                "location2": location_space,
                "location3": location_space,
            })
        })
        self.observation_spaces = {agent: self._observation_space for agent in self.possible_agents}

        action_size = max_hand_size * num_location + 1
        self.pass_action = 21
        self.action_spaces = {agent: spaces.Sequence(spaces.Discrete(action_size)) for agent in self.possible_agents}

    def encode_action(self,card_idx, location_idx):
        return card_idx * self.num_location + location_idx

    def decode_action(self, action):
        card_idx = action // 3
        location_idx = action % 3
        return (card_idx, location_idx)
    
    def reset(self, seed=None, options=None):
        self.gm.reset()
        self.agents = ["player_1", "player_2"]
        if seed is not None:
            random.seed(seed)
        observations = {agent: self.observe(agent) for agent in self.agents}
        return observations

    def observation_space(self, agent):
        return self.observation_space[agent]

    def action_space(self, agent):
        return self.action_spaces[agent]
    
    def fromCardToDict(self, card):
        if card is None:
            return {"id": -1, "cost": 0, "power": 0}
        return {
            "id":self.CARD_NAME_TO_ID.get(card.name, -1),
            "cost": card.cur_cost,
            "power": card.cur_power}

    def calculateRewards(self):
        player1count, player2count = 0, 0
        for location in self.gm.locationList.values():
            if location.winning == "Ally":
                player1count += 1
            elif location.winning == "Enemy":
                player2count += 1
        reward = {"player_1": player1count, "player_2": player2count}
        return reward
    def step(self, actions):
        rewards = {agent: 0 for agent in self.agents}
        terminations = {agent: False for agent in self.agents}
        truncations = {agent: False for agent in self.agents}
        infos = {agent: {} for agent in self.agents}
        print(actions)
        for agent, agent_actions in actions.items():
            for action in agent_actions:
                if action == self.pass_action:
                    if agent == "player_2":
                        self.gm.turnEnd(True)
                        rewards = self.calculateRewards()
                        if self.gm.game_end:
                            terminations = {agent: True for agent in self.agents}
                            break
                        break
                print(action)
                cardidx, locationidx = self.decode_action(action)
                current_hand = self.gm.getHand(agent=agent)
                if cardidx > len(current_hand) - 1:
                    continue
                card = current_hand[cardidx]
                if agent == "player_1":
                    ally = True
                    if card.cost <= self.gm.status["allyenergy"]:
                        result = self.gm.addUnit(card, ally, self.gm.locationList[f"location{locationidx+1}"].locationNum)
                        if result:
                            self.gm.status["allyenergy"] -= card.cost
                elif agent == "player_2":
                    ally = False
                    if card.cost <= self.gm.status["enemyenergy"]:
                        result = self.gm.addUnit(card, ally, self.gm.locationList[f"location{locationidx+1}"].locationNum)
                        if result:
                            self.gm.status["enemyenergy"] -= card.cost
                if self.gm.game_end:
                    terminations = {agent: True for agent in self.agents}
                    break
        observations = {agent: self.observe(agent) for agent in self.agents}
        self.agents = [] if all(terminations.values()) else self.agents
        self.render()
        return observations, rewards, terminations, truncations, infos
    
    def observe(self, agent):
        hand = self.gm.getHand(agent=agent)
        obs_hand = [self.fromCardToDict(card) for card in hand]  # Rimosso `{}` esterno inutile

        obs_locations = {}  # raccogli tutte le location

        for locnum in range(3):
            loc = self.gm.locationList["location" + str(locnum + 1)]
            if agent == "player_1":
                obs_locations[f"location{locnum+1}"] = {
                    "ally_power": loc.alliesPower,
                    "enemy_power": loc.enemiesPower,
                    "ally_cards": [self.fromCardToDict(card) for card in loc.allies],
                    "ally_cards_pre_reveal": [self.fromCardToDict(card) for card in loc.preRevealAllies],
                    "enemy_cards": [self.fromCardToDict(card) for card in loc.enemies],
                }
            elif agent == "player_2":
                # Inverti le prospettive
                obs_locations[f"location{locnum+1}"] = {
                    "ally_power": loc.enemiesPower,
                    "enemy_power": loc.alliesPower,
                    "ally_cards": [self.fromCardToDict(card) for card in loc.enemies],
                    "ally_cards_pre_reveal": [self.fromCardToDict(card) for card in loc.preRevealEnemies],
                    "enemy_cards": [self.fromCardToDict(card) for card in loc.allies],
                }

        return {
            "hand": obs_hand,
            "energy": self.gm.status["allyenergy"] if agent == "player_1" else self.gm.status["enemyenergy"],
            "turn": self.gm.status["turncounter"],
            "locations": obs_locations
        }

    def render(self):
        print(self.gm.boardStatus())
            