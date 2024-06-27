import json
import torch

from torch.utils.data import Dataset
from torchvision.transforms import v2 as transforms
from torchvision.io import read_image, ImageReadMode
from utils.constants import data_path, cuda_device
from utils.functions import encode_type


class ImageTypeDataset(Dataset):
    def __init__(self):
        with open(data_path / "pokemon_full.json") as f:
            pokemons = json.load(f)

        self.images = []
        self.types = []

        for pokemon in pokemons:
            # skip if pokemon does not have a sprite
            if pokemon["sprites"]["front_default"] is None:
                print(f"Skipping {pokemon["name"]} (no. {pokemon["id"]}): No sprite.")
                continue

            # get image tensor
            image_path = data_path / "sprites" / "front_default" / f"{pokemon["id"]}.png"
            image = read_image(image_path, ImageReadMode.RGB)

            image_process = transforms.Compose([
                transforms.Resize((80, 80)),
                transforms.ToDtype(torch.float, True),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
            ])

            # get encoded type
            encoded_type = encode_type([_type["type"]["name"] for _type in pokemon["types"]])
            encoded_type = torch.tensor(encoded_type, dtype=torch.float)

            # send to gpu
            image = image.to(cuda_device)
            encoded_type = encoded_type.to(cuda_device)

            # add to dataset
            self.images.append(image)
            self.types.append(encoded_type)

    def __len__(self):
        return len(self.images)

    def __getitem__(self, index):
        return self.images[index], self.types[index]


def augment_image(image: torch.Tensor, n: int = 10) -> list[torch.Tensor]:
    transformer = transforms.RandomAffine((0, 360), (0.0, 0.25), (0.75, 1.25))
    return [transformer(image) for _ in range(n)]