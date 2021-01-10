export ROS_DOMAIN_ID=2

ros2 run key_presses key_subscriber --ros-args --remap __node:=our_key_listener       #to listen our key presses topic and perform basic moves
