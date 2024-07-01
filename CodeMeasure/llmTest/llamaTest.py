import os
from huggingface_hub import snapshot_download
from transformers import pipeline
import torch

token = os.getenv("HUGGINGFACE_TOKEN")
model_id = "meta-llama/Meta-Llama-3-8B"
snapshot_download(repo_id=model_id, force_download=True, token=token)

textGenerator = pipeline(
    "text-generation", 
    model=model_id, 
    model_kwargs={"torch_dtype": torch.bfloat16}, 
    device_map="auto", 
    use_auth_token=token
)

result = textGenerator("Hey, how are you doing today?")
print(result)