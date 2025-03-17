import asyncio
import os
import typing as t

import aiohttp

import utils

#Se descarga una sola imagen de forma asíncrona
async def download_and_save_pokemon(session: aiohttp.ClientSession, pokemon: dict, output_dir: str):
    async with session.get(pokemon["Sprite"]) as response:
        if response.status == 200:
            content = await response.read()
        else:
            content = None
    if content is not None:
        target_dir = os.path.join(output_dir, pokemon["Type1"])
        utils.maybe_create_dir(target_dir)
        filepath = os.path.join(target_dir, pokemon["Pokemon"] + ".png")
        utils.write_binary(filepath, content)


#Preparar la descarga de imágenes
async def async_main_inner(output_dir: str, inputs: t.List[str]):
    utils.maybe_create_dir(output_dir)
    pokemons = list(utils.read_pokemons(inputs))
    async with aiohttp.ClientSession() as session:
        tasks = [
            download_and_save_pokemon(session, pokemon, output_dir)
            for pokemon in pokemons
        ]
        await asyncio.gather(*tasks)

#Inicializador de eventos asíncronos
@utils.timeit
def main(output_dir: str, inputs: t.List[str]):
    asyncio.run(async_main_inner(output_dir, inputs))
