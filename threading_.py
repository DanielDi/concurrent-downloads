import os
import typing as t
import requests
import concurrent.futures

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
    utils.maybe_create_dir(output_dir)
    pokemons = list(utils.read_pokemons(inputs))
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(download_and_save_pokemon, pokemon, output_dir) for pokemon in pokemons]
        #Esperar que finalicen las tareas
        concurrent.futures.wait(futures)
