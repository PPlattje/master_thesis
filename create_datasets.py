#script that takes the original datasets and combines them in different datasets:
import csv
import random
import re

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
    new = re.sub(r'#([^ ]*)', r'\1', new)
    new = re.sub(r'http[^ ]*', 'URL', new)
    new = re.sub(r'&#*[0-9]*;', ' EMOJI ', new)
    return new

 
with open('data/datasets/abusivetrain.tsv', 'w') as abusetrain:
    with open('data/datasets/hatetrain.tsv', 'w') as hatetrain:
        with open('data/datasets/abusivetest.tsv', 'w') as abusetest:
            with open('data/datasets/hatetest.tsv', 'w') as hatetest:
                with open('data/datasets/generaltest.tsv', 'w') as generaltest:
                    with open('data/datasets/abusivedev.tsv', 'w') as abusedev:
                        with open('data/datasets/hatedev.tsv', 'w') as hatedev:
                            print('created / emptied datset files')


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
    
with open('data/waseem_hoovy/combined.csv') as csvfile:
    hateclass = []
    abuseclass = []
    noneclass = []
    reader = csv.reader(csvfile, delimiter='\t')
    for line in reader:
        line[0] = preprocess(line[0].replace('\n', ' '))
        if line[1] == 'sexism':
            hateclass.append(line[0])
            abuseclass.append(line[0])
        elif line[1] == 'racism':
            hateclass.append(line[0])
            abuseclass.append(line[0])
        else:
            noneclass.append(line[0])
    print('Waseem & Hoovy | hate: {0} | abuse: {1} | none: {2}' \
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
            trainnone.append(line[0])    


print('trainhate: {0} | devhate: {1} | testhate: {2}' \
.format(len(trainhate), len(devhate), len(testhate)))
print('trainabuse: {0} | devabuse: {1} | testabuse: {2}' \
.format(len(trainabuse), len(devabuse), len(testabuse)))
print('trainnone: {0} | devnone: {1} | testnone: {2}' \
.format(len(trainnone), len(devnone), len(testnone)))
print('trainoffensive: {0} | devoffensive: {1} | testoffensive: {2}' \
.format(len(trainoffensive), len(devoffensive), len(testoffensive)))
with open('data/datasets/abusivetest.tsv', 'a') as abusetest:
    abusewriter = csv.writer(abusetest, delimiter='\t')
    abusetestset = []
    for item in testhate:
        abusetestset.append((item, '1'))
    for item in testabuse:
        abusetestset.append((item, '1'))
    for item in testnone:
        abusetestset.append((item, '0'))
    for item in testoffensive:
        abusetestset.append((item, '1'))
    random.shuffle(abusetestset)
    for item in abusetestset:
        abusewriter.writerow([item[0], item[1]])

with open('data/datasets/abusivedev.tsv', 'a') as abusetest:
    abusewriter = csv.writer(abusetest, delimiter='\t')
    abusedevset = []
    for item in testhate:
        abusedevset.append((item, '1'))
    for item in testabuse:
        abusedevset.append((item, '1'))
    for item in testnone:
        abusedevset.append((item, '0'))
    for item in devoffensive:
        abusedevset.append((item, '1'))
    random.shuffle(abusedevset)
    for item in abusedevset:
        abusewriter.writerow([item[0], item[1]])
        
with open('data/datasets/abusivetrain.tsv', 'a') as abusetrain:
    abusewriter = csv.writer(abusetrain, delimiter='\t')
    abusetrainset = []
    for item in trainhate:
        abusetrainset.append((item, '1'))
    for item in trainabuse:
        abusetrainset.append((item, '1'))
    for item in trainnone:
        abusetrainset.append((item, '0'))
    for item in trainoffensive:
        abusetestset.append((item, '1'))
    random.shuffle(abusetrainset)
    for item in abusetrainset:
        abusewriter.writerow([item[0], item[1]])       
        
with open('data/datasets/hatetrain.tsv', 'a') as hatetrain:
    abusewriter = csv.writer(hatetrain, delimiter='\t')
    hatetrainset = []
    for item in trainhate:
        hatetrainset.append((item, '1'))
    for item in trainabuse:
        hatetrainset.append((item, '0'))
    for item in trainoffensive:
        hatetrainset.append((item, '0'))
    random.shuffle(hatetrainset)
    for item in hatetrainset:
        abusewriter.writerow([item[0], item[1]])       


with open('data/datasets/hatetest.tsv', 'a') as hatetest:
    abusewriter = csv.writer(hatetest, delimiter='\t')
    hatetestset = []
    for item in testhate:
        hatetestset.append((item, '1'))
    for item in testabuse:
        hatetestset.append((item, '0'))
    for item in testoffensive:
        hatetestset.append((item, '0'))
    random.shuffle(hatetestset)
    for item in hatetestset:
        abusewriter.writerow([item[0], item[1]])       


with open('data/datasets/hatedev.tsv', 'a') as hatedev:
    abusewriter = csv.writer(hatedev, delimiter='\t')
    hatedevset = []
    for item in devhate:
        hatedevset.append((item, '1'))
    for item in devabuse:
        hatedevset.append((item, '0'))
    for item in devoffensive:
        hatedevset.append((item, '0'))
    random.shuffle(hatedevset)
    for item in hatedevset:
        abusewriter.writerow([item[0], item[1]])     


with open('data/datasets/generaltest.tsv', 'a') as generaltest:
    abusewriter = csv.writer(generaltest, delimiter='\t')
    generaltestset = []
    for item in testhate:
        generaltestset.append((item, '2'))
    for item in testabuse:
        generaltestset.append((item, '1'))
    for item in testoffensive:
        generaltestset.append((item, '1'))
    for item in testnone:
        generaltestset.append((item, '0'))
    random.shuffle(generaltestset)
    for item in generaltestset:
        abusewriter.writerow([item[0], item[1]])  
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                