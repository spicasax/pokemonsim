import os
from pymongo import MongoClient
import csv
import click

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.collocations import *
from nltk import FreqDist, Text, pos_tag

from nltk.tag.senna import SennaTagger

from os.path import expanduser
HOME = expanduser("~")
# point SennaTagger to the installation directory
st = SennaTagger(HOME+'/senna')

client = MongoClient()
db = client.pokemontcg

# we ended up not using this list of stopwords
stopwords_en = stopwords.words('english')

THIS_PATH = os.getcwd()
PARENT_PATH  = os.path.dirname(THIS_PATH)
DATA_DIR = os.path.join(PARENT_PATH, 'data_extract')

attack_text = []
with open(os.path.join(DATA_DIR,'attack_text.csv'),'w') as f:
    writer = csv.writer(f, delimiter=',')
    for card in db.cards.aggregate([
        {'$match': {"supertype": "Pokémon"}},
    ]):
        if 'attacks' in card:
            for a in card['attacks']:
                if 'text' in a:
                    if len(a['text']) > 0:
                        attack_text.append(a['text'])
                        writer.writerow((a['text'],))

# We put every word into list
words = []
# We will also put every first word of the text in a list to look for interesting patterns there
first_words = []
# And we will also put the first word with it's part of speech (POS) tag in a list
first_words_pos = []

# debug:
# attack_text = attack_text[0:999]

# This can take a while with the Senna Tagger (~45 minutes), let's display a progress bar
with click.progressbar(attack_text) as bar:
    for text in bar:
        # Convert common contractions to two words with same meaning
        # This is so that we don't have the word tokenized as two parts.
        # For example, we avoid this: do, n't
        text = text.replace("can't", "can not")
        text = text.replace("don't", "do not")
        text = text.replace("Don't", 'Do not')
        text = text.replace("aren't", "are not")

        # Tokenize each attack text
        attack_words = word_tokenize(text)

        # lower case everything
        attack_words = [word.lower() for word in attack_words]

        # remove single characters, mostly punctuation
        attack_words = [word for word in attack_words if word not in ['(', ')', '.', ',', ]]

        # note that we could have also removed English stop words and numbers here if needed

        # POS tagging -- opting to use Senna Tagger over the built-in POS tagger for higher accuracy
        # The built-in POS tagger was classifying 'flip' as a proper noun instead of a verb.
        # The Senna Tagger does better at identifying the verbs in the attack text, which is important, because
        # most of the text is command-form sentences telling you to do something. :-)
        # see:
        #  https://stackoverflow.com/questions/30821188/python-nltk-pos-tag-not-returning-the-correct-part-of-speech-tag
        # NLTK built in POS tagger:
        # tagged = pos_tag(attack_words)
        # Senna POS tagger:
        tagged = st.tag(attack_words)

        # Add tokens to words lists
        words.extend(attack_words)
        first_words.extend((attack_words[0],))
        first_words_pos.extend((tagged[0],))

# instantiate Text object so we can use nltk package
attack_text_list = Text(words)

# get the contexts of a given word
print("concordance of: flip")
attack_text_list.concordance('flip')
"""
Displaying 25 of 3558 matches:
                                     flip a coin if heads this attack does 10 
ur other pokémon in any way you like flip a coin if heads your opponent 's act
at during your opponent 's next turn flip a coin if heads your opponent 's act
d to your opponent 's active pokémon flip 3 coins this attack does 30 damage t
nent this attack does 80 more damage flip a coin if heads this attack does 20 
ter applying weakness and resistance flip a coin if tails this pokémon does 30
d an energy attached to this pokémon flip 2 coins this attack does 20 more dam
with 1 of his or her benched pokémon flip 2 coins if either of them is tails t
s and resistance for benched pokémon flip a coin for each water energy attache
ter on each of your benched magikarp flip a coin if heads this attack does 30 
his pokémon does 10 damage to itself flip a coin if heads your opponent 's act
his pokémon does 30 damage to itself flip 3 coins for each heads choose a rand
ard on it into your opponent 's hand flip a coin if heads discard an energy at
d to your opponent 's active pokémon flip a coin if tails this attack does not
nergy card attach it to this pokémon flip 2 coins this attack does 90 damage t
rom your discard pile into your hand flip 2 coins this attack does 20 more dam
ter applying weakness and resistance flip a coin until you get tails this atta
her hand during his or her next turn flip a coin if heads your opponent 's act
o it this attack does 20 more damage flip a coin if heads your opponent 's act
t 's active pokémon is now paralyzed flip a coin if heads this attack does 30 
eads this attack does 30 more damage flip a coin if tails this attack does not
our deck shuffle your deck afterward flip 3 coins this attack does 30 damage t
amage then discard that stadium card flip a coin if heads your opponent 's act
s the number of your benched pokémon flip a coin if heads the defending pokémo
os if any and attach it to 1 of them flip a coin if heads the defending pokémo
"""

# find words with similar contexts
# in other words, for a given a word w, finds all contexts w1 w w2,
# then finds all words w' that appear in the same context, i.e. w1 w' w2.
print("\nFind words with similar context as: flip")
attack_text_list.similar('flip')
"""
discard draw put attach choose remove move is has and shuffle flips if
to as have of show return for
"""

# find common contexts of two words
print("\nFind common contexts of: pokémon, hand")
attack_text_list.common_contexts(['pokémon', 'hand'])
"""
your_flip opponent_this your_on your_the opponent_if her_put
opponent_put your_heal your_at your_choose her_during opponent_search
her_does your_shuffle her_you opponent_does your_search her_and
your_move your_for
"""

# find collocations of two words
print("\nFind collocation of two words:")
attack_text_list.collocations()
"""
defending pokémon; next turn; benched pokémon; apply weakness; energy
attached; damage plus; damage times; active pokémon; deck afterward;
damage counters; energy card; n't affected; discard pile; applying
weakness; energy cards; damage done; damage counter; fire energy;
cards attached; card attached
"""

# create a Frequency Distribution, FreqDist, which is like Python Counter
attack_fd = FreqDist(attack_text_list)

# most frequent words in attack text
print("\nMost frequent words in attack text")
for word, frequency in attack_fd.most_common(30):
    print('{0}: {1}'.format(word, frequency))
"""
pokémon: 9622
damage: 7829
your: 7153
this: 5930
the: 5086
attack: 5046
to: 4934
does: 4887
if: 4855
of: 4376
a: 4216
opponent: 3863
's: 3851
flip: 3558
heads: 3252
is: 3229
defending: 3229
coin: 2867
and: 2759
energy: 2465
for: 2441
more: 2210
now: 2052
benched: 2042
1: 2010
10: 1906
not: 1686
attached: 1685
20: 1674
you: 1673
"""

# looking at only first words, what is frequency distribution?
first_text = Text(first_words)
first_fd = FreqDist(first_text)
print("\nMost frequent first words in attack text")
for word, frequency in first_fd.most_common(30):
    print('{0}: {1}'.format(word, frequency))
"""
flip: 3343
if: 988
this: 870
does: 707
discard: 668
the: 616
search: 446
choose: 405
your: 369
during: 338
you: 284
heal: 197
put: 162
remove: 152
draw: 142
switch: 135
attach: 100
move: 100
look: 81
before: 61
shuffle: 53
each: 33
both: 27
return: 23
count: 23
do: 21
after: 19
prevent: 18
20x: 17
for: 17
"""

# looking at only first words, what is the frequency distribution with POS?
first_tagged = Text(first_words_pos)
tag_fd = FreqDist((word,tag) for (word, tag) in first_tagged)
print("\nMost frequent first word POS in attack text")
for tag, frequency in tag_fd.most_common(30):
    print("{0}: {1}".format(tag, frequency))
"""
('flip', 'VB'): 3343
('if', 'IN'): 988
('this', 'DT'): 870
('does', 'VBZ'): 707
('discard', 'VB'): 668
('the', 'DT'): 616
('search', 'VB'): 444
('choose', 'VB'): 405
('your', 'PRP$'): 369
('during', 'IN'): 338
('you', 'PRP'): 284
('heal', 'VB'): 197
('remove', 'VB'): 152
('draw', 'VB'): 142
('switch', 'VB'): 135
('put', 'VBD'): 133
('move', 'VB'): 100
('attach', 'VB'): 100
('look', 'VB'): 81
('before', 'IN'): 61
('shuffle', 'VB'): 50
('each', 'DT'): 33
('both', 'DT'): 27
('count', 'VB'): 23
('do', 'VBP'): 21
('put', 'VBN'): 20
('after', 'IN'): 19
('return', 'VB'): 18
('prevent', 'VB'): 18
('20x', 'RB'): 17
"""
