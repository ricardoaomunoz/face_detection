 sudo usbip attach --remote=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}') --busid=1-5
 sudo chmod 777 /dev/video0