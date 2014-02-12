import numpy
import urllib

import thinkplot
import thinkstats2

import codecs
import datetime

def reviseDataType (string):
    try:
        return int(string)
    except:
        pass
    try:
        return float(string)
    except:
        pass
    if string.strip() == "":
        return None
    if len(string.split("/")) == 3:
        [day, month, year] = string.split("/")
        try:
            return datetime.date(int(year), int(month), int(day))
        except:
            pass

    return string



def dataToDict(filename):
    d = {}
    tagToDataType = {}
    f = open(filename, 'r')
    wr = open("strings" + filename, "w")
    count = 0
    
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
            val = reviseDataType(ans[i])
            if isinstance(val, str):
                count += 1
                wr.write(val + "\n--\n")
            d[keys[i]].append(val)
    print "count: ", count
    
    return d


def mean(d, key):
    vals = d[key]
    s = 0
    try:
        for val in vals:
            s += int(val)
        return float(s)/len(val)
    except:
        "One of your values is not a number."

def AgePmf(d):
    pmf = thinkstats2.MakePmfFromList(d['age'], 'age')
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

def Scatter(d, var1, var2):
    """Assuming numerical for now (will call isNumerical()"""
    xs = d[var1]
    ys = d[var2]
    thinkplot.Scatter(xs, ys)
    thinkplot.show()

beths = dataToDict('beths.csv')
taxo = dataToDict('taxo.csv')

Scatter(taxo, 'ComsxFac', 'anxwom')

#AgeCdf(beths)
#AgeCdf(taxo)
