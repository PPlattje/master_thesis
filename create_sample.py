#script used to create a random sample from data
import random
import pandas

dataset = 'hate'
with open ('data/preds/hate sieve.tsv', 'r') as csvfile:
    dat = pandas.read_csv(csvfile, sep='\t')
sample = dat.sample(int(len(dat)/10))
sample.to_csv('data/preds/hate_sieve_sample.tsv', sep='\t')