import thinkstats2
import math
from filter_data import dataToDict, remove_none, restrict
import matplotlib.pyplot as plt
import rpy2.robjects as robjects
import itertools
from scales import *
r = robjects.r

#import agemodel


"""
Linear Regressions for our Data.

Broadly, This is a group of functions performing linear and multiple regressions for our data.
Specifically, we are investigating the relationship between pornography use and sexuality in relation to gender.

pornography use:
early use - Pnearex
violent - Pnvio
child - Pnchldjv & Pnchldad
hetero - Pnheter
homo - Pnhomo

and gender - genderversion

potential outcomes/correlates:
paraphilias - ParaRat
sadism - sadbehr
scatol - scatologia paraphilia factor scale
sadism fantasies - sadfanr
denial of sexual behaviors - sxdeny
and paraphilic / coercive - PCD
Masculine Adequacy - masadeq
Negative masculinity - negmas
hostility towards women - hoswom
anxiety towards women - anxwom
sexualization (hypsxrat, comsxfac, sxprfac)

Overall Plan:

Find related variables: correlation network
Perform Linear Regressions
Multiple linear regressions
Logistic Regressions
Linearizing Data
Consider Clustering models if we find success in multiple linear regressions.
Factor analysis,  and beyond...

"""
"""
taxo = dataToDict("taxo.csv")

xs = taxo["Exhibit"]
ys = taxo["ParaRat"]

print ys
[xs, ys] = remove_none([xs, ys])

print ys

inter, slope = thinkstats2.LeastSquares(xs, ys)
fxs, fys = thinkstats2.FitLine(xs, inter, slope)
res = thinkstats2.Residuals(xs, ys, inter, slope)
print "correlations:"
print thinkstats2.Corr(xs, ys)
print thinkstats2.Corr(ys, xs)

fig = plt.figure()
plt.plot(fxs, fys)
plt.scatter(xs, ys)
plt.show()


train_line, = plt.plot(range(1,d+1),avg_train_r2)
plt.hold(True)
test_line, = plt.plot(range(1,d+1),avg_test_r2)
plt.legend([train_line, test_line],['Average Training R^2','Average Testing R^2'],loc="upper left")
plt.xlabel('Number of Features')
plt.show()
"""








def RunModel(model, print_flag=True):
    """Submits model to r.lm and returns the result."""
    model = r(model)
    res = r.lm(model)
    if print_flag:
        PrintSummary(res)
    return res


def PrintSummary(res):
    """Prints results from r.lm (just the parts we want)."""
    flag = False
    lines = r.summary(res)
    lines = str(lines)

    for line in lines.split('\n'):
        # skip everything until we get to coefficients
        if line.startswith('Coefficients'):
            flag = True
        if flag:
            print line
    print


def ResStdError(res):
    """
    return a float of the residual standard error from a model result
    """
    lines = str(r.summary(res))
    for line in lines.split('\n'):
        # extract the residual standard error
        if line.startswith('Residual standard error'):
            rse = float(''.join(c for c in line.replace('Residual standard error: ','')[:6] if c.isdigit() or c == '.'))
    return rse


def makeModel(d, *scales):
    """
    given a a series of variables, try to model the first based on the rest.
    Returns the model string to be passed to RunModel
    """
    
    data = [d[scale] for scale in scales]
    
    #remove none values
    data = remove_none(data)
    if len(data[0]) == 0:
        print data, scales
    # create the r global objects
    for i in range(len(scales)):
        robjects.globalenv[str(scales[i])] = robjects.FloatVector(data[i])
    
    model = '{} ~ {}'.format(scales[0], ' + '.join(scales[1:]))
    return model


def allModels(d, *scales):
    """
    Create all possible models given the scales (with squaring)
    """
    
    # first, create a smaller dictionary, just of the data we are using
    data = {scale:d[scale] for scale in scales}
    scales = list(scales)

    # now, add the squares (except for the dependant)
    for scale in list(scales[1:]):
        name = scale+'2'
        data[name] = [datum**2 if not datum is None else None for datum in data[scale]]
        scales.append(name)
    
    # now form all possible combinations of explanitory variables
    explanitory_combinations = allSubsets(list(scales[1:]))
    
    model_results = []
    for combo in explanitory_combinations:
        model = makeModel(data, scales[0], *combo)
        power = modelPower(RunModel(model, print_flag=False), data[scales[0]])
        model_results.append((ResStdError(RunModel(model, print_flag=False)), power, model))
    
    model_results.sort()
    return model_results


def allSubsets(iterable):
    """
    returns list of every possible subset of the iterable
    """
    subsets = []    
    for i in range(1, len(iterable)+1):
        subsets.extend(itertools.combinations(iterable, i))
    return subsets

def modelPower(res, variable):
    """
    return the amount by which the standerd deviation has decreased using this model
    
    res: result from running the model
    variable: thing the model was measuring
    """
    
    # extract the residual standard error from the report
    std_er = ResStdError(res)
    var = [datum for datum in variable if not(datum is None)]
    
    # calculate the initial standard deviation
    std_dev =  math.sqrt(thinkstats2.Var(var, ddof = 1))
    
    # report improvement
    return (std_dev - ResStdError(res))/std_dev

def main(script, model_number=0):
    
    taxo = dataToDict("taxo.csv")
    reduced_taxo = {scale:taxo[scale] for scale in scales}
    taxo_m = restrict(reduced_taxo,'male')
    taxo_f = restrict(reduced_taxo,'female')
    
    print allModels(taxo, "HypSxRat", "genderversion", "Pnheter", "sxdeny")[:2]
    #print allModels(taxo, "ComsxFac", "genderversion", "Pnheter", "sxdeny")[:2]
    #print allModels(taxo, "SxPrFAC", "genderversion", "Pnheter", "sxdeny")[:2]
    #print allModels(taxo, "HypSxRat", "genderversion", "Pnheter", "SxPrFAC")[:2]
    
    print "\n ======== Gender Specific ========\n"
    print allModels(taxo_f, "HypSxRat", "Pnheter", "drug_use_teen")[:2]
    
    from brute_force import Scatter
    Scatter(taxo_f, "HypSxRat", "Pnheter")
    Scatter(taxo_f, "HypSxRat", "drug_use_teen")
    Scatter(reduced_taxo, "HypSxRat", "sxdeny")
    #hypsxrat = taxo["HypSxRat"]
    #gender = taxo["genderversion"]
    #Pnheter = taxo["Pnheter"]
    #sxdeny = taxo["sxdeny"]

    #comsxfac = taxo["ComsxFac"]
    #sxprfac = taxo["SxPrFAC"]
    
    #[sxdeny, hypsxrat, gender, Pnheter, comsxfac, sxprfac] = remove_none([sxdeny, hypsxrat, gender, Pnheter, comsxfac, sxprfac])
    #Pnheter2 = [d**2 for d in Pnheter]    
    #model_number = int(model_number)
    
    #plt.scatter(hypsxrat, gender)
    #plt.show()
    #plt.scatter(hypsxrat, Pnheter)
    #plt.show()    
    #plt.scatter(hypsxrat, sxdeny)
    #plt.show()
    # put the data into the R environment
    #robjects.globalenv['hypsxrat'] = robjects.FloatVector(hypsxrat)
    #robjects.globalenv['Pnheter'] = robjects.FloatVector(Pnheter)
    #robjects.globalenv['Pnheter2'] = robjects.FloatVector(Pnheter2)
    #robjects.globalenv['gender'] = robjects.FloatVector(gender)
    #robjects.globalenv['sxdeny'] = robjects.FloatVector(sxdeny)
    #robjects.globalenv['comsxfac'] = robjects.FloatVector(comsxfac)
    #robjects.globalenv['sxprfac'] = robjects.FloatVector(sxprfac)
    
    # run the models
    #models = ['hypsxrat ~ Pnheter',
    #          'hypsxrat ~ gender',
    #          'hypsxrat ~ Pnheter2 + Pnheter',
    #          'hypsxrat ~ Pnheter2 + Pnheter + gender',
    #          'Pnheter ~ gender',
    #          'hypsxrat ~ sxdeny',
    #          'hypsxrat ~ sxdeny + Pnheter',
    #          'hypsxrat ~ sxdeny + Pnheter + gender',
    #          'hypsxrat ~ comsxfac + sxprfac + sxdeny + gender + Pnheter']


    #model = models[model_number]
    #print model
    #std_dev =  math.sqrt(thinkstats2.Var(hypsxrat, ddof = 1))
    #print std_dev    
    #res = RunModel(model)
    #print (std_dev - ResStdError(res))/std_dev
    
    #RunModel(makeModel(taxo, 'HypSxRat', 'Pnheter', 'sxdeny'))
    
if __name__ == '__main__':
    import sys
    main(*sys.argv)
