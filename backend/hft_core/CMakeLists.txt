cmake_minimum_required(VERSION 3.10)
project(stonks_hft)

# 1. Enable IntelliSense (compile_commands.json)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# 2. Automatically find ALL .cpp files in "src" and its subfolders
file(GLOB_RECURSE APP_SOURCES "src/*.cpp")

# 3. Create the executable using all the files we found
add_executable(stonks_hft ${APP_SOURCES})

# 4. Include paths
target_include_directories(stonks_hft PRIVATE include)
