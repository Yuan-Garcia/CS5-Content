from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("bigscience/bloom")
model = AutoModelForCausalLM.from_pretrained("bigscience/bloom")

prompt = "Explain what AI is. Explanation:"
inputs = tokenizer.encode(prompt, return_tensors="pt")
output = tokenizer.decode(model.generate(inputs, max_new_tokens=100)[0])
print(output.replace(prompt, ""))