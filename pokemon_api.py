#!/usr/bin/env python3
'''
    pokemon_api.py
    Veronica Child, Amanda Klein
	11 April 2016

    An assignment for CS 257 Software Design. Retrieves results
    from an HTTP-based API, PokeAPI, parses the results (JSON in this case),
    and manages the potential errors.

'''

import sys
import argparse
import json
import urllib.request


def get_pokemon():
	'''
	Returns a list of all the pokemon (811).
	
	'''
	# Pokemon each has an ID. Offset specifies what pokemon ID to start with. 
	# Limit specifies what pokemon ID to end with (811 Pokemon in database).
	url = 'http://pokeapi.co/api/v2/pokemon/?limit=811&offset=1'
	
	try:
		req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
		data_from_server = urllib.request.urlopen(req).read()
		string_from_server = data_from_server.decode('utf-8')
		#Loads a dictionary from API server
		pokemon_dict = json.loads(string_from_server)
	except Exception as e:
		# Problems with network access of JSON parsing.
		print("Cannot list Pokémon")
		return []

	result_list = []
	
	pokemon_list = pokemon_dict['results']
	for pokemon in pokemon_list:
		name = pokemon['name']
		if type(name) != type(''):
			raise Exception('Pokemon name has no type: "{0}"'.format(name))		
		result_list.append(name)
	
	return sorted(result_list)	


def get_abilities(pokemon):
	'''
	Returns a list of the abilities of the pokemon given.
	
	'''
	base_url = 'http://pokeapi.co/api/v2/pokemon/{0}'
	url = base_url.format(pokemon)
	
	try:		
		#data_from_server = urllib.request.urlopen(url).read()
		req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
		data_from_server = urllib.request.urlopen(req).read()
		string_from_server = data_from_server.decode('utf-8')
		#Loads a dictionary from API server
		pokemon_data = json.loads(string_from_server)
	
	except Exception as e:
		# Problems with network access of JSON parsing.
		print("Network error access or {0} is not a Pokémon. "
		"Please enter a valid Pokémon name".format(pokemon))
		return []
	
	result_list = []
	
	# Indexes into list of dictionaries for PokemonAbility
	ability_list = pokemon_data['abilities']
	for ability_info in ability_list:
		if ability_info['is_hidden'] == True:
			ability = ability_info['ability']['name']
			result_list.append({'Name': ability + ' (Hidden Ability)'})
		else:
			ability = ability_info['ability']['name']
			result_list.append({'Name': ability})	
	
	if type(ability) != type(''):
		raise Exception('Ability has no type: "{0}"'.format(ability))	
	return result_list

def get_traits(pokemon):
	'''
	Returns a list of traits of the pokemon given, including
	base experience, height, weight, species, type(s), abilities, 
	and locations where the pokemon might be found.
	
	'''
	
	base_url = 'http://pokeapi.co/api/v2/pokemon/{0}'
	url = base_url.format(pokemon)
	
	try:		
		req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
		data_from_server = urllib.request.urlopen(req).read()
		string_from_server = data_from_server.decode('utf-8')
		#Recieves a dictionary from API server
		pokemon_data = json.loads(string_from_server)
	
	except Exception as e:
		# Problems with network access of JSON parsing.
		print("{0} is not a Pokémon. Please enter a valid Pokémon name".format(pokemon))
		return []
		
	result_list = []
	
	# Accesses base_experience integer
	base_experience = pokemon_data['base_experience']
	result_list.append('Base Experience: ' + str(base_experience))
	
	# Accesses height integer
	height = pokemon_data['height']
	result_list.append('Height: ' + str(height))
	
	# Accesses weight integer
	weight = pokemon_data['weight']
	result_list.append('Weight: ' + str(weight))
	
	# Accesses PokemonSpecies resource, which is a dictionary,
	# then indexes into dict to find name of species
	species_dict = pokemon_data['species']
	species = species_dict['name']
	result_list.append('Species: ' + species)
	
	# Accesses list of dictionaries PokemonType,
	# indexes into dict to find name of type
	type_list = pokemon_data['types']
	result_list.append('Type(s) of this Pokémon: ')
	for type_info in type_list:
		type = type_info['type']['name']
		result_list.append(type)

	# Calls get_abilities method to print out abilities for the Pokémon given
	abilities = get_abilities(args.pokemon)
	result_list.append('Abilities of this Pokémon: ')
	for ability in abilities:
		action = ability['Name']
		result_list.append('{0}'.format(action))
	
	# Accesses list of dictionaries of possible locations in 
	# which the Pokémon can be found, indexes into dict to find name of location
	location_list = pokemon_data['location_area_encounters']
	result_list.append('Location areas this Pokémon can be found in: ')
	for location_info in location_list:
		location = location_info['location_area']['name']
		result_list.append(location)
	
	return result_list

def main(args):
	if (args.action == 'list') & (args.pokemon == 'pokemon'):
		pokemon_list = get_pokemon()
		for pokemon in pokemon_list:
			print(pokemon)
	elif args.action == 'abilities':
		ability_list = get_abilities(args.pokemon)
		for ability in ability_list:
			action = ability['Name']
			print('{0}'.format(action))
	elif args.action == 'traits':
		traits = get_traits(args.pokemon)
		for trait in traits:
			print(trait)

if __name__ == '__main__':
	
	# Use argeparse to parse command line
	parser = argparse.ArgumentParser(description='Get Pokémon info from the PokeAPI')

	parser.add_argument('action',
		                metavar='action', #cleans usage statement
	                    #helps user understand the program
		                help='type of data request on the Pokémon',
		                choices=['abilities', 'list', 'traits'])
	
	parser.add_argument('pokemon', help='the Pokémon you want info on')

	args = parser.parse_args()
	main(args)	