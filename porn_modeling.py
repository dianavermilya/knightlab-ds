from scales import *
from filter_data import taxo, taxo_f, taxo_m
from regressions import bestExplained

other_scales = [scale for scale in scales if not(scale in porn_scales) and not(scale == "genderversion")]


fp = open("porn_models.txt", 'w')
fp.write("This document shows how well pornography habits predict other psycological scales\n\n")
fp.write("Total population:\n")
fp.write(str(bestExplained(taxo, other_scales+["genderversion"], porn_scales)))
fp.write("\n===========\n")
print ("\n===========\n")
fp.write("For women:\n")
fp.write(str(bestExplained(taxo_f, other_scales, porn_scales)))
fp.write("\n===========\n")
print ("\n===========\n")
fp.write("For men:\n")
fp.write(str(bestExplained(taxo_m, other_scales, porn_scales)))
fp.close()
