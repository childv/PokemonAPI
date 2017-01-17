# PokemonAPI
This repository processes data from the Pokeapi API into something the viewer can easily read.

An assignment for CS 257 Software Design. Retrieves results from an HTTP-based API, PokeAPI, parses the results (JSON in this case), and manages the potential errors.

# Usage
Query the abilities and traits of a specified pokemon, and get a list of all the pokemon in the API.

In order to run this program, call from the command line.

Example:  python3 api_test.py traits pikachu

list | abilities | traits (required) Specifies which function you want to run.

    list - Coupled with argument "pokemon", will list all 811 Pokémon
    abilities - Gives a list of abilities for specified Pokémon
    traits - Gives a list of traits for specified Pokémon
