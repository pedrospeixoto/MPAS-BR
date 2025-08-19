# Author: Guilherme L. Torres Mendonça
# 15/03/2024

These are template scripts designed to automate the whole process of running a simulation with MPAS-A. The scripts can be run independently or automatically in sequence (for instance for sensitivity tests), and are enumerated following the needed steps to run a simulation, starting from the mesh generation. Scripts whose names do not start with a number are only auxiliary.

All input information needed for running the simulation should be entered in input_file.txt, in the format indicated there.

The needed conda environments to run the scripts can be installed by running 0_create_envs.sh.

With the correct input information and conda environments, to run a simulation one just needs to execute the scripts in the appropriate order, starting from 1_create_mesh.sh.
