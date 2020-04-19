#variant of create_datasets.py that creates the Extra Hate dataset
import csv
import random
import re
import emoji
import html

def distribute_data(hateclass, abuseclass, noneclass):
    trainhate = []
    devhate = []
    testhate = []
    trainabuse = []
    devabuse = []
    testabuse = []
    trainnone = []
    devnone = []
    testnone = []
    trainoffensive = []
    random.shuffle(hateclass)
    random.shuffle(abuseclass)
    random.shuffle(noneclass)
    ratio = int(0.1 * len(hateclass))
    for x in range(ratio):
        devhate.append(hateclass.pop())
    for x in range(ratio):
        testhate.append(hateclass.pop())
    for item in hateclass:
        trainhate.append(item)
    ratio = int(0.1 * len(abuseclass))
    for x in range(ratio):
        devabuse.append(abuseclass.pop())
    for x in range(ratio):
        testabuse.append(abuseclass.pop())
    for item in abuseclass:
        trainabuse.append(item)
    ratio = int(0.1 * len(noneclass))
    for x in range(ratio):
        devnone.append(noneclass.pop())
    for x in range(ratio):
        testnone.append(noneclass.pop())
    for item in noneclass:
        trainnone.append(item)
    return trainhate, devhate, testhate, \
           trainabuse, devabuse, testabuse, \
           trainnone, devnone, testnone
 
def preprocess(tweet):
    new = re.sub(r'@[^ ]*', '@USER', tweet)
    new = re.sub(r'http[^ ]*', 'URL', new)
    #new = re.sub(r'&#*[0-9]*;', ' EMOJI ', new)
    new = re.sub(r'(&)([0-9]+;)', r'\1#\2', new)
    new = emoji.demojize(html.unescape(new), use_aliases=True)
    new = re.sub(r'#([^ ]*)', r'# \1', new)
    return new

 
with open('data/datasets/extra_hate/abusivetrain.tsv', 'w') as abusetrain:
    with open('data/datasets/extra_hate/hatetrain.tsv', 'w') as hatetrain:
        with open('data/datasets/extra_hate/abusivetest.tsv', 'w') as abusetest:
            with open('data/datasets/extra_hate/hatetest.tsv', 'w') as hatetest:
                with open('data/datasets/extra_hate/generaltest.tsv', 'w') as generaltest:
                    with open('data/datasets/extra_hate/abusivedev.tsv', 'w') as abusedev:
                        with open('data/datasets/extra_hate/hatedev.tsv', 'w') as hatedev:
                            print('created / emptied dataset files')


hateclass = []
abuseclass = []
noneclass = []
trainhate = []
devhate = []
testhate = []
trainabuse = []
devabuse = []
testabuse = []
trainnone = []
devnone = []
testnone = []
trainoffensive = []
devoffensive = []
testoffensive = []
trainhatenone = []
devhatenone = []
testhatenone = []



with open('data/founta/sorted.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    hateclass = []
    abuseclass = []
    noneclass = []
    hatevote = 0
    abusivevote = 0
    normalvote = 0
    previousline = ''
    for line in reader:
        line[0] = preprocess(line[0].replace('\n', ' '))
        if line[0] != previousline:
            if hatevote > abusivevote and hatevote > normalvote:
                hateclass.append(previousline)
            elif abusivevote > hatevote and abusivevote > normalvote:
                abuseclass.append(previousline)
            else:
                noneclass.append(previousline)
            hatevote = 0
            abusivevote = 0
            normalvote = 0
        if line[1] == 'hateful':
            hatevote += int(line[2])
        elif line[1] == 'abusive':
            abusivevote += int(line[2])
        else:
            normalvote += int(line[2])
        previousline = line[0]

    print('founta et al | hate: {0} | abuse: {1} | none: {2}' \
    .format(len(hateclass), len(abuseclass), len(noneclass)))
    dataset_trainhate, dataset_devhate,dataset_testhate, \
    dataset_trainabuse, dataset_devabuse, dataset_testabuse, \
    dataset_trainnone, dataset_devnone, dataset_testnone \
    = distribute_data(hateclass, abuseclass, noneclass)
    trainhate = trainhate + dataset_trainhate
    devhate = devhate + dataset_devhate
    testhate = testhate + dataset_testhate
    trainabuse = trainabuse + dataset_trainabuse
    devabuse = devabuse + dataset_devabuse
    testabuse = testabuse + dataset_testabuse
    trainnone = trainnone + dataset_trainnone
    devnone = devnone + dataset_devnone
    testnone = testnone + dataset_testnone
    print(len(devnone), len(testnone))
    


with open('data/OLID/olidtransformed.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    noneclass = []
    offensiveclass = []
    for line in reader:
        line[0] = preprocess(line[0].replace('\n', ' '))
        if line[1] == '1':
            offensiveclass.append(line[0])
        else:
            noneclass.append(line[0])
    random.shuffle(offensiveclass) 
    ratio = int(0.2 * len(offensiveclass))
    for x in range(ratio):
        devoffensive.append(offensiveclass.pop())
    for item in offensiveclass:
        trainoffensive.append(item)
    random.shuffle(offensiveclass) 
    ratio = int(0.2 * len(noneclass))
    for x in range(ratio):
        devnone.append(noneclass.pop())
    for item in noneclass:
        trainnone.append(item)


with open('data/OLID/olidtest.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    for line in reader:
        line[0] = preprocess(line[0].replace('\n', ' '))
        if line[1] == '1':
            testoffensive.append(line[0])
        else:
            testnone.append(line[0])    


with open('data/hateval/hateval_train_transformed.tsv') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    for line in reader:
        line[0] = preprocess(line[0].replace('\n', ' '))
        if line[1] == '1':
            trainhate.append(line[0])
        elif line[1] == '0':
            trainhatenone.append(line[0])
            


with open('data/hateval/hateval_dev_transformed.tsv') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    for line in reader:
        line[0] = preprocess(line[0].replace('\n', ' '))
        if line[1] == '1':
            devhate.append(line[0])
        elif line[1] == '0':
            devhatenone.append(line[0])

with open('data/hateval/reference_test_en/hateval_test_transformed.tsv') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    for line in reader:
        line[0] = preprocess(line[0].replace('\n', ' '))
        if line[1] == '1':
            testhate.append(line[0])
        elif line[1] == '0':
            testhatenone.append(line[0])
            
with open('data/waseem_hoovy/combined.csv') as csvfile:
    hateclass = []
    abuseclass = []
    noneclass = []
    reader = csv.reader(csvfile, delimiter='\t')
    for line in reader:
        line[0] = preprocess(line[0].replace('\n', ' '))
        if line[1] == 'sexism':
            hateclass.append(line[0])
        elif line[1] == 'racism':
            hateclass.append(line[0])
    print('Waseem & Hoovy | hate: {0} | abuse: {1} | none: {2}' \
    .format(len(hateclass), len(abuseclass), len(noneclass)))
    dataset_trainhate, dataset_devhate,dataset_testhate, \
    dataset_trainabuse, dataset_devabuse, dataset_testabuse, \
    dataset_trainnone, dataset_devnone, dataset_testnone \
    = distribute_data(hateclass, abuseclass, noneclass)
    trainhate = trainhate + dataset_trainhate
    devhate = devhate + dataset_devhate
    testhate = testhate + dataset_testhate
    trainhatenone = trainhatenone + dataset_trainnone
    devhatenone = devhatenone + dataset_devnone
    testhatenone = testhatenone + dataset_testnone
    

print('trainhate: {0} | devhate: {1} | testhate: {2}' \
.format(len(trainhate), len(devhate), len(testhate)))
print('trainabuse: {0} | devabuse: {1} | testabuse: {2}' \
.format(len(trainabuse), len(devabuse), len(testabuse)))
print('trainnone: {0} | devnone: {1} | testnone: {2}' \
.format(len(trainnone), len(devnone), len(testnone)))
print('trainoffensive: {0} | devoffensive: {1} | testoffensive: {2}' \
.format(len(trainoffensive), len(devoffensive), len(testoffensive)))
       
        
with open('data/datasets/extra_hate/hatetrain.tsv', 'a') as hatetrain:
    abusewriter = csv.writer(hatetrain, delimiter='\t')
    hatetrainset = []
    for item in trainhate:
        hatetrainset.append((item, '1'))
    for item in trainabuse:
        hatetrainset.append((item, '0'))
    for item in trainoffensive:
        hatetrainset.append((item, '0'))
    for item in trainhatenone:
        hatetrainset.append((item, '0'))
    random.shuffle(hatetrainset)
    for item in hatetrainset:
        abusewriter.writerow([item[0], item[1]])
       


with open('data/datasets/extra_hate/hatetest.tsv', 'a') as hatetest:
    abusewriter = csv.writer(hatetest, delimiter='\t')
    hatetestset = []
    for item in testhate:
        hatetestset.append((item, '1'))
    for item in testabuse:
        hatetestset.append((item, '0'))
    for item in testoffensive:
        hatetestset.append((item, '0'))
    for item in testhatenone:
        hatetestset.append((item, '0'))
    random.shuffle(hatetestset)
    for item in hatetestset:
        abusewriter.writerow([item[0], item[1]])       


with open('data/datasets/extra_hate/hatedev.tsv', 'a') as hatedev:
    abusewriter = csv.writer(hatedev, delimiter='\t')
    hatedevset = []
    for item in devhate:
        hatedevset.append((item, '1'))
    for item in devabuse:
        hatedevset.append((item, '0'))
    for item in devoffensive:
        hatedevset.append((item, '0'))
    for item in devhatenone:
        hatedevset.append((item, '0'))
    random.shuffle(hatedevset)
    for item in hatedevset:
        abusewriter.writerow([item[0], item[1]])   