#!/bin/bash
# Creates intermediate files from ERA5 nc files by means of https://github.com/NCAR/era5_to_int?tab=readme-ov-file
# !!!!! Requires era5_to_init code !!!!!

# Activate conda vtx_env environment
CONDA_PATH="$(conda info --root)"
source "$CONDA_PATH/etc/profile.d/conda.sh"
conda activate mpas-tools

# Select parameters from input_file.txt
echo "Reading input parameters:"
while IFS="=" read -r name value; do
    if [[ ! "$name" =~ ^\# ]]; then
        declare -r $name=$value
        echo $name":" $value
    fi
done < input_file.txt

# Go to WPS directory
cd $era5_to_int_dir

python3 era5_to_int.py --path $raw_input_data_dir -i ${date1}_"${time1:0:2}" ${date2}_"${time2:0:2}" 1

mv FILE* $intermediate_input_data_dir
