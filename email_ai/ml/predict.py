import os
import sys
import pickle
import torch

from email_ai.ml.model import SpamClassifier
from email_ai.utils.preprocessing import clean_text
from email_ai.utils.tokenizer import Tokenizer
from email_ai import utils

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_tokenizer():
    tokenizer_path = os.path.join(BASE_DIR, "tokenizer.pkl")

    with open(tokenizer_path, "rb") as file:
        sys.modules['utils'] = utils 
        return pickle.load(file)

def load_model(vocab_size):
    model_path = os.path.join(BASE_DIR, "spam_model.pth")
    
    model = SpamClassifier(vocab_size)
    model.load_state_dict(torch.load(model_path))
    model.eval()

    return model

def predict(text, model, tokenizer, max_len=50):
    text = clean_text(text)
    tokens = tokenizer.encode(text)

    if len(tokens) < max_len:
        tokens += [0] * (max_len - len(tokens))
    else:
        tokens = tokens[:max_len]

    x = torch.tensor(tokens).unsqueeze(0)

    with torch.no_grad():
        pred = model(x)

    return "SPAM" if pred.item() > 0.5 else "HAM"