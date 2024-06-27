import torch

from enum import StrEnum, Enum
from pathlib import Path


project_path = Path(r"C:\Users\jaket\PycharmProjects\ai_pokemon")
data_path = project_path / "data"
datasets_path = project_path / "datasets"
models_path = project_path / "models"

cuda_device = torch.device("cuda")


class Gender(Enum):
    MALE = 1
    FEMALE = 2


class Orientation(StrEnum):
    FRONT = "front"
    BACK = "back"


class Game(StrEnum):
    NONE = ""
    RED_BLUE = "red-blue"
    YELLOW = "yellow"
    GOLD = "gold"
    SILVER = "silver"
    CRYSTAL = "crystal"
    RUBY_SAPPHIRE = "ruby-sapphire"
    EMERALD = "emerald"
    FIRERED_LEAFGREEN = "firered-leafgreen"
    DIAMOND_PEARL = "diamond-pearl"
    PLATINUM = "platinum"
    HEARTGOLD_SOULSILVER = "heartgold-soulsilver"
    BLACK_WHITE = "black-white"
    X_Y = "x-y"
    OMEGARUBY_ALPHASAPPHIRE = "omegaruby-alphasapphire"
    ULTRASUN_ULTRAMOON = "ultra-sun-ultra-moon"
    DREAM_WORLD = "dream_world"
    HOME = "home"
    OFFICIAL_ARTWORK = "official-artwork"
    SHOWDOWN = "showdown"
    GEN7_ICONS = "gen7"
    GEN8_ICONS = "gen8"
