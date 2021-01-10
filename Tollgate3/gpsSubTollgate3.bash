export ROS_DOMAIN_ID=2
ros2 run key_presses key_subscriber --ros-args --remap __node:=gps_key_listener -r key_presses_gr3:=action       #to listen GPS /action topic and perform basic moves
