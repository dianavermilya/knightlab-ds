import thinkstats2
from filter_data import dataToDict, remove_none
import matplotlib.pyplot as plt
import rpy2.robjects as robjects
r = robjects.r

import agemodel


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


def main(script, model_number=0):
    
    taxo = dataToDict("taxo.csv")
    hypsxrat = taxo["hypsxrat"]
    gender = taxo["genderversion"]
    Pnheter = taxo["Pnheter"]
    Pnheter2 = [d**2 for d in Pnheter]

    model_number = int(model_number)

    # put the data into the R environment
    robjects.globalenv['hypsxrat'] = robjects.FloatVector(hypsxrat)
    robjects.globalenv['Pnheter'] = robjects.FloatVector(Pnheter)
    robjects.globalenv['Pnheter2'] = robjects.FloatVector(Pnheter2)
    robjects.globalenv['gender'] = robjects.FloatVector(gender)

    # run the models
    models = ['hypsxrat ~ Pnheter',
              'hypsxrat ~ gender',
              'hypsxrat ~ Pnheter2 + Pnheter',
              'hypsxrat ~ Pnheter2 + Pnheter + gender',
              'Pnheter ~ gender']


    model = models[model_number]
    print model
    RunModel(model)


if __name__ == '__main__':
    import sys
    main(*sys.argv)
