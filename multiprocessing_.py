import os
import typing as t
import requests
import multiprocessing

import utils

def download_and_save_pokemon(pokemon: dict, output_dir: str):
    with requests.Session() as session:
        content = utils.maybe_download_sprite(session, pokemon["Sprite"])
    if content is not None:
        target_dir = os.path.join(output_dir, pokemon["Type1"])
        utils.maybe_create_dir(target_dir)
        filepath = os.path.join(target_dir, pokemon["Pokemon"] + ".png")
        utils.write_binary(filepath, content)


@utils.timeit
def main(output_dir: str, inputs: t.List[str]):
    # Crear directorio
    utils.maybe_create_dir(output_dir)
    pokemons = list(utils.read_pokemons(inputs))
    # Lista de tareas
    tasks = [(pokemon, output_dir) for pokemon in pokemons]
    with multiprocessing.Pool() as pool:
        pool.starmap(download_and_save_pokemon, tasks)
