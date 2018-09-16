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

print('Subtype distribution:')
print(cards.Subtype.value_counts())

print('X shape:')
print(X.shape)

print('Y shape:')
print(y.shape)

clf1 = svm.SVC(C=1.0, cache_size=500, kernel='linear')
clf2 = RandomForestClassifier(n_estimators=500, max_depth=None, min_samples_split=2, random_state=0, max_features=2)
clf3 = MLPClassifier(solver='lbfgs', alpha=1e-6, hidden_layer_sizes=(5, 2), random_state=1)
voting = VotingClassifier(estimators=[('svc', clf1), ('rf', clf2), ('mlp', clf3), ], voting='hard')
for clf, label in zip(
        [clf1, clf2, clf3, voting],
        ['Support Vector Machine', 'Random Forest', 'Multi-Layer Perceptron', 'Voting Ensemble']
):
    scores = cross_val_score(clf, X, y, cv=5, scoring='accuracy')
    print("Accuracy: %0.2f (+/- %0.2f) [%s]" % (scores.mean(), scores.std(), label))

'''
Subtype distribution:
Basic       222
Stage 1     166
Stage 2      59
Level Up      2
Name: Subtype, dtype: int64
X shape:
(449, 7)
Y shape:
(449,)
Accuracy: 0.90 (+/- 0.03) [Support Vector Machine]
Accuracy: 0.89 (+/- 0.04) [Random Forest]
Accuracy: 0.86 (+/- 0.04) [Multi-Layer Perceptron]
Accuracy: 0.90 (+/- 0.04) [Voting Ensemble]
'''
