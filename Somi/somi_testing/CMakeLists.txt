cmake_minimum_required(VERSION 2.8.3)
project(robosub)

## By default no optimization or debug flags are set use the following
## two lines to pass in these flags. Only use one at a time!
#set(CMAKE_BUILD_TYPE Debug) #Uncomment this line to enable debug symbols
#set(CMAKE_BUILD_TYPE Release) #Uncomment this for max optimization

#enable C++ 11 support
set(CMAKE_CXX_FLAGS "-Wall -Werror -std=c++11 ${CMAKE_CXX_FLAGS}")

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  cv_bridge
  image_transport
  sensor_msgs
  roslaunch
  tf
)

catkin_python_setup()

# Check all files in the launch folder for common mistakes

find_package(OpenCV REQUIRED)


catkin_package(
  INCLUDE_DIRS src
  CATKIN_DEPENDS roscpp rospy std_msgs cv_bridge image_transport sensor_msgs tf 
)

include_directories(
  src
  ${catkin_INCLUDE_DIRS}
  ${OpenCV_INCLUDE_DIRS}
)

# Mark executable scripts (Python etc.) for installation
install(PROGRAMS
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)


# Macros for declaring ros nodes and libraries 
include(cmake/ros-node.cmake)

# Constructors declares libraries that are convenient for building ros messages
add_subdirectory(src/sensor_check)

include(cmake/cppcheck.cmake)
include(cmake/clang-format.cmake)
include(cmake/pylint.cmake)
