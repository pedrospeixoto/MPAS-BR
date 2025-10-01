#!/bin/bash

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

generate_dates() {
    local start_date=$1
    local end_date=$2

    # Convert start and end dates to seconds since Unix epoch for comparison
    start_seconds=$(date -d "$start_date" +%s)
    end_seconds=$(date -d "$end_date" +%s)

    current_seconds=$start_seconds

    # Generate dates from start to end date
    while [ $current_seconds -le $end_seconds ]; do
        current_date=$(date -d @$current_seconds +%Y%m%d)
        echo $current_date
        current_seconds=$((current_seconds + 86400))  # Increment by one day (86400 seconds)
    done
}

# generate dates and year-mont
dates=$(generate_dates $date1 $date2)
yearmonth=$(echo "${dates[0]}" | cut -c1-6)

if [ ! -d "$raw_input_data_dir" ]; then
    mkdir -p "$raw_input_data_dir"
fi

cd $raw_input_data_dir

cp ${simulation_template_scripts_dir}/download_* .

# Download 3D data
echo "downloading 3D data..."
echo "$dates" | bash download_era5_3D_data.sh $yearmonth

# Download surface data
echo "Downloading surface data..."
bash download_era5_surface_data.sh $yearmonth

# Download invariant data
echo "Downloading invariant data..."
bash download_era5_invariant_data.sh
