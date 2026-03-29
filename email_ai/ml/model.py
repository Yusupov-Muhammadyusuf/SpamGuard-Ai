import torch
import torch.nn as nn

class SpamClassifier(nn.Module):
    def __init__(self, vocab_size, embed_dim=64):
        super().__init__()

        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.fc = nn.Linear(embed_dim, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.embedding(x)
        x = x.mean(dim=1)
        x = self.fc(x)

        return self.sigmoid(x)
