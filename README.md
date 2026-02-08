# toykenizer

A from-scratch implementation of Byte Pair Encoding (BPE) tokenization, without any other dependencies in Python.

## Usage

```python
from toykenizer import BPETokenizer
import json

# Train a new tokenizer
tokenizer = BPETokenizer()
tokenizer.train("training text here", vocab_size=512)

# Encode and decode
tokens = tokenizer.encode("hello world")
text = tokenizer.decode(tokens)

# Save and load trained merges
merges = tokenizer.save()
with open("model.json", "w") as f:
    json.dump(merges, f)

other_tokenizer = BPETokenizer()
with open("model.json") as f:
    other_tokenizer.load(json.load(f))
```

## Pre-trained models

A tokenizer trained on Harry Potter text is included in `models/harry-potter-tokenizer/`.
