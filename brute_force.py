import math
import thinkplot
import thinkstats2
import numpy
from filter_data import dataToDict, remove_none

def ChooseTwo(l):
    """
    Given a list, retruns a list of all possible tuples of the elements
    (considering order as irrelevant)
    """
    
    return [(a, b) for a in l for b in l[l.index(a)+1:]]

def KeyCompare(d, key1, key2, comp = thinkstats2.Corr):
    """
    Given a dictionary, and two keys, returns a comparison constant.
    Assumes: keys are valid and lead to equal-length numeric lists
    """
    
    l1 = list(d[key1])
    l2 = list(d[key2])
    l = remove_none([l1,l2])
    
    #if there is nothing left, return a corrolation of zero
    if len(l[0])<=1 or len(l[1])<=1:
        return 0
    
    corr = comp(l[0], l[1])
    if math.isnan(corr):
        corr = 0

    return corr

def AllPairs(d, comp = thinkstats2.Corr):
    """
    Calculates the absolute value of the comparison function for all pairs of
    numeric columns in the data dictionary whose keys satisfy the filter function
    """
    
    numeric_keys = [key for key in d["__numeric__"] if key in d["__relevant__"]]
    key_pairs = ChooseTwo(numeric_keys)
    return [(abs(KeyCompare(d,*pair, comp = comp)),) + pair for pair in key_pairs]

def Interestingness(l1, l2):
    """
    Given a dictionary, and two keys, returns an interestingness value, based on assuming alternately that l2 depends on l1 and vice versa.
    """
    
    # we don't care which is the independant or depandant variable
    # except for some reason, using l1 seems to work better
    return max(Interest(l1,l2), Interest(l2,l1))

def Interest(l1, l2):
    """
    Tries to say how interesting l1 is as a predictor of l2.
    """
    
    points = zip(l1,l2)
    l1min = min(l1)
    l1max = max(l1)
    l2var = numpy.var(l2)
    
    # not interesting cases
    if l1min == l1max or l2var == 0:
        return 0

    # arbitrarily bin it into 10 bins
    num_bins = 20
    width = (max(l1) - min(l1))/float(num_bins)
    
    # now, we bin the l2 points based on the l1 values they
    # correspond to
    point_bins = [list() for i in range(num_bins)]
    for p in points:
        index = int((p[0] - l1min)/width)
        if index >= num_bins:
            index = num_bins - 1;
        
        point_bins[index].append(p[1])
    
    # we define the interestingness of a bin to be the squared difference
    # of the median in the bin to the median of all l2 values, times the
    # number of items in the bin   
    l2median = numpy.median(l2)
    interest_value = 0
    for pbin in point_bins:
        if len(pbin)>0:
            diff = numpy.median(pbin) - l2median
            interest_value += math.sqrt(diff**2*math.sqrt(len(pbin)))/math.sqrt(l2var)
    
    return interest_value

def Scatter(d, var1, var2, **kwargs):
    """scatter plots the various data, and prints info on it.
    """
    xs = list(d[var1])
    ys = list(d[var2])
    data = remove_none([xs,ys])
    
    print 'Spearman corr', thinkstats2.SpearmanCorr(data[0], data[1]), 'for ' + var1 + ' vs ' + var2
    
    print 'interest', Interestingness(data[0],data[1]), 'for ' + var1 + ' vs ' + var2
    
    thinkplot.Scatter(data[0], data[1], **kwargs)
    thinkplot.show()

if __name__ == '__main__':
    #beths = dataToDict('beths.csv')
    taxo = dataToDict('taxo.csv')

    all_corrs = AllPairs(taxo, comp = Interestingness)
    all_corrs.sort(reverse=True)
    print all_corrs[:19]
    for c in all_corrs[:19]:
        Scatter(taxo, c[1], c[2], label = c[1] + " vs " + c[2])
\
