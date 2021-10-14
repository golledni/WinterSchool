# -*- coding: utf-8 -*-
#
# Winterschool 2021 - Alena and Alex 
#  
# Analysis and plotting of spatial data
###################################################

import numpy as np  # This will import the python numerical library. It can be utilised to perform a 
#number of mathematical operations on arrays such as trigonometric, statistical, and algebraic routines.

from netCDF4 import Dataset # This will enable to read in netcdf datasets.

import matplotlib.pyplot as plt # This is an interface to provide a MATLAB-like way of plotting

from batlow import *    # to have a *fancy* colormap



ftsize=12

# read in the data
filename='thetao_Omon_CESM2_historical_r1i1p1f1_gr_201301-201412.nc' 
ncfile = Dataset(filename)

var = ncfile.variables['thetao'][0,:,:,180]
level = ncfile.variables['lev']
lat = ncfile.variables['lat']

# create a mesh grid
Lat,Level=np.meshgrid(lat,level);

#plot
plot=plt.pcolor(Lat,Level,var,cmap=batlow_map)
cont=plt.contour(Lat,Level,var,[0,10,20,30],colors='w')
plt.clabel(cont,fmt='%d',inline=1)

# revert axes
ax = plot.axes
ax.invert_yaxis()

# add axes labels
plt.xlabel('latitude',fontsize = ftsize)
plt.ylabel('depth [m]',fontsize = ftsize)

# colorbar

cbar = plt.colorbar(plot)
cbar.ax.get_yaxis().labelpad = 15
cbar.ax.set_ylabel('temperature [Celsius]',fontsize = ftsize,rotation=270)

plt.show()
