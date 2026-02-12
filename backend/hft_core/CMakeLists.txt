cmake_minimum_required(VERSION 3.17)
project(HFT_Engine)

set(CMAKE_CXX_STANDARD 17)

# --- 1. CONFIGURATION ---
# Point to your downloaded ONNX Runtime folder
set(ONNX_ROOT "${CMAKE_SOURCE_DIR}/onnxruntime-win-x64-1.16.3") 

# --- 2. INCLUDE PATHS (THE FIX) ---
# This tells the compiler to look in your local 'include' folder AND ONNX headers
include_directories(include)
include_directories("${ONNX_ROOT}/include")

# --- 3. GATHER SOURCES ---
file(GLOB SOURCES "src/*.cpp")

# --- 4. CREATE EXECUTABLE ---
add_executable(hft_trader ${SOURCES})

# --- 5. LINKING ---
# Link against the ONNX Runtime library
# Try linking the .lib first (Standard way)
target_link_libraries(hft_trader "${ONNX_ROOT}/lib/onnxruntime.lib")

# If MinGW complains about the .lib, comment the line above and uncomment this:
# target_link_libraries(hft_trader "${ONNX_ROOT}/bin/onnxruntime.dll")

# --- 6. AUTO-COPY DLL (Optional but helpful) ---
add_custom_command(TARGET hft_trader POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_if_different
    "${ONNX_ROOT}/lib/onnxruntime.dll"
    $<TARGET_FILE_DIR:hft_trader>)