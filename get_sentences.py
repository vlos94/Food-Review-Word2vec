##Script to produce a file of sentences to use for producing word
##embeddings. Our basic preprocessing will be to strip stopwords and
##punctuation, as well as convert all letters to lowercase.

import re
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

data = pd.read_csv('/Users/vlos/MLProjects/ReviewData/data/Reviews.csv')
data.drop(range(200000, data.shape[0]), axis=0, inplace=True)
data = data[data.Summary.notnull() == True]


stop_words = set(stopwords.words('english'))

def combine_strings(s1, s2):
    if s1[-1] in '?.!':
        return ' '.join([s1, s2])
    else:
        return '. '.join([s1, s2])

def row_combine(r):
    return combine_strings(r['Summary'], r['Text'])


Reviews = data.apply(row_combine, axis=1)

tokenizer = RegexpTokenizer('[\w\']+[!\?\.]?')

def clean_string(s):
    tokens = tokenizer.tokenize(s)
    g = (w.lower().strip() for w in tokens if w not in stop_words)
    return ' '.join(g)

Reviews = Reviews.apply(clean_string)

##Reviews.to_csv('cleaned_reviews.csv')

##Reviews.drop(range(50000, 75000), axis=0, inplace=True)

f = open('sentences.txt', 'w')

for s in Reviews:
    sentences = re.split('([\.\?!])', s)
    for t in sentences:
        if t in '?.!':
            f.write('\n')
        else:
            f.write(t.strip())
   
    

f.close()



s1 = 'This is a no punctuation summary'
s2 = 'This is a summary with punctuation!'

r = 'Here is a review.'

assert combine_strings(s1, r) ==  'This is a no punctuation summary. Here is a review.', 'No punctuation combining failed'
assert combine_strings(s2, r) == 'This is a summary with punctuation! Here is a review.', 'Combining with punctuation failed'


