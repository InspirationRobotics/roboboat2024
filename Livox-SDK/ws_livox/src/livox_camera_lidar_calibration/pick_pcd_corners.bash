#!/bin/bash

cd ../../data/pcdFiles
ls 

result_path="./corner_lidar.txt"

read -r -p "Would you like to delete previously saved lidar corners? [y/n] " response
case "$response" in
    [yY][eE][sS]|[yY]) 
        : > $result_path
        ;;
    *)
        # do nothing for now
        ;;
esac

# iterate over all the pcd files
for file in *.pcd; do
    echo "==================================="
    echo "Launching $file using pcl_viewer"
    echo "Press SHIFT + LEFT CLICK to select a point."
    echo "Start from the top / top left of the board and go counter-clockwise until all 4 corners are marked."
    echo "Press Q to finish point picking and move on to the next point cloud."
    echo "Press H for help on how to navigate the point cloud visualization."
    echo $file >> $result_path
    while true; do
        output=`pcl_viewer -use_point_picking $file | grep "Point index"`
        echo "$output"
        num_line=`wc -l <<< "$output"`
        echo $num_line
        if [ $num_line -eq 4 ]; then
            echo "$output" | sed 's/\[//g; s/\]//g; s/,//g' | cut -d " " -f8,9,10 |\
            sed '1 i 1' | sed '3 i 2' | sed '5 i 3' | sed '7 i 4' |\
            tee -a $result_path
            break
        else
            echo "You didn't pick 4 points! Try again."
        fi
    done
done
