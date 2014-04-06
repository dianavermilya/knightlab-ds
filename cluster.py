# Authors : Vincent Michel, 2010
#           Alexandre Gramfort, 2010
#           Gael Varoquaux, 2010
# License: BSD 3 clause

print(__doc__)

import time as time
import numpy as np
import pylab as pl
import mpl_toolkits.mplot3d.axes3d as p3
from sklearn.cluster import Ward, KMeans
from sklearn.datasets.samples_generator import make_swiss_roll
from filter_data import *

###############################################################################
# Clustering Functions

def kMeans_inertia_from_keys(data, n_clusters):
	"""data should be a nested list where each internal list is a list of responses for a given peram name."""
	#clean and prepare data
	data = remove_none(data)
	lens = []
	for i in range(len(data)):
		lens.append(len(list(set(data[i]))))
	if max(lens) < 4:
		return -1
	if max(lens) < 8 or min(lens) < 4:
		n_clusters = 2
	data = np.array(data).transpose()
	# Compute clustering
	kmeans = KMeans(n_clusters = 6).fit(data)
	kMeans_plot(kmeans, data)
	print "inertia", kmeans.inertia_
	return kmeans.inertia_


########

def two_d_clusters():
	possibleKeys = no_digits_keys(taxo)
	n_clusters = 6
	l = []
	for key_a in possibleKeys:
		print key_a
		for key_b in possibleKeys:
			keys = [key_a, key_b]
			nested_list = [list(taxo[key]) for key in keys]

			try:
				inertia = kMeans_inertia_from_keys(nested_list, n_clusters)
				
				l.append([inertia, key_a, key_b])
			except ValueError:
				print "error"
	l.sort()
	return l

#print two_d_clusters()

def kMeans_plot (kMeans, X):
	"""data should be in scikit form"""
	if len(X[0]) != 3:
		return None
	label = kMeans.labels_
	fig = pl.figure()
	ax = p3.Axes3D(fig)
	ax.view_init(7, -80)
	for l in np.unique(label):
	    ax.plot3D(X[label == l, 0], X[label == l, 1], X[label == l, 2],
	              'o', color=pl.cm.jet(np.float(l) / np.max(label + 1)))
	pl.title('Without connectivity constraints')
	pl.show()

taxo = dataToDict('taxo.csv')
nested_list = [list(taxo[key]) for key in ['JuvDelBehSexual', 'drug_adult_rave', 'drug_adult_rave']]
kMeans_inertia_from_keys(nested_list, n_clusters=6)
plot_clusters(nested_list)


"""

	taxo = dataToDict('taxo.csv')
	keys = ['Pnviojv', 'Pnviojv', 'Pnviojv'] #'sxdeny', 'SxPrFAC', 'lkemp', 'Pnvioad']
	nested_list = [list(taxo[key]) for key in keys]
	n_clusters = 6
	print kMeans_inertia_from_keys(nested_list, n_clusters)



###############################################################################
# Plot result
fig = pl.figure()
ax = p3.Axes3D(fig)
ax.view_init(7, -80)
for l in np.unique(label):
    ax.plot3D(X[label == l, 0], X[label == l, 1], X[label == l, 2],
              'o', color=pl.cm.jet(np.float(l) / np.max(label + 1)))
pl.title('Without connectivity constraints')
pl.show()

"""
