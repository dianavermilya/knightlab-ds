import numpy
import urllib
import math
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
    """
        Turns a csv databse into a dictionarry.
        
        Assumes: "__numeric__" is not a column heading
    """
    numeric_key = "__numeric__"
    d = {numeric_key: {}}
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
            if (isinstance(val,(int, long, float, complex, type(None)))):
                # mark data in this column as numeric
                d[numeric_key][keys[i]] = True
             
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

def Scatter(d, var1, var2, **kwargs):
    """Assuming numerical for now (will call isNumerical()"""
    xs = list(d[var1])
    ys = list(d[var2])
    RemoveNone(xs,ys)
    
    print 'Spearman corr', thinkstats2.SpearmanCorr(xs, ys)
    
    thinkplot.Scatter(xs, ys, **kwargs)
    thinkplot.show()

def RemoveNone(*args):
    """Given an arbitrary number of lists, removes the ith entry from
       all of them if any of them is None at that point.
       
       Assumes: all lists are the same dimension"""
    
    # we start out with all elements
    length = len(args[0])
    
    # this is probably the ugliest code I have ever written :(
    index = 0
    while index < length:
        old_length = length
        for array in args:
            if array[index] is None:
                # pop each list
                for array in args:
                    array.pop(index)       
                length -= 1
                break
        # only increment index if we didn't remove any items
        if old_length == length:
            index += 1

def ChooseTwo(l):
    """
    Given a list, retruns a list of all possible tuples of the elements
    (considering order as irrelevant)
    """
    
    return [(a, b) for a in l for b in l[l.index(a)+1:]]


def AllSpearmanCorr(d):
    """
    Calculates the absolute value of the Spearman corrolation for all pairs of
    numeric columns in the data dictionary
    """
    
    numeric_keys = [key for key in d.keys() if key in d["__numeric__"]]
    
    key_pairs = ChooseTwo(numeric_keys)
    return [(abs(KeyCorrolation(d,*pair)),) + pair for pair in key_pairs]

def KeyCorrolation(d, key1, key2):
    """
    Given a dictionary, and two keys, returns a corrolation constant.
    Assumes: keys are valid and lead to equal-length numeric lists
    """
    
    l1 = list(d[key1])
    l2 = list(d[key2])
    RemoveNone(l1,l2)
    
    #if there is nothing left, return a corrolation of zero
    if len(l1)<=1 or len(l2)<=1:
        return 0

    return thinkstats2.SpearmanCorr(l1,l2)
  

#beths = dataToDict('beths.csv')
taxo = dataToDict('taxo.csv')

# test on a small sample
import re
_digits = re.compile('\d')
def contains_digits(d):
    return bool(_digits.search(d))

# I chose to arbitrarily filter out data with digits, because they semmed less useful.
small_taxo = {key:taxo[key] for key in taxo.keys()[:] if not(contains_digits(key))}
small_taxo.update({"__numeric__": taxo["__numeric__"]})
import pdb; pdb.set_trace()
all_corrs = AllSpearmanCorr(small_taxo)
all_corrs.sort(reverse=True)
print all_corrs[:20]

Scatter(taxo, 'sxdeny','SxPrFAC', label="sxdeny vs SxPrFAC")
Scatter(taxo, 'ExAggbeh', 'JuvDelBehSexual')
Scatter(taxo, 'ComsxFac', 'anxwom', label="ComsxFac vs anxwom")
Scatter(taxo, 'Voyeur', 'PCD', label="Voyer vs PCD")
Scatter(taxo, 'lkemp', 'JuvDrgFc', label="lkemp vs JuvDrgFc")
Scatter(taxo, 'JuvaslFc', 'JuvDrgFc', label="JuvaslFc vs JuvDrgFc")
Scatter(taxo, 'asltcomc', 'Pnchldjv', label="asltcomc vs Pnchldjv")
#AgeCdf(beths)
#AgeCdf(taxo)

#l1 = [1,2,3,4,None]
#l2 = [1,2,3,4,5]
#RemoveNone(l1,l2)
