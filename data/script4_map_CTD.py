# -*- coding: utf-8 -*-

import numpy as np
from netCDF4 import Dataset
from batlow import *    # to have a *fancy* colormap
import matplotlib.pyplot as plt

# tool to plot maps
import cartopy.crs as ccrs
import matplotlib.ticker as mticker
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

ftsize=10

filename='../data/thetao_Omon_CESM2_historical_r1i1p1f1_gr_201301-201412.nc'
ncfile = Dataset(filename)

var = ncfile.variables['thetao'][0,0,:,:]
lat = ncfile.variables['lat']
lon = ncfile.variables['lon']
lev = ncfile.variables['lev']

# get the PlateCarree projection, centered over longitude 0
ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=0.0))

# add coastlines
ax.coastlines(color='grey')

# it is  global file, but show only the southern hemisphere
ax.set_extent([-180, 180, -90, 0], ccrs.PlateCarree())


# create a mesh grid
Lon,Lat=np.meshgrid(lon,lat);

# plot the variable (+ *fancy* colormap)
plt.pcolor(Lon,Lat,var,transform=ccrs.PlateCarree(),cmap=batlow_map)

gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,alpha=0.5, linestyle='--')


# add axes labels
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER

# choose where to put the ticks
gl.xlocator = mticker.FixedLocator([-180, -90, 0, 90, 180])
gl.ylocator = mticker.FixedLocator([0,-30, -60, -90])

# customize the font
gl.xlabel_style = {'color': 'grey', 'weight': 'bold'}
gl.ylabel_style = {'color': 'grey', 'weight': 'bold'}


# colorbar
cbar = plt.colorbar(orientation='horizontal')
cbar.ax.get_yaxis().labelpad = 15
cbar.ax.set_title('temperature [Celsius]',fontsize = ftsize)
plt.clim(0,20)

# add the CTD point
plt.scatter(-60,-40,30,color='blue') # 60 W - 40 S

plt.show()



