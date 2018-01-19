import pandas as pd
import os
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import VotingClassifier

import warnings
warnings.filterwarnings("ignore")

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

# Create our numpy arrays for our model
X = cards[['HP', 'RetreatCostCount', 'AttackCount', 'AttackConvertedEnergyCostTotal',
           'WeaknessTotal', 'ResistanceTotal', 'Ability']].values
y = cards.Subtype.values

print('X shape:')
print(X.shape)

print('Y shape:')
print(y.shape)

clf1 = svm.SVC(C=1)
clf2 = RandomForestClassifier(n_estimators=10, max_depth=None, min_samples_split=2, random_state=0)
clf3 = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
voting = VotingClassifier(estimators=[('svc', clf1), ('rf', clf2), ('mlp', clf3), ], voting='hard')
for clf, label in zip(
        [clf1, clf2, clf3, voting],
        ['Support Vector Machine', 'Random Forest', 'Multi-Layer Perceptron', 'Voting Ensemble']
):
    scores = cross_val_score(clf, X, y, cv=5, scoring='accuracy')
    print("Accuracy: %0.2f (+/- %0.2f) [%s]" % (scores.mean(), scores.std(), label))

'''
Accuracy: 0.87 (+/- 0.05) [Support Vector Machine]
Accuracy: 0.88 (+/- 0.04) [Random Forest]
Accuracy: 0.84 (+/- 0.07) [Multi-Layer Perceptron]
Accuracy: 0.89 (+/- 0.05) [Voting Ensemble]
'''
