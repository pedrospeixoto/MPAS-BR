import os

import pandas as pd

from vtxmpasmeshes.dataset_utilities import open_mpas_regional_file
from vtxmpasmeshes.mesh_generator import full_generation_process, \
    cut_circular_region_beta, cut_circular_region
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
PATH_LIMITED_AREA = '/storage/guilherme_torresmendonca/MPAS-Limited-Area'
sys.path.append('/storage/guilherme_torresmendonca/projeto_nudging_mpas/' \
    'vtx-mpas-meshes/vtxmpasmeshes')


# SITE: perdigao
lat_ref = 39.7136
lon_ref = -7.73

highres = 3 # cgs
lowres = 20 # mgs
numlayers = 8 # layers outside requested nominal radius

details = {}
grids = []
for margin in [#50,
               #75,
               100,
               #125,
               #150, 250
               ]:
    for size in [#15,
                 #20, 25,
                 30,# 35,
                 #50
                 ]:

        name = 'senst_s' + str(size).zfill(2) + '_m' + str(margin).zfill(3)
        folder = DATA_FOLDER + '/' + name + '/'
        basename = folder + name

        global_mesh = basename + '.grid.nc'
        if not os.path.exists(global_mesh):
            os.system('mkdir -p ' + folder)

            # I do a global mesh centered at 0,0 -> to use in MPAS workflow
            print ('creating global mesh centered at 0,0 for mpas workflow')
            full_generation_process(
                global_mesh, 'doughnut',
                redo=False, do_plots=False, do_region=False,
                highresolution=highres, lowresolution=lowres,
                size=size, margin=margin,
                lat_ref=0., lon_ref=0.,
            )

        radius = size+margin
        region_border = radius + (numlayers*lowres)*0.9
        configid = '99' + str(size).zfill(2) + str(margin).zfill(3)
        details[name] = {
            'globalfile': global_mesh,
            'configid': configid,
            'size': size,
            'margin': margin,
            'radius': radius,
            'region_border': region_border,
        }

        with open(DATA_FOLDER + '/' + name + '/config.' + configid + '.txt', 'w') as f:
            f.write('mesh=' + name + '.grid.nc \n')
            f.write('resolution=3' + '\n')
            f.write('inner_size=' + str(size) + '\n')
            f.write('radius=' + str(radius) + '\n')
            f.write('region_border=' + str(region_border) + '\n')
            f.write('num_boundary_layers=8' + '\n')
            f.write('product=raw' + '\n')
            f.write('max_num_domains=2' + '\n')
            f.write('time_integration_order=2' + '\n')
            f.write('two_way_nesting=false' + '\n')
            f.write('stream_list=\'reduced\'' + '\n')
            f.write('final_vars=\'reduced\'' + '\n')
            f.write('levs=\'as_vortex\'' + '\n')

        regional_mesh = DATA_FOLDER + '/' + name + '.region.grid.nc'
        if not os.path.exists(regional_mesh):
            # I do a regional mesh at my location -> with 4 layers
            print ('creating regional mesh centered at chosen location')
            full_generation_process(
                regional_mesh, 'doughnut',
                redo=False, do_plots=False, do_region=True,
                highresolution=highres, lowresolution=lowres,
                num_boundary_layers=numlayers,
                size=size, margin=margin,
                lat_ref=lat_ref, lon_ref=lon_ref,
            )

        f = DATA_FOLDER + '/' + name + '.mpaswrf_mesh.png'
        if not os.path.isfile(f):
            print('MPAS WRF Plots')
            view_mpas_regional_mesh(regional_mesh,
                                    outfile=f,
                                    do_plot_resolution_rings=True,
                                    do_plot_era5_grid=False,
                                    do_plot_wrf_grid=True,
                                    vname='resolution')

        vname = 'resolution'
        units = 'km'

        ds = open_mpas_regional_file(regional_mesh, full=True)

        myats = ds.attrs

        ax = plt.axes(projection=ccrs.PlateCarree())
        zorder = 2
        ax.add_feature(cfeature.BORDERS, linestyle=':', zorder=zorder)
        ax.stock_img()
        ax.coastlines(resolution='10m', zorder=zorder + 1)

        gl = ax.gridlines(draw_labels=True, alpha=0., linestyle='--',
                          zorder=zorder + 2)
        gl.top_labels = False
        gl.right_labels = False

        plot_kwargs = set_plot_kwargs(ds[vname])
        plot_mpas_darray(ds, vname, ax=ax, title='', lat_ref=0.,
                         lon_ref=0., border_radius=None,
                         **plot_kwargs)
        plot_expected_resolution_rings(ds, ax=ax)
        add_colorbar(ax, label=vname + ' (' + units + ')', **plot_kwargs)
        close_plot(outfile=DATA_FOLDER + '/' + name + '.mpasmesh.png',
                   size_fig=[6, 4])

        ax = plt.axes(projection=ccrs.PlateCarree())
        zorder = 2
        ax.add_feature(cfeature.BORDERS, linestyle=':', zorder=zorder)
        ax.stock_img()
        ax.coastlines(resolution='10m', zorder=zorder + 1)

        gl = ax.gridlines(draw_labels=True, alpha=0., linestyle='--',
                          zorder=zorder + 2)
        gl.top_labels = False
        gl.right_labels = False

        plot_kwargs = set_plot_kwargs(ds[vname])
        plot_mpas_darray(ds, vname, ax=ax, title='', lat_ref=0.,
                         lon_ref=0., border_radius=None,
                         **plot_kwargs)
        plot_expected_resolution_rings(ds, ax=ax)
        plot_wrf_grid(ds, ax=ax)
        add_colorbar(ax, label=vname + ' (' + units + ')', **plot_kwargs)
        close_plot(outfile=DATA_FOLDER + '/' + name + '.mpaswrfmesh.png',
                   size_fig=[6, 4])

        for border_radius in [size + 10, radius, region_border,
                              region_border + 200]:
            ax = plt.axes(projection=ccrs.PlateCarree())
            zorder = 2
            ax.add_feature(cfeature.BORDERS, linestyle=':', zorder=zorder)
            ax.stock_img()
            ax.coastlines(resolution='10m', zorder=zorder + 1)

            gl = ax.gridlines(draw_labels=True, alpha=0., linestyle='--',
                              zorder=zorder + 2)
            gl.top_labels = False
            gl.right_labels = False

            plot_kwargs = set_plot_kwargs(ds[vname].where(ds['cellDistance']
                                                          <= border_radius))
            plot_mpas_darray(ds, vname, ax=ax, title='',
                             border_radius=border_radius,
                             **plot_kwargs)
            plot_expected_resolution_rings(ds, ax=ax)
            plot_wrf_grid(ds, ax=ax)
            add_colorbar(ax, label=vname + ' (' + units + ')', **plot_kwargs)
            ax.set_title(str(int(border_radius)) + 'km zoom', fontsize=14)
            close_plot(outfile=DATA_FOLDER + '/' + name + '.regionmesh.' +
                               str(border_radius) + '.png', size_fig=[6, 4])