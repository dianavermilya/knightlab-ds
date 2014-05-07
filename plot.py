from brute_force import Scatter
from scales import scales, porn_scales
from filter_data import taxo, taxo_f, taxo_m

#for scale in porn_scales:
#    Scatter(taxo_f, "negmas", scale)

for scale in porn_scales:
    Scatter(taxo_f, "ParaRat", scale)
