#script to transform our datasets to to a format expected by BERT
import pandas as pd

data = pd.read_csv('data/lala.tsv', delimiter='\t', header=None)
bertraindata = pd.DataFrame({'id':range(len(data)), 'label':data[1], 'alpha':['a'] * data.shape[0], 'text':data[0]})
bertraindata.to_csv('data/abusive/data/testing_something.tsv', sep='\t', index=False, header=False)

