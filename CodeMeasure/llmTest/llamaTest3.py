import torch
import transformers
from accelerate import init_empty_weights, load_checkpoint_and_dispatch

model_id = "meta-llama/Meta-Llama-3-8B"

# Initialize empty model weights
with init_empty_weights():
    model = transformers.AutoModelForCausalLM.from_config(
        transformers.AutoConfig.from_pretrained(model_id)
    )

# Load model with disk offload
model = load_checkpoint_and_dispatch(
    model, model_id, device_map="auto", offload_folder="offload", offload_state_dict=True
)

# Create the pipeline
pipeline = transformers.pipeline(
    "text-generation", model=model, tokenizer=model_id, torch_dtype=torch.bfloat16
)

# Generate text
output = pipeline("Hey, how are you doing today?")
print(output)