import json
import os
import requests
import time

from pathlib import Path
from typing import Any
from utils.constants import Orientation, Gender, Game
from utils.functions import get_sprite_path, try_search_dict


def get_pokemon_data(id_or_name: int | str) -> dict[str, Any]:
    api_url = f"https://pokeapi.co/api/v2/pokemon/{id_or_name}/"
    response = requests.get(api_url)
    return response.json() if response.status_code == 200 else None


def download_basic_pokemon_data() -> None:
    api_url = "https://pokeapi.co/api/v2/pokemon/"
    response = requests.get(api_url)
    pokemon_count = response.json()["count"] if response.status_code == 200 else 0

    pokemons = []
    while len(pokemons) < pokemon_count:
        time.sleep(1)
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            pokemons.extend(data["results"])
            api_url = data["next"]
        else:
            print(f"Download failed. Status code: {response.status_code}.")
            break

    s = json.dumps(pokemons)
    with open("data/pokemon.json", "w") as f:
        f.write(s)


def download_full_pokemon_data() -> None:
    # download basic pokemon data if necessary
    basic_pokemon_data_path = Path("data/pokemon.json")
    if not basic_pokemon_data_path.exists():
        download_basic_pokemon_data()

    # get basic pokemon data
    with open(basic_pokemon_data_path) as f:
        pokemons = json.load(f)

    # download full pokemon data from basic pokemon data
    pokemons_full = []
    for pokemon in pokemons:
        time.sleep(1)
        response = requests.get(pokemon["url"])
        if response.status_code == 200:
            data = response.json()
            pokemons_full.append(data)
        else:
            print(f"Download failed. Status code: {response.status_code}.")
            break

    s = json.dumps(pokemons_full)
    with open("data/pokemon_full.json", "w") as f:
        f.write(s)


def download_pokemon_sprites(orientation: Orientation = Orientation.FRONT,
                             gender: Gender = Gender.MALE,
                             shiny: bool = False,
                             game: Game = Game.NONE) -> None:
    # download full pokemon data if necessary
    full_pokemon_data_path = Path("data/pokemon_full.json")
    if not full_pokemon_data_path.exists():
        download_full_pokemon_data()

    # get full pokemon data
    with open(full_pokemon_data_path) as f:
        pokemons_full = json.load(f)

    sprite_path = get_sprite_path(orientation, gender, shiny, game)
    dir_path = Path(f"data/{"/".join(sprite_path)}/")
    dir_path.mkdir(parents=True, exist_ok=True)
    print(f"Downloading data to {dir_path}...")

    for pokemon in pokemons_full:
        sprite_url, _ = try_search_dict(pokemon, sprite_path)
        if not sprite_url:
            print(f"No sprite URL provided for {pokemon["name"]}.")
            continue
        file_path = dir_path / f"{pokemon["id"]}.png"
        if os.path.exists(file_path):
            print(f"Sprite for {pokemon["name"]} already downloaded.")
            continue
        time.sleep(1)
        response = requests.get(sprite_url)
        if response.status_code == 200:
            with open(file_path, "wb") as f:
                f.write(response.content)
            print(f"{pokemon["name"]} sprite downloaded successfully.")
        else:
            print(f"Could not download sprite for {pokemon["name"]}.")
            continue


def download_all_pokemon_sprites() -> None:
    for orientation in Orientation:
        for gender in Gender:
            for shiny in [True, False]:
                for game in Game:
                    download_pokemon_sprites(orientation, gender, shiny, game)
