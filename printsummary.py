import pandas as pd
import numpy as np
import csv

samplelist="sample.list"
#workdir="/home/jeffrey/projects/test/171023_compare35geneswhitepaper/"

def dfbatch(x):
    with open(samplelist) as f:
        for line in f:
           try:
            line = line.strip()
            sample1,sample2 = line.split('\t')
            
            df1 = pd.read_csv(run_dir+'output'+x+'/'+sample1+'.1.cpra',sep='\t',header=None)
            df2 = pd.read_csv(run_dir+'output'+x+'/'+sample2+'.2.cpra',sep='\t',header=None)
            dfs = [df1,df2]
            results = pd.concat(dfs)
            nf1 = df1[0].count()
            nf2 = df2[0].count()
            ndup = results[results[0].duplicated()].count()[0]
            nf1only = nf1-ndup
            nf2only = nf2-ndup
            #precision: TP/(TP+FP)
            #Recall: TP/(TP+FN)
            precision = float(ndup) / (float(ndup) + float(nf1only))
            recall = float(ndup) / (float(ndup) + float(nf2only))
            name = df1[1][0]
            dfsingle = pd.DataFrame({'f1':nf1,
                                    'f2':nf2,
                                    'dup':ndup,
                                    'f1only':nf1only,
                                    'f2only':nf2only,
                                    'precision':precision,
                                    'recall':recall},
                                index=[sample1])
            
            print(dfsingle)
            dfsingle.to_csv('batchsummary'+x+'.txt',sep="\t",mode='a',header=False)
           except:
            pass 
            
#dfbatch()
#need to add colnames:  dup    f1  f1only    f2  f2only  precision    recall

def dfheader(x):
    with open('batchsummary'+x+'.txt',mode='a') as csvfile:
     writer = csv.writer(csvfile, delimiter = "\t")
     writer.writerow(('Sample','TP','Variants called','FP','Variants called(ref)','FN','Precision:TP/(TP+FP)','Recall:TP(TP+FN)'))

def summary(y):
    dfheader(y)
    dfbatch(y)


summary('indel')
summary('snp')
