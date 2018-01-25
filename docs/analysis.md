# Questions

## What does the data look like?
See ```analysis/exploratory_data_analysis.ipynb```.

## Can we classify a Pokémon Subtype?

A Pokémon subtype falls into one of:

```
['BREAK' 'Basic' 'EX' 'GX' 'LEGEND' 'Level Up' 'MEGA' 'Restored' 'Stage 1'
 'Stage 2']
```
 
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

## Can we predict HP?

Another thing we can attempt with this data set is to predict HP given values for Weakness total, Retreat Cost, Total of all Attack Energy Costs. Even though HP are in increments of 10, we will consider them as continuous, when building a regression model in ```analysis/predict_hp.py```.

Using R squared and MSE, we can evaluate a few different models:

```
R squared: 0.86, MSE: 86.22, [Linear Regression]
R squared: 0.86, MSE: 88.13, [Gradient Boosting Regressor]
R squared: 0.86, MSE: 87.59, [Support Vector Regression]
```

These are very close, with Linear Regression giving the best model.

## Can we simulate one-on-one battles?
As a very basic way to play, kids sometimes will just battle Pokemon one on one, without worrying about energies, trainers, etc. Can we randomly pit two Pokémon cards against each other?

In ```game/simulator.py```, we randomly select two Pokémon cards, simulate a battle against the two cards where attacks are chosen at random. We run 100 battles like this and calculate which Pokémon wins the most battles. 

Note that this is not a realistic game scenario, but it gets our feet wet in battle simulation.