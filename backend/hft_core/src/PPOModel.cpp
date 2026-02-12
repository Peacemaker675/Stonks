#include "PPOModel.hpp"
#include <algorithm>
#include <iostream>
#include <vector>

PPOModel::PPOModel(const std::string& model_path) 
    : env_(ORT_LOGGING_LEVEL_WARNING, "HFT_PPO") {
    
    Ort::SessionOptions session_options;
    session_options.SetIntraOpNumThreads(1);
    session_options.SetGraphOptimizationLevel(GraphOptimizationLevel::ORT_ENABLE_ALL);

    // Load the ONNX model
    // specific to Windows wstring path requirement, or use generic string on Linux
#ifdef _WIN32
    std::wstring w_path(model_path.begin(), model_path.end());
    session_ = Ort::Session(env_, w_path.c_str(), session_options);
#else
    session_ = Ort::Session(env_, model_path.c_str(), session_options);
#endif
}

int PPOModel::predict(const std::vector<float>& input_data) {
    // 1. Prepare Memory
    auto memory_info = Ort::MemoryInfo::CreateCpu(OrtArenaAllocator, OrtMemTypeDefault);
    
    // 2. Create Tensor
    // We pass the flat data, but specify the 3D shape {1, 60, 17}
    Ort::Value input_tensor = Ort::Value::CreateTensor<float>(
        memory_info, 
        const_cast<float*>(input_data.data()), 
        input_data.size(), 
        input_shape_.data(), 
        input_shape_.size()
    );

    // 3. Run Inference
    const char* input_names[] = {input_name_};
    const char* output_names[] = {output_name_};

    auto output_tensors = session_.Run(
        Ort::RunOptions{nullptr}, 
        input_names, &input_tensor, 1, 
        output_names, 1
    );

    // 4. Get Output (Logits)
    float* logits = output_tensors[0].GetTensorMutableData<float>();
    
    // 5. ArgMax (0=Buy, 1=Sell, 2=Hold) - Assuming 3 discrete actions
    int best_action = 0;
    float max_val = logits[0];
    
    for (int i = 1; i < 3; ++i) {
        if (logits[i] > max_val) {
            max_val = logits[i];
            best_action = i;
        }
    }
    return best_action;
}