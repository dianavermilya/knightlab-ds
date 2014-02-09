import numpy
import urllib

import thinkplot
import thinkstats2

def dataToDict(f):
    d = {}
    f = open(f, 'r')
    keyString = f.readline()[:-2]
    keys = keyString.split(",")
    for key in keys:
        d[key] = []
    for line in f:
        ans=line.split(",")
        for i in range(len(keys)):
            d[keys[i]].append(ans[i])
    return d

def meanAge(d):
    ages = d['age']
    s = 0
    for age in ages:
        s += int(age)
    return float(s)/len(ages)

def AgePmf(d):
    print d['age'], type(d['age'])
    pmf = thinkstats2.MakePmfFromList(d['age'], 'age')
    print "got here"

    thinkplot.Hist(pmf)
    thinkplot.Show(title='PMF of Age',
               xlabel='age(years',
               ylabel='probability')





beths = dataToDict('beths.csv')
taxo = dataToDict('taxo.csv')
AgePmf(beths)
