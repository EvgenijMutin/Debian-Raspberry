while true; do  
    echo "14" > /sys/class/gpio/export
    echo "out" > /sys/class/gpio/gpio14/direction
    sleep 0.5
    echo "14" > /sys/class/gpio/unexport
    sleep 0.5
    echo "15" > /sys/class/gpio/export
    echo "out" > /sys/class/gpio/gpio15/direction
    sleep 0.5
    echo "15" > /sys/class/gpio/unexport
    sleep 0.5
    echo "26" > /sys/class/gpio/export
    echo "out" > /sys/class/gpio/gpio26/direction
    sleep 0.5
    echo "26" > /sys/class/gpio/unexport
    sleep 0.5
done 

