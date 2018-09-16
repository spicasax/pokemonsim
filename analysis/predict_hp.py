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
                                      HP  RetreatCostCount  AttackCount  AttackConvertedEnergyCostTotal  WeaknessTotal  ResistanceTotal   Ability  StrongestDamage
HP                              1.000000          0.492049    -0.008730                        0.622477       0.912584              NaN  0.386493         0.712292
RetreatCostCount                0.492049          1.000000    -0.028344                        0.433707       0.376392              NaN  0.139320         0.367096
AttackCount                    -0.008730         -0.028344     1.000000                        0.445368      -0.054133              NaN -0.550093         0.076314
AttackConvertedEnergyCostTotal  0.622477          0.433707     0.445368                        1.000000       0.554961              NaN -0.024480         0.653237
WeaknessTotal                   0.912584          0.376392    -0.054133                        0.554961       1.000000              NaN  0.391766         0.660419
ResistanceTotal                      NaN               NaN          NaN                             NaN            NaN              NaN       NaN              NaN
Ability                         0.386493          0.139320    -0.550093                       -0.024480       0.391766              NaN  1.000000         0.256545
StrongestDamage                 0.712292          0.367096     0.076314                        0.653237       0.660419              NaN  0.256545         1.000000
"""


# Create our numpy arrays for our model based on most correlated features
X = cards[['WeaknessTotal', 'StrongestDamage', 'AttackConvertedEnergyCostTotal', 'RetreatCostCount']].values
y = cards.HP.values

# I've experimented and tweaked any parameters given here
clf1 = linear_model.LinearRegression()
clf2 = ensemble.GradientBoostingRegressor(n_estimators=500, max_depth=2, min_samples_split=2,
          learning_rate=0.01, loss='huber')
clf3 = svm.SVR(kernel='linear', C=5)

print('\nCalculate R squared and MSE for different regression models:')
for clf, label in zip(
        [clf1, clf2, clf3, ],
        ['Linear Regression', 'Gradient Boosting Regressor', 'Support Vector Regression']
):
    prediction = cross_val_predict(clf, X, y, cv=3)
    print("R squared: %0.3f, MSE: %0.2f, [%s]" % (r2_score(y, prediction), mean_squared_error(y, prediction), label))

"""
R squared: 0.867, MSE: 82.72, [Linear Regression]
R squared: 0.866, MSE: 83.52, [Gradient Boosting Regressor]
R squared: 0.865, MSE: 83.94, [Support Vector Regression]
"""

# Supposing we want to use the Linear Regression model (since it performed slightly better than the other two models),
# we would want to round any prediction to the nearest 10s for HP.
clf1.fit(X, y)
AttackConvertedEnergyCostTotal = 7
WeaknessTotal = 2
RetreatCostCount = 3
StrongestDamage = 80
pred = clf1.predict([[WeaknessTotal, StrongestDamage, AttackConvertedEnergyCostTotal,  RetreatCostCount],])
print("HP prediction for [WeaknessTotal, StrongestDamage, AttackConvertedEnergyCostTotal,  RetreatCostCount = [{0}, {1}, {2}, {3}] is: {4}".format(
    WeaknessTotal, StrongestDamage, AttackConvertedEnergyCostTotal, RetreatCostCount, round(pred[0],-1))
)