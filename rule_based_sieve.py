# script for the dictionary sieve
import csv
from nltk.tokenize import word_tokenize
import re
from nltk.stem import PorterStemmer
import wordlists

def calc_prec(file, wordlist):
    reader = csv.reader(csvfile, delimiter='\t')
    predictions = []
    tp = 0
    fp = 0
    fn = 0
    tn = 0
    pos = 0
    neg = 0
    with open('data/datasets/sieve/Abusive_test_sieve_1_0.tsv', 'w') as f1:
        with open('data/datasets/sieve/Abusive_test_sieve_1_1.tsv', 'w') as f0:
            writer1 = csv.writer(f1, delimiter='\t')
            writer0 = csv.writer(f0, delimiter='\t')
            for instance in reader:
                badwords = 0
                ps = PorterStemmer()
                tokenized = word_tokenize(instance[0].lower())
                for word in wordlist:
                    if word in tokenized:
                        badwords += 1
                    elif ps.stem(word) in tokenized:
                        badwords += 1
                if badwords > 3:
                    if instance[1] == '1':
                        writer1.writerow([instance[0], instance[1]])
                        tp += 1
                    else:
                        writer0.writerow([instance[0], instance[1]])
                        fp += 1
                else:
                    writer0.writerow([instance[0], instance[1]])
                    if instance[1] == '1':
                        fn += 1
                    else:
                        tn += 1
    return(tp, fp, fn, tn)


with open('dictionaries/wiegand_e_075', 'r') as f:
    regex = re.compile(r".+?(?=_)")
    lines = f.readlines()
    wordlist = []
    for line in lines:
        word = re.match(regex, line)[0]
        if word not in wordlist:
            wordlist.append(word)

print('results from dictionary model')
with open("data/datasets//abusivetest.tsv", 'r') as csvfile:
    tp, fp, fn, tn, = calc_prec(csvfile, wordlist)
    print('tp: {0} | fp: {1} | fn: {2} | tn: {3}'.format(tp,fp,fn,tn))
    