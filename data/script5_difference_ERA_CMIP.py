# -*- coding: utf-8 -*-

import numpy as np
from netCDF4 import Dataset
import matplotlib.pyplot as plt
from batlow import *    

# interpolation tool
from scipy.interpolate import griddata
from vik import * 
import matplotlib.colors as colors

# tool to plot maps
import cartopy.crs as ccrs
import matplotlib.ticker as mticker
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# function to center around zero:

class MidpointNormalize(colors.Normalize):
	def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
		self.midpoint = midpoint
		colors.Normalize.__init__(self, vmin, vmax, clip)

	def __call__(self, value, clip=None):
		x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
		return np.ma.masked_array(np.interp(value, x, y), np.isnan(value))

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

ftsize=20
ftsize2=15

filename_cmip='thetao_Omon_CESM2_historical_r1i1p1f1_gr_201301-201412.nc'
filename_era5='SST_ERA5_201301.nc'

ncfile_cmip = Dataset(filename_cmip)
ncfile_era5 = Dataset(filename_era5)

var_cmip = ncfile_cmip.variables['thetao'][0,0,:,:]
lat_cmip = ncfile_cmip.variables['lat']; lat_cmip=np.array(lat_cmip)
lon_cmip = ncfile_cmip.variables['lon']; lon_cmip=np.array(lon_cmip)

var_era5= ncfile_era5.variables['sst'][0,:,:]-273.15
lat_era5 = ncfile_era5.variables['latitude']; lat_era5=np.array(lat_era5)
lon_era5 = ncfile_era5.variables['longitude'];lon_era5=np.array(lon_era5)

# the latitude/longitude variables are 1D and we need 2D: use meshgrid

grid_lon_era5,grid_lat_era5 = np.meshgrid(lon_era5,lat_era5)
grid_lon_cmip,grid_lat_cmip = np.meshgrid(lon_cmip,lat_cmip)

# the latitude/longitude coordinates should be in the shape(2,N): use ".ravel()" to get all the points from 2D to 1D 
# and "stack" to glue them together

points_cmip= np.stack([grid_lat_cmip.ravel(), grid_lon_cmip.ravel()], -1)

# now we can interpolate, using griddata
# the input is
#  - points: the (2,N) grid of points to interpolate 
#  - theta: the values to interpolate (as one long array, using .ravel())
#  - (grid_latera,grid_longera): the two 2D coordinates of the grid we interpolate into 

var_cmip_regridded = griddata(points_cmip, var_cmip.ravel(), (grid_lat_era5,grid_lon_era5),method='nearest')

## make a mask
var_cmip_regridded= np.ma.MaskedArray(var_cmip_regridded,mask=[(a>35) for a in var_cmip_regridded])

# plot using subplots:

# subplot1 
fig=plt.figure(figsize=(12,12))

# add cartopy arguments:
A=fig.add_subplot(3,1,1,projection=ccrs.PlateCarree())
A.coastlines(color='grey')
A.set_extent([-180,180,-90,0],ccrs.PlateCarree())
plt.title('ERA5 201301',fontsize=ftsize)
plt.pcolor(grid_lon_era5,grid_lat_era5,var_era5, vmin=-2,vmax=33,transform=ccrs.PlateCarree(),cmap=batlow_map)

# add axes labels
gl = A.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,alpha=0.5, linestyle='--')
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER

# choose where to put the ticks
gl.xlocator = mticker.FixedLocator([-180, -90, 0, 90, 180])
gl.ylocator = mticker.FixedLocator([0,-45, -90])

# customize the font
gl.xlabel_style = {'color': 'grey'}
gl.ylabel_style = {'color': 'grey'}

# colorbar
cbar = plt.colorbar()
cbar.ax.get_yaxis().labelpad = 15
cbar.ax.set_ylabel('SST [\xb0 C]',fontsize = ftsize2,rotation=270)

# subplot2
B=fig.add_subplot(3,1,2,projection=ccrs.PlateCarree())
B.coastlines(color='grey')
B.set_extent([-180,180,-90,0],ccrs.PlateCarree())
plt.title('CMIP regridded 201301',fontsize=ftsize)
plt.pcolor(grid_lon_era5,grid_lat_era5,var_cmip_regridded,vmin=-2,vmax=33,transform=ccrs.PlateCarree(),cmap=batlow_map)

# add axes labels
gl = B.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,alpha=0.5, linestyle='--')
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER
# choose where to put the ticks
gl.xlocator = mticker.FixedLocator([-180, -90, 0, 90, 180])
gl.ylocator = mticker.FixedLocator([0,-45, -90])
# customize the font
gl.xlabel_style = {'color': 'grey'}
gl.ylabel_style = {'color': 'grey'}

# add colorbar
cbar = plt.colorbar()
cbar.ax.get_yaxis().labelpad = 15
cbar.ax.set_ylabel('SST [\xb0 C]',fontsize = ftsize2,rotation=270)

# subplot3
C=fig.add_subplot(3,1,3,projection=ccrs.PlateCarree())
C.coastlines(color='grey')
C.set_extent([-180,180,-90,0],ccrs.PlateCarree())
plt.title('Difference (ERA5-CMIP) 201301',fontsize=ftsize)

# add the min, max and centre values for the blue-red colorbar:
mid_val=0; minvar = -13; maxvar = 8;

# plot using the limits
plt.pcolor(grid_lon_era5,grid_lat_era5,var_era5-var_cmip_regridded,transform=ccrs.PlateCarree(),cmap=vik_map,norm=MidpointNormalize(midpoint=mid_val,vmin=minvar, vmax=maxvar))

# add axes labels
gl = C.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,alpha=0.5, linestyle='--')
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER
# choose where to put the ticks
gl.xlocator = mticker.FixedLocator([-180, -90, 0, 90, 180])
gl.ylocator = mticker.FixedLocator([0,-45, -90])
# customize the font
gl.xlabel_style = {'color': 'grey'}
gl.ylabel_style = {'color': 'grey'}
cbar = plt.colorbar()
cbar.ax.get_yaxis().labelpad = 15
cbar.ax.set_ylabel('SST [\xb0 C]',fontsize = ftsize2,rotation=270)

###############

fig.tight_layout(pad=0.3)

plt.savefig('ERA5_CMIP_difference_sst_201301.png')
