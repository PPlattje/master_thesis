#Script that calculates several metrics of a dataset for analysis
import csv
from nltk.tokenize import word_tokenize
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import math
import re
from scipy.spatial import distance

def count_words(text):
    prev_prev_word = ''
    prev_word = ''
    wordcount = 0
    for word in text:
        if word not in ['@', '#',]:
            wordcount += 1
        prev_prev_word = prev_word
        prev_word = word
    return wordcount
                
        


def badwords(tokenized, wordlist):
    data = []
    badwords = []
    score = 0
    wordcount = count_words(tokenized)
    for word in wordlist:
        if word[0] in tokenized:
            badwords.append(word[0])
            score += word[1]
    try:
        return (score / wordcount), len(badwords)
    except ZeroDivisionError:
        print(tokenized)
    
with open('dictionaries/wiegand_e_075', 'r') as f:
    reader = csv.reader(f, delimiter = '\t')
    regex = re.compile(r".+?(?=_)")
    wordlist = []
    words = []
    for line in reader:
        word = re.match(regex, line[0])[0]
        if word not in words:
            words.append(word)
            wordlist.append((word, float(line[1])))   

    
with open('data/datasets/extra_hate/extrahatetest.tsv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    pos_examples = []
    neg_examples = []
    pos_count = 0
    pos_pron_count = 0
    pos_at_count = 0
    neg_pron_count = 0
    neg_at_count = 0
    pos_length = 0
    neg_count = 0
    neg_length = 0
    pos_wordcount = 0
    neg_wordcount = 0
    pos_score = 0
    neg_score = 0
    pos_frequency = 0
    neg_frequency = 0
    pos_words = []
    neg_words = []
    pos_types = []
    neg_types = []
    pronouns = ['we', 'us', 'I', 'me', 'you', 'she','her','he','him', 'they', 'them']
    with open('pos_extrahatetrain.tsv', 'w') as pos_file:
        poswriter = csv.writer(pos_file, delimiter='\t')
        with open('neg_extrahatetrain.tsv', 'w') as neg_file:
            negwriter = csv.writer(neg_file, delimiter='\t')
            for item in reader:
                if item[1] == '1':
                    pos_examples.append(item)
                    poswriter.writerow([item[0]])
                if item[1] == '0':
                    negwriter.writerow([item[0]])
                    neg_examples.append(item)
    for item in pos_examples:
        pos_length += len(item[0])
        tokenized = word_tokenize(item[0].lower())
        item_score, item_frequency = badwords(tokenized, wordlist)
        pos_score += item_score
        pos_frequency += item_frequency
        for item in pronouns:
            if item in tokenized:
                pos_pron_count += 1
                break
        if '@' in tokenized:
            pos_at_count += 1
        for word in tokenized:
            pos_words.append(word)
            if word not in pos_types:
                pos_types.append(word)
        pos_count += 1

    for item in neg_examples:
        neg_length += len(item[0])
        tokenized = word_tokenize(item[0].lower())
        item_score, item_frequency = badwords(tokenized, wordlist)
        neg_score += item_score
        neg_frequency += item_frequency
        for item in pronouns:
            if item in tokenized:
                neg_pron_count += 1
                break
        if '@' in tokenized:
            neg_at_count += 1
        for word in tokenized:
            neg_words.append(word)
            if word not in neg_types:
                neg_types.append(word)
        neg_count += 1
        
        
token_overlap = 0
oov = 0
oovlist = []
for word in pos_types:
    if word in neg_types:
        token_overlap += 1
    if word not in neg_types:
        oov += 1
        oovlist.append(word)

with open('pos_extrahatetrain.tsv', 'r') as posdoc:
    with open('neg_extrahatetrain.tsv', 'r') as negdoc:
        vectorizer = TfidfVectorizer(stop_words='english', max_df =0.5, min_df = 1)
        pos_examples = posdoc.read()
        neg_examples = negdoc.read()
        vectors = vectorizer.fit_transform([pos_examples, neg_examples])
        feature_names = vectorizer.get_feature_names()
        dense = vectors.todense()
        denselist = dense.tolist()
        df = pd.DataFrame(denselist, columns=feature_names)
TFIDF_dict = df.to_dict()


with open('TFIDF.csv', 'w') as f:
    writer = csv.writer(f, delimiter='\t')
    for item in TFIDF_dict:
        writer.writerow([item, TFIDF_dict[item][0], TFIDF_dict[item][1]])
        
with open('PMI.csv', 'w') as f:
    writer = csv.writer(f, delimiter='\t')
    for item in list(dict.fromkeys(pos_words)):
        x = pos_words.count(item)
        y = x + neg_words.count(item)
        PMI = math.log((x/y))
        writer.writerow([item, PMI])

with open('oovlist.txt', 'w') as f:
    for item in oovlist:
        print(item, file=f)



print('positive examples: {0} | negative examples: {1}'.format(pos_count, neg_count))
print('average length positive class: ' + str(pos_length / pos_count))
print('average length negative class: ' + str(neg_length / neg_count))
print('average number of words positive class: ' + str(len(pos_words) / pos_count))
print('average number of words negative class: ' + str(len(neg_words) / neg_count))
print('# positive types: {0} | # negative types: {1} | overlap: {2}'.format(len(pos_types), len(neg_types), token_overlap))
print('oov-words: {0}'.format(oov))
print(pos_length)
print('average badword score positive class: {0}: average badword score negative classs: {1}'.format(pos_score / pos_count, neg_score / neg_count))
print('average # of bad words positive class: {0}: average # of bad words negative classs: {1}'.format(pos_frequency / pos_count, neg_frequency / neg_count))
print('positive class % use pronoun: {0} | negativve class % use pronoun: {1}'.format((pos_pron_count / pos_count) * 100, (neg_pron_count / neg_count) * 100))
print('positive class % use @: {0} | negativve class % use @: {1}'.format((pos_at_count / pos_count) * 100, (neg_at_count / neg_count) * 100))