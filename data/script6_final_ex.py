# -*- coding: utf-8 -*-

import numpy as np
from netCDF4 import Dataset
import matplotlib.pyplot as plt
from batlow import *    

# interpolation tool
from scipy.interpolate import griddata
from vik import * 
import matplotlib.colors as colors

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# function to center around zero:

class MidpointNormalize(colors.Normalize):
    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        colors.Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        # I'm ignoring masked values and all kinds of edge cases to make a
        # simple example...
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return np.ma.masked_array(np.interp(value, x, y), np.isnan(value))

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

ftsize=20

# load data

filename_2013='thetao_Omon_CESM2_historical_r1i1p1f1_gr_201301-201412.nc'
filename_1850='thetao_Omon_CESM2_historical_r1i1p1f1_gr_185001-185112.nc'

ncfile_2013 = Dataset(filename_2013)
ncfile_1850 = Dataset(filename_1850)

lat = ncfile_2013.variables['lat']; lat=np.array(lat)
lon = ncfile_2013.variables['lon']; lon=np.array(lon)
lev = ncfile_2013.variables['lev']; lev=np.array(lev)

# get the profiles and only the two months 
june_2013 = ncfile_2013.variables['thetao'][5,:,:,179]
june_2014 = ncfile_2013.variables['thetao'][17,:,:,179]
june_1850 = ncfile_1850.variables['thetao'][5,:,:,179]
june_1851 = ncfile_1850.variables['thetao'][17,:,:,179]

# get the mean of the two files
june_2013_14 = (june_2013 +june_2014)/2
june_1850_51 = (june_1850 +june_1851)/2

# plot using subplots:

fig=plt.figure(figsize=(10,15))

fig.add_subplot(3,1,1)

plt.title('ERA5 june 2013-2014',fontsize=ftsize)
plot=plt.pcolor(lat,lev,june_2013_14,cmap=batlow_map)

cbar = plt.colorbar()
cbar.ax.get_yaxis().labelpad = 15
cbar.ax.set_ylabel('theta [\xb0 C]',fontsize = ftsize,rotation=270)
plt.clim=(-2,33)
cbar.ax.tick_params(labelsize=ftsize)

ax=plot.axes
ax.invert_yaxis()
ax.tick_params(axis='both', labelsize=ftsize)

plt.xlabel('latitude',fontsize=ftsize)
plt.ylabel('depth [m]',fontsize=ftsize)

fig.add_subplot(3,1,2)
plt.title('ERA5 june 1850-1851',fontsize=ftsize)
plot=plt.pcolor(lat,lev,june_1850_51,cmap=batlow_map)

cbar = plt.colorbar()
cbar.ax.get_yaxis().labelpad = 15
cbar.ax.set_ylabel('theta [\xb0 C]',fontsize = ftsize,rotation=270)
cbar.ax.tick_params(labelsize=ftsize)
plt.clim=(-2,33)

ax=plot.axes
ax.invert_yaxis()
ax.tick_params(axis='both', labelsize=ftsize)

plt.xlabel('latitude',fontsize=ftsize)
plt.ylabel('depth [m]',fontsize=ftsize)

# compute the difference between the two time periods
diff = june_2013_14 - june_1850_51

fig.add_subplot(3,1,3)
plt.title('ERA5 (2013-14 - 1850-51)',fontsize=ftsize)

# add the min, max and centre values for the blue-red colorbar:
mid_val=0; minvar = -2.5; maxvar = 4.5;

# plot using the limits
plot=plt.pcolor(lat,lev,june_2013_14 - june_1850_51,cmap=vik_map,norm=MidpointNormalize(midpoint=mid_val,vmin=minvar, vmax=maxvar))

cbar = plt.colorbar()
cbar.ax.get_yaxis().labelpad = 15
cbar.ax.set_ylabel('difference [\xb0 C]',fontsize = ftsize,rotation=270)
cbar.ax.tick_params(labelsize=ftsize)

ax=plot.axes
ax.invert_yaxis()
ax.tick_params(axis='both', labelsize=ftsize)

plt.xlabel('latitude',fontsize=ftsize)
plt.ylabel('depth [m]',fontsize=ftsize)

plt.tight_layout()

plt.savefig('ERA5_difference_2013_1850_june.png')


#############################################################################################################################
# difference between cdo and python commands

filename_cdo='secres.nc'
ncfile_cdo = Dataset(filename_cdo)

# get the profiles and only the two months 
june_cdo = ncfile_cdo.variables['thetao'][0,:,:,0]

# get the difference between 2013 and 1850
diff = june_2013_14 - june_1850_51

fig=plt.figure(figsize=(10,15))

fig.add_subplot(3,1,1)
plt.title('theta python',fontsize=ftsize)
plot=plt.pcolor(lat,lev,diff,cmap=batlow_map)

cbar = plt.colorbar()
cbar.ax.get_yaxis().labelpad = 15
cbar.ax.set_ylabel('difference [\xb0 C]',fontsize = ftsize,rotation=270)
cbar.ax.tick_params(labelsize=ftsize)

ax=plot.axes
ax.invert_yaxis()
ax.tick_params(axis='both', labelsize=ftsize)
plt.xlabel('latitude',fontsize=ftsize)
plt.ylabel('depth [m]',fontsize=ftsize)

fig.add_subplot(3,1,2)
plt.title('ttheta cdo',fontsize=ftsize)
plot=plt.pcolor(lat,lev,june_cdo,cmap=batlow_map)

cbar = plt.colorbar()
cbar.ax.get_yaxis().labelpad = 15
cbar.ax.set_ylabel('difference [\xb0 C]',fontsize = ftsize,rotation=270)
cbar.ax.tick_params(labelsize=ftsize)

ax=plot.axes
ax.invert_yaxis()
ax.tick_params(axis='both', labelsize=ftsize)
plt.xlabel('latitude',fontsize=ftsize)
plt.ylabel('depth [m]',fontsize=ftsize)

fig.add_subplot(3,1,3)
plt.title('theta python - cdo',fontsize=ftsize)

# add the min, max and centre values for the blue-red colorbar:
mid_val=0; minvar = -2.5; maxvar = 4.5;

# plot using the limits
plot=plt.pcolor(lat,lev,diff - june_cdo,cmap=vik_map)#,norm=MidpointNormalize(midpoint=mid_val,vmin=minvar, vmax=maxvar))

cbar = plt.colorbar()
cbar.ax.get_yaxis().labelpad = 15
cbar.ax.set_ylabel('python - cdo [\xb0 C]',fontsize = ftsize,rotation=270)
cbar.ax.tick_params(labelsize=ftsize)

ax=plot.axes
ax.invert_yaxis()
ax.tick_params(axis='both', labelsize=ftsize)
plt.xlabel('latitude',fontsize=ftsize)
plt.ylabel('depth [m]',fontsize=ftsize)

plt.tight_layout()

fig.subplots_adjust(hspace=0.7)

plt.savefig('difference_cdo_python.png')

