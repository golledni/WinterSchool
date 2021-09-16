# -*- coding: utf-8 -*-
#
# Winterschool 2021 - Alena and Alex 
#  
# Analysis and plotting of spatial data
###################################################

import numpy as np  # This will import the python numerical
# library. It can be utilised to perform a number of 
# mathematical operations on arrays such as trigonometric, 
# statistical, and algebraic routines.

from netCDF4 import Dataset # This will enable to read in 
# netcdf datasets.

import matplotlib.pyplot as plt # This is an interface to 
# provide a MATLAB-like way of plotting

from batlow import *    # to have a *fancy* colormap


ftsize=12

# read in the data
filename='thetao_Omon_CESM2_historical_r1i1p1f1_gr_201301-201412.nc' 
ncfile = Dataset(filename)

var = ncfile.variables['thetao'][0,0,:,:]
lat = ncfile.variables['lat']
lon = ncfile.variables['lon']


## make a mask

#var= np.ma.MaskedArray(var,mask=[(a>10) for a in var])

# create a mesh grid
#Lon,Lat=np.meshgrid(lon,lat)
#var= np.ma.MaskedArray(var,mask=[(a>10) for a in Lat])


#plot

plt.pcolor(lon,lat,var,cmap=batlow_map)

# add axes labels
plt.xlabel('longitude',fontsize = ftsize)
plt.ylabel('latitude',fontsize = ftsize)

# colorbar
cbar = plt.colorbar()
cbar.ax.get_yaxis().labelpad = 15
cbar.ax.set_ylabel('temperature [Celsius]',fontsize = ftsize,rotation=270)
plt.clim(0,20)


plt.show()
