#pragma once
#include <vector>
#include <string>
// --- MINGW COMPATIBILITY HACK START ---
// The ONNX headers use Microsoft-specific annotations that GCC/MinGW doesn't understand.
// We define them as empty macros to make the compiler ignore them.
#ifdef __MINGW32__
  #undef _Frees_ptr_opt_
  #undef _In_
  #undef _In_opt_
  #undef _Inout_
  #undef _Inout_opt_
  #undef _Out_
  #undef _Out_opt_
  #undef _Outptr_
  #undef _Outptr_result_buffer_maybenull_
  #undef _Check_return_
  #undef _Ret_maybenull_
  #undef _Ret_notnull_
  #undef _Post_writable_byte_size_
  #undef _Outptr_result_bytebuffer_all_maybenull_
  
  #define _Frees_ptr_opt_
  #define _In_
  #define _In_opt_
  #define _Inout_
  #define _Inout_opt_
  #define _Out_
  #define _Out_opt_
  #define _Outptr_
  #define _Outptr_result_buffer_maybenull_(X)
  #define _Check_return_
  #define _Ret_maybenull_
  #define _Ret_notnull_
  #define _Post_writable_byte_size_(X)
  #define _Outptr_result_bytebuffer_all_maybenull_(X)
  #define _Success_(X)
#endif
// --- MINGW COMPATIBILITY HACK END ---
#include <onnxruntime_cxx_api.h>

class PPOModel {
public:
    PPOModel(const std::string& model_path);
    
    // Returns: 0=Buy, 1=Sell, 2=Hold
    // Input: Flat vector of 60 * 17 = 1020 floats
    int predict(const std::vector<float>& input_data);

private:
    Ort::Env env_;
    Ort::Session session_{nullptr};
    
    // Model expects [Batch=1, Sequence=60, Features=17]
    std::vector<int64_t> input_shape_ = {1, 60, 17};
    
    const char* input_name_ = "input";
    const char* output_name_ = "output";
};