source devel/setup.bash


id=$1

## make directory
output_dir="./bag_file/$id/img"
if [ ! -d "$output_dir" ]; then
    echo "makng directory ..."
    mkdir -p "$output_dir"
    echo "directory created"
else
    echo "directory already exists"
fi

## record image
rosrun data_processing record_sync_data.py $id
