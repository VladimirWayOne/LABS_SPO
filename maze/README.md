#LABS_SPO/maze
Save python file in $ROS_PACKAGE_PATH/<your_directory>/src
Save .world and .png wherever you want, but note that the path to the image is indicated in .world (line 64)

rosrun stage_ros stageros <path to .world>

Open new terminal

rosrun $ROS_PACKAGE_PATH/<your_directory> <python file>
