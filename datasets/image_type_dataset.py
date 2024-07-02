import json
import torch

from torch.utils.data import Dataset
from torchvision.transforms import v2 as transforms
from torchvision.io import read_image, ImageReadMode
from utils.constants import data_path, cuda_device, Orientation, Gender, Game
from utils.functions import encode_type, get_sprite_paths, try_search_dict


class ImageTypeDataset(Dataset):
    def __init__(self):
        with open(data_path / "pokemon_full.json") as f:
            pokemons = json.load(f)

        self.images = []
        self.types = []

        orientations = [Orientation.FRONT, Orientation.BACK]
        genders = [Gender.MALE, Gender.FEMALE]
        shinys = [False, ]
        games = [Game.RUBY_SAPPHIRE, Game.EMERALD, Game.FIRERED_LEAFGREEN, Game.DIAMOND_PEARL, Game.PLATINUM,
                 Game.HEARTGOLD_SOULSILVER, Game.BLACK_WHITE, Game.X_Y, Game.OMEGARUBY_ALPHASAPPHIRE,
                 Game.ULTRASUN_ULTRAMOON, Game.DREAM_WORLD, Game.HOME, Game.OFFICIAL_ARTWORK, Game.SHOWDOWN,
                 Game.GEN7_ICONS, Game.GEN8_ICONS]
        sprite_paths = get_sprite_paths(orientations, genders, shinys, games)

        for pokemon in pokemons:
            # get encoded type
            encoded_type = encode_type([_type["type"]["name"] for _type in pokemon["types"]])
            encoded_type = torch.tensor(encoded_type, dtype=torch.float)
            encoded_type = encoded_type.to(cuda_device)

            for sprite_path in sprite_paths:
                # skip if pokemon does not have a sprite
                sprite_url, _ = try_search_dict(pokemon, sprite_path)
                if sprite_url is None:
                    print(f"Skipping {pokemon["name"]} (no. {pokemon["id"]}) {sprite_path}: No sprite.")
                    continue

                # check file has been downloaded
                image_path = data_path.joinpath(*sprite_path) / f"{pokemon["id"]}.png"
                if not image_path.is_file():
                    raise FileNotFoundError(image_path)

                # get image tensor
                image = read_image(image_path, ImageReadMode.RGB_ALPHA)

                image_transforms = transforms.Compose([
                    transforms.Resize((64, 64)),
                    transforms.ToDtype(torch.float, True),
                    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
                ])

                image = image_transforms(image).to(cuda_device)

                # add to dataset
                self.images.append(image)
                self.types.append(encoded_type)

    def __len__(self):
        return len(self.images)

    def __getitem__(self, index):
        transformer = transforms.RandomAffine((0, 360), (0.0, 0.25), (0.75, 1.25))
        return transformer(self.images[index]), self.types[index]
