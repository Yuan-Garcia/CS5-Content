from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F

model_id = "distilbert-base-uncased-finetuned-sst-2-english"
tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path=model_id)
model = AutoModelForSequenceClassification.from_pretrained(pretrained_model_name_or_path=model_id)

classifier = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

trainData = ["I've been waiting for a HuggingFace Course my whole life.", "I hate this so much!"]

result = classifier(trainData)
print(result)

# in PyTorch
""" Tokenization:
    - splits text into smaller units (tokens)
    - padding: for NLP, we need to have the same length for each input, tokenizers can pad the input
      to achieve uniform length
    - truncation: if the input is too long, we can truncate it to fit the model's input size
    - tokenizer will convert each correspondind token to an integer ID
    - different types of tokenizers: WordPiece, BytePair Encoding, SentencePiece, etc.
"""
# pt = pytorch format
# tokenizer: preprocesses trainData
batch = tokenizer(trainData, padding=True, truncation=True, max_length=512, return_tensors="pt")
print(batch)

""" 
    with torch.no_grad(): disables gradient, speeds up computation
    **batch: unpacks the dictionary into keyword arguments
    print(outputs.logits): the raw output of the model

    post-processing + prediction:
    F.softmax: converts the raw output into probabilities
    dim=1: specifies softmax applied along second dimension
    torch.argmax: returns the index of the highest probability, corresponds w predicted class

"""
with torch.no_grad():
    outputs = model(**batch)
    print(outputs.logits)
    predictions = F.softmax(outputs.logits, dim=1)
    print(predictions)
    labels = torch.argmax(predictions, dim=1)
    print(labels)