# Questions

## What does the data look like?
See the python notebook [exploratory_data_analysis.ipynb](../analysis/exploratory_data_analysis.ipynb) for some basic Exploratory Data Analysis (EDA). This notebook is to get a feel of the distribution of the data.

TODO: does this help us in our overall goal?

## Can we classify a Pokémon Subtype?

A Pokémon subtype falls into one of:

* Basic
* Stage 1
* Stage 2
* and some others, like MEGA

Note that you can evolve a Pokémon: Basic -> Stage 1 -> Stage 2, where, generally speaking, the higher the evolution, the more powerful the Pokémon is in terms of HP, Attacks and Abilities.
 
As a warmup exercise to our goal of creating the best deck, here is a question: Given some features of a Pokémon card, can we predict it's subtype?

TODO: does this help us in our overall goal?

To transform our data into a tabular format, run: [build_subtype_dataset.py](../utilities/build_subtype_dataset.py). This python script will do a simple query for all Pokémon cards, and write to a CSV file in the ../data_extract directory.

To answer our question, I built several classifiers using sci-kit learn, and then also an ensemble voting classifier, in file: [predict_subtype.py](../analysis/predict_subtype.py).

TODO: why did you pick these classifier algorithms?

TODO: how did you tune or select parameters?

Results were decent, but not super, the Voting Ensemble of SVM, Random Forest and MLP, performing the best:

```
Accuracy: 0.87 (+/- 0.05) [Support Vector Machine]
Accuracy: 0.88 (+/- 0.04) [Random Forest]
Accuracy: 0.84 (+/- 0.07) [Multi-Layer Perceptron]
Accuracy: 0.89 (+/- 0.05) [Voting Ensemble]
```

TODO: how to interpret the results? what metrics do you use to compare?

## Can we predict HP?

TODO: fix link below

Another thing we can attempt with this data set is to predict HP given values for Weakness total, Retreat Cost, Total of all Attack Energy Costs. Even though HP are in increments of 10, we will consider them as continuous, when building a regression model in ```analysis/predict_hp.py```.

TODO: how did you pick which algorithm to try?

Using R squared and MSE, we can evaluate a few different models:

```
R squared: 0.86, MSE: 86.22, [Linear Regression]
R squared: 0.86, MSE: 88.13, [Gradient Boosting Regressor]
R squared: 0.86, MSE: 87.59, [Support Vector Regression]
```

TODO: how to interpret the results? what metrics do you use to compare?

These are very close, with Linear Regression giving the best model.

