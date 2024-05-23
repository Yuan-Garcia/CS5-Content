#don't forget to pip install
import requests
yourPokemon = "ditto"
# check out the documentation here! 
# https://pokeapi.co/docs/v2#pokemon-section
response = requests.get("https://pokeapi.co/api/v2/pokemon/ditto/")# + yourPokemon + "/")
print(response.json())
# now look at the documentation https://pokeapi.co/docs/v2#pokemon and see what that large JSON (really large dictionary) output actually means!

# change some of the data to make it unbeatable in a pokemon battle!

# make your own pokemon!