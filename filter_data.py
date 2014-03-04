import numpy
import urllib
import math
import thinkplot
import thinkstats2
import codecs
import datetime

def reviseDataType (string):
    """
    Atttempts to turn the string into the appropriate data type
    """

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
    #wr = open("strings" + filename, "w")
    count = 0
    
    # strip line ending characters
    keyString = f.readline().rstrip()
    
    # check for and strip utf-8 BOM (python bug wont auto-remove it :( )
    if keyString[0:3] == codecs.BOM_UTF8:
        keyString = keyString[3:]
      
    keys = keyString.split(",")
    
    #start out by assuming everything is numeric
    d[numeric_key] = {key:True for key in keys}
    for line in f:
        ans=line.split(",")
        for i in range(len(keys)):
            val = reviseDataType(ans[i])
            if not(isinstance(val,(int, long, float, complex, type(None)))):
                # mark data in this column as containing non-numeric
                if keys[i] in d[numeric_key]:
                    d[numeric_key].pop(keys[i])
                    count += 1
             
            #if isinstance(val, str):
            #    count += 1
            #    wr.write(val + "\n--\n")
            d.setdefault(keys[i], []).append(val)
    print "numeric columns: ", len(keys) - count
    
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

def remove_none(listOfLists):
    """Given an arbitrary number of lists, removes the ith entry from
       all of them if any of them is None at that point.
       
       Assumes: all lists are the same dimension"""
    
    # we start out with all elements
    length = len(listOfLists[0])
    
    # this is probably the ugliest code I have ever written :(
    index = 0
    while index < length:
        old_length = length
        for array in listOfLists:
            if array[index] is None:
                # pop each list
                for array in listOfLists:
                    array.pop(index)       
                length -= 1
                break

        # only increment index if we didn't remove any items
        if old_length == length:
            index += 1

if __name__ == '__main__':
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

