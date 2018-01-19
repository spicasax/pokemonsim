# Introduction
My son loves Pokémon TCG (trading card game) a lot. At first, it was just about collecting them, but as he got older, we started playing the game together, and I like it now too. Lately, I've heard him say things like, "I've just put together a new deck, and it is my best deck yet!" This made me think, how do you determine the best Pokémon deck? What makes a deck win more? These are questions I want to answer with data.

# Set up
1. Please clone or download the zip from https://github.com/PokemonTCG/pokemon-tcg-data to your local git directory.
2. Install MongoDB.
3. Run database/init_cards_mongodb.py to load the cards into MongoDB.

# Questions

## Can we classify a Pokémon Subtype?

A Pokémon subtype falls into one of:

```['BREAK' 'Basic' 'EX' 'GX' 'LEGEND' 'Level Up' 'MEGA' 'Restored' 'Stage 1'
 'Stage 2']```
 
As a warmup exercise to our goal of creating the best deck, here is a question: Given some features of a Pokémon card, can we predict it's subtype?

To transform our data into a tabular format, run: ```utilities/build_subtype_dataset.py```

To answer the question, I built several classifiers, and then also an ensemble voting classifier, in file: ```analysis/predict_subtype.py```

Results were decent, but not super:

```
Accuracy: 0.87 (+/- 0.05) [Support Vector Machine]
Accuracy: 0.88 (+/- 0.04) [Random Forest]
Accuracy: 0.84 (+/- 0.07) [Multi-Layer Perceptron]
Accuracy: 0.89 (+/- 0.05) [Voting Ensemble]
```

