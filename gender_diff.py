from filter_data import *
from brute_force import *
from thinkstats2 import *
import thinkplot # for plotting
import random
from scales import scales

def genderCorrs(scale1, scale2):
    """
    Compute the corrolation differences between genders
    """
    
    # compute corrolations
    # corr = KeyCompare(taxo, scale1, scale2)
    corr_m = KeyCompare(taxo_m, scale1, scale2)
    corr_f = KeyCompare(taxo_f, scale1, scale2)
    
    return abs(corr_m) - abs(corr_f), scale1, scale2


def statSig(scale1, scale2, n = 1000):
    """
    Compute statisitcal significance of the gender differences for the two sales
    """
    
    actual_diff = genderCorrs(scale1, scale2)[0]
    
    rand_diffs = randomDiffs(scale1, scale2, n)
    
    # compute how many are greater that the actual_diff
    num_greater = 0
    for rdiff in rand_diffs:
        if abs(rdiff) > abs(actual_diff):
            num_greater += 1
    
    return float(num_greater)/n

def randomDiffs(scale1, scale2, n = 1000):
    """
    randomely partition the dictionary into two sets the sizes of the gender sets
    and compute the PMF for the difference in corrolations
    """
    
    # make sure everyone is one gender or the other
    genders = list(taxo['genderversion'])
    for g in genders:
        assert g in [0,1]
    
    diff = []
    for k in range(n):
        # now randomize the genders
        random.shuffle(genders)
        
        # create two new dicts based on this random gender
        mr = {}
        fr = {}
        
        for key in [scale1, scale2]:
            mr[key] = []
            fr[key] = []
            
            # populate the data into the two dictionaries
            for i in range(len(genders)):
                if genders[i] == 1:
                    mr[key].append(taxo[key][i])
                else:
                    fr[key].append(taxo[key][i])
        
        diff.append(abs(KeyCompare(mr, scale1, scale2)) - abs(KeyCompare(fr, scale1, scale2)))
    
    # round the number to essentially bin them
    # diff = [round(num, 3) for num in diff]
    # pmf = MakePmfFromList(diff)
    # thinkplot.Pmf(pmf)
    # thinkplot.show()
    return diff

def PMFDiff(scale1, scale2):
    """
    create (and plot) the PMF of the differences in corrolations between the scales
    based on gender.
    """
    
    # more the merrier (and slower)
    n = 1000
    
    # create the diff
    diff = randomDiffs(scale1, scale2, n)

    diff = [round(num, 3) for num in diff]
    pmf = MakePmfFromList(diff)
    thinkplot.Pmf(pmf)
    thinkplot.show()
    
def allDiffs():
    hyp_sex_factors = ["HypSxRat", "ComsxFac", "SxPrFAC"]
    threshold = 0.05
    
    fp = open("gender_diffs2.txt", 'w')
    for sex_scale in hyp_sex_factors:
        for scale in scales:
            if scale != sex_scale and scale != "genderversion":
                p_val = statSig(sex_scale, scale)
                # record significant differences
                if (p_val < threshold):
                    write_string = "Scales: {} {},\tDiff: {:.4F},\tp: {:.4F}\n".format(sex_scale, scale, genderCorrs(sex_scale, scale)[0], p_val)
                    print write_string
                    fp.write(write_string)
    
    fp.close()

if __name__ == "__main__":
    
    # print genderCorrs("HypSxRat", "Pnheter"), statSig("HypSxRat", "Pnheter")
    # print genderCorrs("HypSxRat", "sxdeny"), statSig("HypSxRat", "sxdeny")
    # print genderCorrs("HypSxRat", "ParaRat"), statSig("HypSxRat", "ParaRat")
    # print genderCorrs("HypSxRat", "Voyeur"), statSig("HypSxRat", "Voyeur")
    # print genderCorrs("HypSxRat", "ComsxFac"), statSig("HypSxRat", "ComsxFac")
    # print genderCorrs("HypSxRat", "SxPrFAC"), statSig("HypSxRat", "SxPrFAC")
    # print genderCorrs("HypSxRat", "PCD"), statSig("HypSxRat", "PCD")
    # print genderCorrs("HypSxRat", "Fetish"), statSig("HypSxRat", "Fetish")
    #allDiffs()
    
    PMFDiff("HypSxRat", "lkemp")
    
    
    
