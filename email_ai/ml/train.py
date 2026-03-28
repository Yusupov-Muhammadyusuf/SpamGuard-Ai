import pickle
import torch
import torch.nn as nn

from torch.utils.data import DataLoader
from ml.model import SpamClassifier
from ml.dataset import SpamDataset
from utils.preprocessing import clean_text
from utils.tokenizer import Tokenizer

def data_load(path):
    texts = []
    labels = []

    with open(path, encoding="utf-8") as file:
        for line in file:
            label, text = line.strip().split("\t")
            texts.append(clean_text(text))
            labels.append(1 if label == "spam" else 0)

    return texts, labels

def train():
    texts, labels = data_load("SMSSpamCollection")

    tokenizer = Tokenizer()
    tokenizer.fit(texts)

    vocab_size = len(tokenizer.word2idx) + 1

    dataset = SpamDataset(texts, labels, tokenizer)
    loader = DataLoader(dataset, batch_size=32, shuffle=True)

    model = SpamClassifier(vocab_size=vocab_size)
    criterion = nn.BCELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    for epoch in range(5):
        total_loss = 0

        for x, y in loader:
            y = y.float().unsqueeze(1)

            optimizer.zero_grad()
            preds = model(x)

            loss = criterion(preds, y)
            loss.backward()

            optimizer.step()

            total_loss += loss.item()
        
        print(f"Epoch: {epoch+1}, Loss: {total_loss / len(loader)}")

    torch.save(model.state_dict(), "spam_model.pth")
    print("Model saved!") 

    with open("tokenizer.pkl", "wb") as file:
        pickle.dump(tokenizer, file)

if __name__ == "__main__":
    train()