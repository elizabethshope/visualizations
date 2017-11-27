# Libraries
import re
from nltk import word_tokenize, FreqDist
from nltk.corpus import stopwords
import math

# Import blog content
with open('blogtext.txt') as f:
    squirrels = f.read()

# Tokenize the text
words = word_tokenize(squirrels)

# Make all words lowercase
words = [word.lower() for word in words]

# Remove punctuation, stop words and some other non-meaningful words
pattern = re.compile("[^\w\s]")
words = [word for word in words if not pattern.match(word)]
stop_words = set(stopwords.words('english'))
words = [word for word in words if word not in stop_words]
words = [word for word in words if word not in ['also', 'one', 'like', 'know', "don’t", 'get', 'around', 'even', 'may',
                                                'however', 'would', 'things', "that’s", "it’s", "isn’t", 'another',
                                                'i’m', 'aren’t', 'http']
         ]

# Create frequency distribution of the squirrel blog words
fdist = FreqDist(words)

# Print out for copying into word cloud generator
for term in fdist.most_common(100):
    print('%d\t%s' % (max([1, math.floor(math.sqrt(term[1]))-1]), term[0]))


