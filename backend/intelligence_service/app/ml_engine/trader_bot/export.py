import torch
import torch.nn as nn
from stable_baselines3 import PPO

class OnnxableSB3Policy(nn.Module):
    def __init__(self, policy):
        super().__init__()
        self.policy = policy

    def forward(self, observation):
        features = self.policy.extract_features(observation)
        latent_pi, _ = self.policy.mlp_extractor(features)
        logits = self.policy.action_net(latent_pi)
        
        return logits

model = PPO.load("model/ppo_trader_v2.zip")
policy = model.policy.to("cpu") 
onnxable_model = OnnxableSB3Policy(policy)
onnxable_model.eval()
dummy_input = torch.randn(1, 60, 17)

# 4. Export
print(f"Exporting with input shape: {dummy_input.shape}")
torch.onnx.export(
    onnxable_model,
    dummy_input,
    "ppo_hft.onnx",
    opset_version=11,
    input_names=["input"],
    output_names=["output"],
    dynamic_axes={"input": {0: "batch_size"}, "output": {0: "batch_size"}}
)

print("Model exported to ppo_hft.onnx")