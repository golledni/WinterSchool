# -*- coding: utf-8 -*-
#
# Winterschool 2021 - Alena and Alex 
#  
# Analysis and plotting of spatial data
###################################################

import numpy as np  # This will import the python numerical library.
# It can be utilised to perform a number of mathematical operations 
# on arrays such as trigonometric, statistical, and algebraic routines.

from netCDF4 import Dataset # This will enable to read in netcdf datasets.

import matplotlib.pyplot as plt # This is an interface to provide 
# a MATLAB-like way of plotting

from batlow import *    # to have a *fancy* colormap


ftsize=12

# read in the data
filename='thetao_Omon_CESM2_historical_r1i1p1f1_gr_201301-201412.nc' 
ncfile = Dataset(filename)

var = ncfile.variables['thetao'][:,:,45,180]  # select one location, all levels and timesteps
level = ncfile.variables['lev']
lat = ncfile.variables['lat']
time = ncfile.variables['time']

# to match time X levels
var=np.transpose(var)

plot=plt.pcolor(time,level,var)

plt.ylim(0,1500)
ax=plot.axes
ax.invert_yaxis()

# define time labels
x=(time[0:23])

label=['Jan13','Feb13','Mar13','Apr13','May13','Jun13','Jul13','Aug13','Sep13','Oct13','Nov13','Dec13',
'Jan14','Feb14','Mar14','Apr14','May14','Jun14','Jul14','Aug14','Sep14','Oct14','Nov14']

plt.ylabel('depth [m]',fontsize = ftsize)

# plot time ticks

plt.xticks(x,label,rotation='vertical')

plt.show()
