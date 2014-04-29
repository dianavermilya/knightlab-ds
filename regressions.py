import thinkstats2
import math
from filter_data import dataToDict, remove_none, restrict, taxo, taxo_m, taxo_f
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

def ellementPower(model_tuple, d = None):
    """
    Returns the explanitory power of each variable used in the model
    """
    
    initial_std_er = model_tuple[0]
    model = model_tuple[-1]
    
    # first step is to extract the explanitory variables
    [dependant, variables] = model.split('~')
    dependant = dependant.strip()
    variables = [var.strip() for var in variables.split('+')]
    
    # if we only had one explanatory variable, don't bother
    if len(variables) <= 1:
        return (model_tuple[1], variables[0])

    # now create a model without each 
    models = []
    error_deltas = []
    for var_to_inspect  in variables:
        model = '{} ~ {}'.format(dependant, ' + '.join([var for var in variables if not(var == var_to_inspect)]))
        models.append(model)
        if not(d is None):
            model = makeModel(d, *([dependant] + [var for var in variables if not(var == var_to_inspect)]))

        # compute how much the error increased by removing that variable
        error_increase = ResStdError(RunModel(model, print_flag = False)) - initial_std_er
        error_deltas.append((error_increase, var_to_inspect))
    return error_deltas

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
        #scales.append(name)
    
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

def bestExplained(d, dependant_varialbes, explanitory_variables):
    """
    Sort the dependant variables by how well they are modeled by the
    explanitory variables.
    """
    
    expl_powers = []
    for dependant in dependant_varialbes:
        # find how well it is modeled
        expl_power = allModels(d, dependant, *explanitory_variables)[0][1]
        expl_powers.append((expl_power, dependant))

    expl_powers.sort(reverse = True)
    return expl_powers

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
    var = std_dev**2
    
    # report improvement
    if std_dev == 0:
        # print "\n ;( ;("+variable+"\n"
        return 0
    return (std_dev - ResStdError(res))/std_dev
    
    # return math.sqrt((var - ResStdError(res)**2)/var)

def main(script, model_number=0):
    
    #taxo = dataToDict("taxo.csv")
    #reduced_taxo = {scale:taxo[scale] for scale in scales}
    #taxo_m = restrict(reduced_taxo,'male')
    #taxo_f = restrict(reduced_taxo,'female')
    
    # models = allModels(taxo_m, "HypSxRat", "Pnheter", "Sadtot", "sxdeny", "ParaRat", "Voyeur", "SxPrFAC", "ComsxFac", "Fetish", "PCD")

    # model_tuple = models[0]
    # print model_tuple
    # print ellementPower(model_tuple, taxo_m)
    
    # models = allModels(taxo_f, "HypSxRat", "Pnheter", "Sadtot", "sxdeny", "ParaRat", "Voyeur", "SxPrFAC", "ComsxFac", "Fetish", "PCD")

    # model_tuple = models[0]
    # print model_tuple
    # print ellementPower(model_tuple, taxo_f)
    
    # models = allModels(taxo_m, "HypSxRat", "Pnheter", "Pnhomo", "Pnearex", "Pnchldjv", "Pnchldad", "Pnvio")

    # model_tuple = models[0]
    # print model_tuple
    # print ellementPower(model_tuple, taxo_m)
    
    # models = allModels(taxo_f, "HypSxRat", "Pnheter", "Pnhomo", "Pnearex", "Pnchldjv", "Pnchldad", "Pnvio")

    # model_tuple = models[0]
    # print model_tuple
    # print ellementPower(model_tuple, taxo_f)
    
    models = allModels(taxo_m, "Sadtot", "Pnheter", "Pnhomo", "Pnearex", "Pnchldjv", "Pnchldad", "Pnvio")

    model_tuple = models[0]
    print model_tuple
    print ellementPower(model_tuple, taxo_m)
    
    models = allModels(taxo_f, "Sadtot", "Pnheter", "Pnhomo", "Pnearex", "Pnchldjv", "Pnchldad", "Pnvio")

    model_tuple = models[0]
    print model_tuple
    print ellementPower(model_tuple, taxo_f)
    
    models = allModels(taxo_m, "negmas", "Pnheter", "Pnhomo", "Pnearex", "Pnchldjv", "Pnchldad", "Pnvio")

    model_tuple = models[0]
    print model_tuple
    print ellementPower(model_tuple, taxo_m)
    
    models = allModels(taxo_f, "negmas", "Pnheter", "Pnhomo", "Pnearex", "Pnchldjv", "Pnchldad", "Pnvio")

    model_tuple = models[0]
    print model_tuple
    print ellementPower(model_tuple, taxo_f)
    #print " === Models === "
    #print allModels(taxo, "ComsxFac", "genderversion", "Pnheter", "sxdeny")[:2]
    #print allModels(taxo, "SxPrFAC", "genderversion", "Pnheter", "sxdeny")[:2]
    #print allModels(taxo, "HypSxRat", "genderversion", 'ComsxFac', 'Voyeur', 'ParaRat', 'sxdeny', 'SxPrFAC')[:2]
    #print allModels(taxo, "sxdeny", "genderversion", "Pnheter")[:2]
    #print "\n ======== Gender Specific ========\n"
    #print allModels(taxo_f, "HypSxRat", "Pnheter", "drug_use_teen", "sxdeny")[:2]
    #print allModels(taxo_f, "HypSxRat", "Pnheter", "JuvDrgFc", "sxdeny")[:2]
    #print allModels(taxo_f, "HypSxRat", "Pnheter", "drug_use_teen", "Pnhomo")[:2]
    from brute_force import Scatter
    # Scatter(taxo_f, "HypSxRat", "Pnheter")
    # Scatter(taxo_m, "HypSxRat", "Pnheter")
    # Scatter(taxo_f, "Sadtot", "Pnheter")
    # Scatter(taxo_m, "Sadtot", "Pnheter")
    # Scatter(taxo_f, "negmas", "Pnchldjv")
    # Scatter(taxo_m, "negmas", "Pnchldjv")
    # Scatter(taxo_f, "negmas", "Pnearex")
    # Scatter(taxo_m, "negmas", "Pnearex")
    #Scatter(taxo_f, "HypSxRat", "Pnearex")
    #Scatter(taxo_m, "HypSxRat", "Pnearex")
    #Scatter(taxo_f, "HypSxRat", "JuvDrgFc")
    #Scatter(taxo_m, "HypSxRat", "JuvDrgFc")
    #Scatter(reduced_taxo, "HypSxRat", "sxdeny")
    
    porn_scales = ["Pnheter", "Pnhomo", "Pnearex", "Pnchldjv", "Pnchldad", "Pnvio", "Pnviojv", "Pnvioad"]
    other_scales = [scale for scale in scales if not(scale in porn_scales)]
    
    print bestExplained(taxo_f, other_scales, porn_scales)
    print bestExplained(taxo_m, other_scales, porn_scales)
    
if __name__ == '__main__':
    import sys
    main(*sys.argv)
