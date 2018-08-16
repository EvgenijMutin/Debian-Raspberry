echo "17" > /sys/class/gpio/export
echo "out" > /sys/class/gpio/gpio17/direction
sleep 0.5
echo "17" > /sys/class/gpio/unexport
sleep 0.5
echo "27" > /sys/class/gpio/export
echo "out" > /sys/class/gpio/gpio27/direction
sleep 0.5
echo "27" > /sys/class/gpio/unexport
sleep 0.5
echo "22" > /sys/class/gpio/export
echo "out" > /sys/class/gpio/gpio22/direction
sleep 0.5
echo "22" > /sys/class/gpio/unexport
sleep 0.5
    
