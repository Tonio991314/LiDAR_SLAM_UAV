mode=$1
id=$2

if [ $mode = "m" ]; then
    screen /dev/ttyACM0

elif [ $mode = "q" ]; then
    if [ $id ]; then
        screen -X -s $id quit
    else
        screen -ls
    fi
fi