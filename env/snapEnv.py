from pettingzoo import ParallelEnv
from gymnasium import spaces
import numpy as np
from gameManager import GameState

class SnapEnv(ParallelEnv):
    metadata = {"render.modes": ["human"], "name":"marvel_snap_v0"}

    def __init__(self):
        super().__init__()
        self.possible_agents = ["player_1", "player_2"]
        self.agents = self.possible_agents[:]
        self.gm = GameState()
        self.gm.reset()
    
    def observation_space(self):
        max_hand_size = 7
        card_feature_size = 3

card_name = [
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