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

def KeyCorrolation(d, key1, key2):
    """
    Given a dictionary, and two keys, returns a corrolation constant.
    Assumes: keys are valid and lead to equal-length numeric lists
    """
    
    l1 = list(d[key1])
    l2 = list(d[key2])
    remove_none([l1,l2])
    
    #if there is nothing left, return a corrolation of zero
    if len(l1)<=1 or len(l2)<=1:
        return 0
    
    corr = thinkstats2.SpearmanCorr(l1,l2)
    if math.isnan(corr):
        corr = 0

    return corr*len(l1)

def AllSpearmanCorr(d, filt = lambda(x): True, comp = KeyCorrolation):
    """
    Calculates the absolute value of the Spearman corrolation for all pairs of
    numeric columns in the data dictionary whose keys satisfy the filter function
    """
    
    numeric_keys = [key for key in d["__numeric__"] if filt(key)]
    key_pairs = ChooseTwo(numeric_keys)
    return [(abs(comp(d,*pair)),) + pair for pair in key_pairs]

def KeyInterestingness(d, key1, key2):
    """
    Given a dictionary, and two keys, returns an interestingness value.
    Assumes: keys are valid and lead to equal-length numeric lists
    """
    l1 = list(d[key1])
    l2 = list(d[key2])
    remove_none([l1,l2])
    
    #if there is nothing left, return a interestingness of zero
    if len(l1)<=1 or len(l2)<=1:
        return 0
    
    # we don't care which is the independant or depandant variable
    # except for some reason, using l1 seems to work better
    return min(Interest(l1,l2), Interest(l2,l1))

def Interest(l1, l2):
    """
    Tries to say how interesting the relation between these two lists
    of numbers is
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
    l2median = numpy.mean(l2)
    interest_value = 0
    for pbin in point_bins:
        if len(pbin)>0:
            diff = numpy.mean(pbin) - l2median
            interest_value += math.sqrt(diff**2*math.log(len(pbin)))/math.sqrt(l2var)
    
    return interest_value

def Scatter(d, var1, var2, **kwargs):

    xs = list(d[var1])
    ys = list(d[var2])
    remove_none([xs,ys])
    
    print 'Spearman corr', thinkstats2.SpearmanCorr(xs, ys), 'for ' + var1 + ' vs ' + var2
    
    print 'interest', KeyInterestingness(d, var1, var2), 'for ' + var1 + ' vs ' + var2
    
    thinkplot.Scatter(xs, ys, **kwargs)
    thinkplot.show()

if __name__ == '__main__':
    #beths = dataToDict('beths.csv')
    taxo = dataToDict('taxo.csv')

    # test on a small sample
    import re
    _digits = re.compile('\d')
    def no_digits(d):
        return not(bool(_digits.search(d)))

    # I chose to arbitrarily filter out data with digits, because they semmed less useful.

    all_corrs = AllSpearmanCorr(taxo, filt = no_digits, comp = KeyInterestingness)
    all_corrs.sort(reverse=True)
    print all_corrs[:9]
    for c in all_corrs[:9]:
        Scatter(taxo, c[1], c[2], label = c[1] + " vs " + c[2])
        
    #Scatter(taxo, 'sxdeny','SxPrFAC', label="sxdeny vs SxPrFAC")
    #Scatter(taxo, 'JuvaslFc', 'impschgr', label="sxdeny vs SxPrFAC")
    #Scatter(taxo, 'ComsxFac', 'anxwom', label="ComsxFac vs anxwom")
    #Scatter(taxo, 'Voyeur', 'PCD', label="Voyer vs PCD")
    #Scatter(taxo, 'lkemp', 'JuvDrgFc', label="lkemp vs JuvDrgFc")
    #Scatter(taxo, 'JuvaslFc', 'JuvDrgFc', label="JuvaslFc vs JuvDrgFc")
    #Scatter(taxo, 'asltcomc', 'Pnchldjv', label="asltcomc vs Pnchldjv")
    #AgeCdf(beths)
    #AgeCdf(taxo)
