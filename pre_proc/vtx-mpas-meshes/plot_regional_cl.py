import os
import argparse
from vtxmpasmeshes.mpas_plots import view_mpas_regional_mesh

# Create ArgumentParser object
parser = argparse.ArgumentParser(description=
                                 'Sensitivity test for varying mesh parameters.')
# Input arguments
parser.add_argument('--filename', type=str, default='circle.grid.nc')
parser.add_argument('--var', type=str, default='resolution')
parser.add_argument('--plot_rings', type=str, default=True)

# Parse the command line arguments
args = parser.parse_args()

view_mpas_regional_mesh(args.filename,outfile=f'{args.filename}_mesh.png',vname=args.var,do_plot_resolution_rings=eval(args.plot_rings))
