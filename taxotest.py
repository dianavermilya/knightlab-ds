import numpy
import urllib

import thinkplot
import thinkstats2

import codecs

def dataToDict(f):
	d = {}
	f = open(f, 'r')
	
	# strip line ending characters
	keyString = f.readline().rstrip()
	
	# check for and strip utf-8 BOM (python bug wont auto-remove it :( )
	if keyString[0:3] == codecs.BOM_UTF8:
	    keyString = keyString[3:]
	  
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
    ages = [float(age) for age in d['age']]
    pmf = thinkstats2.MakePmfFromList(ages, 'age')
    thinkplot.Hist(pmf)
    thinkplot.Show(title='PMF of Age',
               xlabel='age(years)',
               ylabel='probability')


def AgeCdf(d):
    ages = [float(age) for age in d['age']]
    cdf = thinkstats2.MakeCdfFromList(ages, 'age')

    thinkplot.Cdf(cdf)
    thinkplot.Show(title='CDF of Age',
               xlabel='age(years)',
               ylabel='probability')


beths = dataToDict('beths.csv')
taxo = dataToDict('taxo.csv')
AgeCdf(beths)
AgeCdf(taxo)
