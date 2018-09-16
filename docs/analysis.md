# Questions

## What does the data look like?
See the python notebook [exploratory_data_analysis.ipynb](../analysis/exploratory_data_analysis.ipynb) for some basic Exploratory Data Analysis (EDA). This notebook helps us get a feel of the distribution of the data.


## Can we classify a Pokémon Subtype?

A Pokémon subtype falls into one of:

* Basic
* Stage 1
* Stage 2
* and some others, like MEGA

Note that you can evolve a Pokémon: Basic -> Stage 1 -> Stage 2, where, generally speaking, the higher the evolution, the more powerful the Pokémon is in terms of HP, Attacks and Abilities.
 
As a warmup exercise to our goal of creating the best deck, here is a question: Given some features of a Pokémon card, can we predict it's subtype? Doing this helps us get a feel for the data as well, as well as practice classification techniques, but the value of this exercise may not go much beyond an exploration. I'm not sure how useful this exercise will be in the long term.

To transform our data into a tabular format, run: [build_subtype_dataset.py](../utilities/build_subtype_dataset.py). This python script will do a simple query for all Pokémon cards, and write to a CSV file in the ../data_extract directory.

For this effort, I built several classifiers using sci-kit learn, and then also an ensemble voting classifier, in file: [predict_subtype.py](../analysis/predict_subtype.py). I chose Random Forest primarily because I have more experience with it, and chose Support Vector Machine and Multi-Layer Perceptron so I could learn more about these classifiers.

For tuning these, I probably should have done a grid search, but since these didn't take long to train, I ended up manually fiddling with the parameters. Note that for the Random Forest, the default number of trees for the classifier is 10, but my personal experience has shown that 100 or 500 is a better choice.

Results were pretty decent, with the SVM and the Voting Ensemble both performing the best:

```
Accuracy: 0.90 (+/- 0.03) [Support Vector Machine]
Accuracy: 0.89 (+/- 0.04) [Random Forest]
Accuracy: 0.86 (+/- 0.04) [Multi-Layer Perceptron]
Accuracy: 0.90 (+/- 0.04) [Voting Ensemble]
```

Note that I chose accuracy as my metric for comparison. Since I don't really have a use case, I can't really associate a cost with the types of errors the classifier could make, and I wouldn't be able to say if precision or recall would be more important, for example.

## Can we predict HP?

TODO: fix link below

Another thing we can attempt with this data set is to predict HP given values for Weakness total, Retreat Cost, Total of all Attack Energy Costs. Even though HP are in increments of 10, we will consider them as continuous, when building a regression model in [predict_hp.py](../analysis/predict_hp.py).

TODO: how did you pick which algorithm to try?

Using R squared and MSE, we can evaluate a few different models:

```
R squared: 0.86, MSE: 86.22, [Linear Regression]
R squared: 0.86, MSE: 88.13, [Gradient Boosting Regressor]
R squared: 0.86, MSE: 87.59, [Support Vector Regression]
```

TODO: how to interpret the results? what metrics do you use to compare?

These are very close, with Linear Regression giving the best model.

