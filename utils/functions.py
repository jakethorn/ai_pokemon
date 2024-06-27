from typing import Any, Tuple, Sequence
from utils.constants import Orientation, Gender, Game


def search_dict(d: dict[str, Any], terms: Sequence[str]) -> Any:
    """
    Recursively searches a dictionary using a series of terms.
    """
    if len(terms) > 0:
        return search_dict(d[terms[0]], terms[1:])
    else:
        return d


def try_search_dict(d: dict[str, Any], terms: Sequence[str]) -> Tuple[Any, bool]:
    try:
        return search_dict(d, terms), True
    except KeyError:
        return None, False


def get_sprite_path(orientation: Orientation = Orientation.FRONT,
                    gender: Gender = Gender.MALE,
                    shiny: bool = False,
                    game: Game = Game.NONE) -> list[str]:
    """
    Get sprite path.
    """
    # path base
    path = ["sprites"]
    # construct sprite directory
    if game in [Game.DREAM_WORLD, Game.HOME, Game.OFFICIAL_ARTWORK, Game.SHOWDOWN]:
        path.extend(["other", game])
    elif game in [Game.RED_BLUE, Game.YELLOW]:
        path.extend(["versions", "generation-i", game])
    elif game in [Game.GOLD, Game.SILVER, Game.CRYSTAL]:
        path.extend(["versions", "generation-ii", game])
    elif game in [Game.RUBY_SAPPHIRE, Game.EMERALD, Game.FIRERED_LEAFGREEN]:
        path.extend(["versions", "generation-iii", game])
    elif game in [Game.DIAMOND_PEARL, Game.PLATINUM, Game.HEARTGOLD_SOULSILVER]:
        path.extend(["versions", "generation-iv", game])
    elif game == Game.BLACK_WHITE:
        path.extend(["versions", "generation-v", game])
    elif game in [Game.X_Y, Game.OMEGARUBY_ALPHASAPPHIRE]:
        path.extend(["versions", "generation-vi", game])
    elif game == Game.ULTRASUN_ULTRAMOON:
        path.extend(["versions", "generation-vii", game])
    elif game == Game.GEN7_ICONS:
        path.extend(["versions", "generation-vii", "icons"])
    elif game == Game.GEN8_ICONS:
        path.extend(["versions", "generation-viii", "icons"])
    # construct sprite name
    key = orientation
    if shiny:
        key += "_shiny"
    if gender == Gender.FEMALE:
        key += "_female"
    if not shiny and gender == Gender.MALE:
        key += "_default"
    path.append(key)
    return path


def get_sprite_paths(orientations: Sequence[Orientation] = (Orientation.FRONT, ),
                     genders: Sequence[Gender] = (Gender.MALE, ),
                     shinys: Sequence[bool] = (False, ),
                     games: Sequence[Game] = (Game.NONE, )) -> list[list[str]]:
    paths = []
    for orientation in orientations:
        for gender in genders:
            for shiny in shinys:
                for game in games:
                    paths.append(get_sprite_path(orientation, gender, shiny, game))
    return paths


def get_all_sprite_paths() -> list[list[str]]:
    return get_sprite_paths(
        (Orientation.FRONT, Orientation.BACK),
        (Gender.MALE, Gender.FEMALE),
        (True, False),
        (Game.RED_BLUE, Game.YELLOW, Game.GOLD, Game.SILVER, Game.CRYSTAL, Game.RUBY_SAPPHIRE, Game.EMERALD,
         Game.FIRERED_LEAFGREEN, Game.DIAMOND_PEARL, Game.PLATINUM, Game.HEARTGOLD_SOULSILVER, Game.BLACK_WHITE,
         Game.X_Y, Game.OMEGARUBY_ALPHASAPPHIRE, Game.ULTRASUN_ULTRAMOON, Game.DREAM_WORLD, Game.HOME,
         Game.OFFICIAL_ARTWORK, Game.SHOWDOWN, Game.GEN7_ICONS, Game.GEN8_ICONS)
    )


def encode_type(types: Sequence[str]) -> list[int]:
    """
    One hot encodes pokemon types.
    E.g., [grass, poison] -> [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0]
    """
    type_indices = {
        "normal": 0,
        "fighting": 1,
        "flying": 2,
        "poison": 3,
        "ground": 4,
        "rock": 5,
        "bug": 6,
        "ghost": 7,
        "steel": 8,
        "fire": 9,
        "water": 10,
        "grass": 11,
        "electric": 12,
        "psychic": 13,
        "ice": 14,
        "dragon": 15,
        "dark": 16,
        "fairy": 17
    }

    encoding = [0] * len(type_indices)
    for _type in types:
        encoding[type_indices[_type]] = 1

    return encoding
