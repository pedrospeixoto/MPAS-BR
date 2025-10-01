import os

import pandas as pd

from vtxmpasmeshes.dataset_utilities import open_mpas_regional_file
from vtxmpasmeshes.mesh_generator import full_generation_process, \
    full_generation_process_gtm, cut_circular_region_beta, \
    cut_circular_region
from vtxmpasmeshes.mpas_plots import compare_plot_mpas_regional_meshes, \
    view_mpas_regional_mesh, plot_era5_grid, plot_wrf_grid, \
    plot_expected_resolution_rings

from vtxmpasmeshes.plot_utilities import plot_mpas_darray, \
    set_plot_kwargs, add_colorbar, \
    start_cartopy_map_axis, close_plot

import matplotlib as mpl
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import sys
from importlib import reload

DATA_FOLDER = '/storage/guilherme_torresmendonca/projeto_nudging_mpas/' \
    'vtx-mpas-meshes/data'

####################################################################
#                        USER INTERFACE                            #
####################################################################
# Site: Perdigao
lat_ref = 39.7136
lon_ref = -7.73

# Parameters
# These parameters define the changing in the resolution. Varying the distance
# from the center of mesh d, we define the expected grid spacing (S):
## 0 < d < size --> S = highres
## size < d < size + margin --> S = highres + lambda*(d-size)
## size + margin < d < alpha (not defined here) --> S = lowres
## alpha < d < beta (not defined here) --> S = lowres + lambda*(d-(size+margin))
size = 30 # s in the paper
highres = 10 # cgs in the paper
margin = 200 # m in the paper
lowres = 20 # mgs in the paper
numlayers = 8 # layers outside requested nominal radius
####################################################################


####################################################################
name = 's' + str(size).zfill(2) + '_m' + str(margin).zfill(3)
radius = size+margin
region_border = radius + (numlayers*lowres)*0.9

regional_mesh = DATA_FOLDER + '/' + name + '.region.grid.nc'
if not os.path.exists(regional_mesh):
    # Create a regional mesh at the desired location -> with 4 layers (?)
    print ('creating regional mesh centered at chosen location')
    full_generation_process_gtm(
        regional_mesh, 'doughnut',
        redo=False, do_plots=True, do_region=True,
        highresolution=highres, lowresolution=lowres,
        num_boundary_layers=numlayers,
        size=size, margin=margin,
        lat_ref=lat_ref, lon_ref=lon_ref,
    )
####################################################################