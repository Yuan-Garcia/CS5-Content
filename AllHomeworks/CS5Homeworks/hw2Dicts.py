import requests
yourPokemon = "ditto"
# check out the documentation here! 
# https://pokeapi.co/docs/v2#pokemon-section
response = requests.get("http://api.open-notify.org/astros")
print(response.json())