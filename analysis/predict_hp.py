import pandas as pd
import os
import warnings
from sklearn.model_selection import cross_val_predict
from sklearn import linear_model
from sklearn import svm
from sklearn import ensemble

from sklearn.metrics import r2_score, mean_squared_error

warnings.filterwarnings("ignore")
pd.set_option('display.max_columns', 500)
pd.set_option('display.expand_frame_repr', False)

THIS_PATH = os.getcwd()
PARENT_PATH  = os.path.dirname(THIS_PATH)
DATA_DIR = os.path.join(PARENT_PATH, 'data_extract')

cards = pd.read_csv(os.path.join(DATA_DIR, 'cards_by_subtype.csv'))

cards = cards.convert_objects(convert_numeric=True)

# We have some cards with missing HP values, we will drop them, as these are mostly some specialty cards
# in the HeartGold & SoulSilver set. See examples:
# https://images.pokemontcg.io/hgss1/112.png
# https://images.pokemontcg.io/hgss1/114.png
cards.dropna(inplace=True)

correlation = cards.corr()
print("Use Pearson Correlation to detect possible relationships:")
print(correlation)

"""
                                      HP  RetreatCostCount  AttackCount  AttackConvertedEnergyCostTotal  WeaknessTotal  ResistanceTotal   Ability
HP                              1.000000          0.489399     0.014008                        0.635734       0.912247              NaN  0.374742
RetreatCostCount                0.489399          1.000000    -0.012634                        0.444247       0.375604              NaN  0.126161
AttackCount                     0.014008         -0.012634     1.000000                        0.520531      -0.031761              NaN -0.537108
AttackConvertedEnergyCostTotal  0.635734          0.444247     0.520531                        1.000000       0.564241              NaN -0.048969
WeaknessTotal                   0.912247          0.375604    -0.031761                        0.564241       1.000000              NaN  0.381741
ResistanceTotal                      NaN               NaN          NaN                             NaN            NaN              NaN       NaN
Ability                         0.374742          0.126161    -0.537108                       -0.048969       0.381741              NaN  1.000000

"""


# Create our numpy arrays for our model based on most correlated features
X = cards[['AttackConvertedEnergyCostTotal', 'WeaknessTotal', 'RetreatCostCount']].values
y = cards.HP.values

# I've experimented and tweaked any parameters given here
clf1 = linear_model.LinearRegression()
clf2 = ensemble.GradientBoostingRegressor(n_estimators=500, max_depth=3, min_samples_split=2,
          learning_rate=0.01, loss='huber')
clf3 = svm.SVR(kernel='linear', C=5)

print('\nCalculate R squared and MSE for different regression models:')
for clf, label in zip(
        [clf1, clf2, clf3, ],
        ['Linear Regression', 'Gradient Boosting Regressor', 'Support Vector Regression']
):
    prediction = cross_val_predict(clf, X, y, cv=3)
    print("R squared: %0.2f, MSE: %0.2f, [%s]" % (r2_score(y, prediction), mean_squared_error(y, prediction), label))

"""
R squared: 0.86, MSE: 86.22, [Linear Regression]
R squared: 0.86, MSE: 88.15, [Gradient Boosting Regressor]
R squared: 0.86, MSE: 87.59, [Support Vector Regression]
"""

# Supposing we want to use the Linear Regression model (since it performed slightly better than the other two models),
# we would want to round any prediction to the nearest 10s for HP.
clf1.fit(X, y)
AttackConvertedEnergyCostTotal = 7
WeaknessTotal = 2
RetreatCostCount = 3
pred = clf1.predict([[AttackConvertedEnergyCostTotal, WeaknessTotal, RetreatCostCount],])
print("HP prediction for [AttackConvertedEnergyCostTotal, WeaknessTotal, RetreatCostCount] = [{0}, {1}, {2}] is: {3}".format(
    AttackConvertedEnergyCostTotal, WeaknessTotal, RetreatCostCount, round(pred[0],-1))
)