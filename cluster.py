# Authors : Vincent Michel, 2010
#           Alexandre Gramfort, 2010
#           Gael Varoquaux, 2010
# License: BSD 3 clause

print(__doc__)

import time as time
import numpy as np
import pylab as pl
import mpl_toolkits.mplot3d.axes3d as p3
from sklearn.cluster import Ward
from sklearn.datasets.samples_generator import make_swiss_roll
from filter_data import *

###############################################################################
# Parameters

db = 'taxo.csv'
keys = ['Pnviojv', 'Pnvioad','SxPrFAC'] #'sxdeny', 'SxPrFAC', 'lkemp']
n_clusters = 6

###############################################################################
#Generate dataset
taxo = dataToDict(db)
data = [taxo[key] for key in keys]
remove_none(data)
X = np.array(data).transpose()

###############################################################################
# Compute clustering
print("Compute unstructured hierarchical clustering...")
st = time.time()
ward = Ward(n_clusters=n_clusters).fit(X)
label = ward.labels_
print("Elapsed time: ", time.time() - st)
print("Number of points: ", label.size)

###############################################################################
# Plot result
fig = pl.figure()
ax = p3.Axes3D(fig)
ax.view_init(7, -80)
for l in np.unique(label):
    ax.plot3D(X[label == l, 0], X[label == l, 1], X[label == l, 2],
              'o', color=pl.cm.jet(np.float(l) / np.max(label + 1)))
pl.title('Without connectivity constraints')


###############################################################################
# Define the structure A of the data. Here a 10 nearest neighbors
from sklearn.neighbors import kneighbors_graph
connectivity = kneighbors_graph(X, n_neighbors=10)

###############################################################################
"""
# Compute clustering
print("Compute structured hierarchical clustering...")
st = time.time()
ward = Ward(n_clusters=6, connectivity=connectivity).fit(X)
label = ward.labels_
print("Elapsed time: ", time.time() - st)
print("Number of points: ", label.size)

###############################################################################
# Plot result
fig = pl.figure()
ax = p3.Axes3D(fig)
ax.view_init(7, -80)
for l in np.unique(label):
    ax.plot3D(X[label == l, 0], X[label == l, 1], X[label == l, 2],
              'o', color=pl.cm.jet(float(l) / np.max(label + 1)))
pl.title('With connectivity constraints')
"""
pl.show()