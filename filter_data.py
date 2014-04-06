import numpy
import urllib
import math
import thinkplot
import thinkstats2
import codecs
import datetime
import warnings

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


import re
_digits = re.compile('\d')
def no_digits(s):
    return not(bool(_digits.search(s)))

def no_digits_keys(d):
    l = []
    for key in d["__numeric__"]:
        if no_digits(key):l.append(key)
    return l




def dataToDict(filename):
    """
        Turns a csv databse into a dictionarry.
        
        Assumes: "__numeric__" is not a column heading
    """
    numeric_key = "__numeric__"
    relevant_key = "__relevant__"
    d = {numeric_key: [], relevant_key:[]}
    f = open(filename, 'r')
    #wr = open("strings" + filename, "w")
    count = 0
    
    # strip line ending characters
    keyString = f.readline().rstrip()
    
    # check for and strip utf-8 BOM (python bug wont auto-remove it :( )
    if keyString[0:3] == codecs.BOM_UTF8:
        keyString = keyString[3:]
      
    keys = keyString.split(",")
    
    # assign all keys that don't contain digits as interesting
    d[relevant_key] = [key for key in keys if no_digits(key)]
    
    #start out by assuming everything is numeric
    d[numeric_key] = list(keys)
    for line in f:
        ans=line.split(",")
        for i in range(len(keys)):
            val = reviseDataType(ans[i])
            if not(isinstance(val,(int, long, float, complex, type(None)))):
                # mark data in this column as containing non-numeric
                if keys[i] in d[numeric_key]:
                    d[numeric_key].remove(keys[i])
                    count += 1
            
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
       
       Does not modify original lists
       
       Assumes: all lists are the same dimension"""
    
    newLists = [list(data) for data in listOfLists]
    
    # we start iterating over the shortest list
    length = min([len(el) for el in newLists])
    
    # check that they are all the same length, of not raise warning
    for el in newLists:
        if len(el) != length:
            warnings.warn("Arrays not te same length!!")
    
    # this is probably the ugliest code I have ever written :(
    index = 0
    while index < length:
        old_length = length
        for array in newLists:
            if array[index] is None:
                # pop each list
                for array in newLists:
                    array.pop(index)       
                length -= 1
                break

        # only increment index if we didn't remove any items
        if old_length == length:
            index += 1
     
    return newLists

if __name__ == '__main__':
    l1 = [1,2,3,None]
    l2 = [1,2,3,4]
    l = remove_none([l1,l2])
    assert l[0] == [1,2,3]
    assert l[0] == l[1]
    
    l1 = [1,2,None,None,None]
    l2 = [1,2,None,None,None]
    l = remove_none([l1,l2])
    assert l[0] == [1, 2]
    assert l[1] == l[0]
    
    l1 = [1,2,3,4,None]
    l2 = [1,2,3,None,5]
    l3 = [1,2,None,4,5]
    l4 = [1,None,3,4,5]
    l5 = [None,2,3,4,5]
    
    l = remove_none([l1,l2,l3,l4,l5])
    assert l[0] == []
    assert l[2] == l[1]
    assert l[3] == l[2]
    assert l[4] == l[3]
    assert l[4] == l[0]
    
    l1 = [1,2,3,None]
    l2 = l1
    l = remove_none([l1,l2])
    assert l[0] == l[1]
    
    with warnings.catch_warnings(record=True) as w:
        l = remove_none([[1,None,3,4],[1,2,3]])
        assert len(w) == 1
        assert "Arrays not te same length!!" in w[0].message
        
        assert l[0] == [1,3,4]
        assert l[1] == [1,3]
    
    taxo = dataToDict("taxo.csv")
    print len(taxo["__relevant__"])
    print taxo["__relevant__"]

