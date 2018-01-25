# Introduction
My son loves Pokémon TCG (trading card game) a lot. At first, it was just about collecting the cards, but as he got older, we started playing the game together, and I like it now too. Lately, I've heard him say things like, "I've just put together a new deck, and it is my best deck yet!" This made me think, how do you determine the best Pokémon deck? What makes a deck win more? Here are some questions I want to answer with data:

1. Can we predict a Pokémon subtype (e.g., Basic, Stage 1, Stage 2, etc.)?
2. Can we predict HP?
3. Can we predict type (e.g., Grass, Fire, Fighting, etc.)?
4. Is there a strongest type?
5. Can we build a winning-est deck?

# Set up
1. Please clone or download the zip from https://github.com/PokemonTCG/pokemon-tcg-data to your local git directory. This is an awesome database of Pokémon TCG.
2. Install MongoDB.
3. Run ```database/init_cards_mongodb.py``` to load the cards into MongoDB.

# Analysis	
Please see: [analysis.md](docs/analysis.md)