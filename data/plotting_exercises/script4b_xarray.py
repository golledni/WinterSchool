# -*- coding: utf-8 -*-

import numpy as np
from netCDF4 import Dataset
from batlow import *    # to have a *fancy* colormap
import matplotlib.pyplot as plt

# tool to plot maps
import cartopy.crs as ccrs
import matplotlib.ticker as mticker
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

# xarray
import xarray as xr

ftsize=16

filename='../data/thetao_Omon_CESM2_historical_r1i1p1f1_gr_201301-201412.nc'
data=xr.open_dataset(filename)

# get the info on the file to know what to select
# print(data)

theta0=data.thetao.isel(time=0,lev=30)
point =data.thetao.sel(time="2013-01",lat=-79.5,lon=40.5,lev=400)


# get the PlateCarree projection, centered over longitude 0
ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=0.0))
ax.coastlines(color='grey')
ax.set_global()
plot=theta0.plot.pcolormesh(ax=ax,transform=ccrs.PlateCarree(), x='lon', 
    y='lat', cmap=batlow_map,vmin=0,vmax=20)

gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,alpha=0.5, linestyle='--')
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER


# choose where to put the ticks
gl.xlocator = mticker.FixedLocator([-180, -45, 0, 45, 180])
gl.ylocator = mticker.FixedLocator([90,60,30,0,-30, -60, -90])
gl.xlabels_top = False
gl.ylabels_right = False
# customize the font
gl.xlabel_style = {'color': 'grey', 'weight': 'bold'}
gl.ylabel_style = {'color': 'grey', 'weight': 'bold'}

# add the CTD point
plt.scatter(point.lat,point.lon,color='blue') # 60 W - 40 S

plt.show()



