import requests
yourPokemon = "ditto"
# check out the documentation here! 
# https://pokeapi.co/docs/v2#pokemon-section
response = requests.get("https://pokeapi.co/api/v2/pokemon/ditto/")# + yourPokemon + "/")
print(response.json())
#