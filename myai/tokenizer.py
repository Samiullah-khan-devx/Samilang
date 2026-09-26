"""Phases 3+4 — pipeline + word tokenizer with BPE stub."""
import re
from collections import Counter

def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())

def word_tokenize(text: str):
    return clean(text).split()

class Tokenizer:
    def __init__(self): self.stoi = {}; self.itos = []
    def train(self, texts, min_freq=1):
        c = Counter()
        for t in texts: c.update(word_tokenize(t))
        toks = ["<pad>", "<unk>", "<bos>", "<eos>"] + sorted(w for w, n in c.items() if n >= min_freq)
        self.stoi = {w: i for i, w in enumerate(toks)}; self.itos = toks
    def encode(self, text):
        return [2] + [self.stoi.get(w, 1) for w in word_tokenize(text)] + [3]
    def decode(self, ids):
        return " ".join(self.itos[i] if 0 <= i < len(self.itos) else "<unk>" for i in ids if i >= 4)
    @property
    def vocab_size(self): return len(self.itos)

def make_batches(ids, seq_len, batch_size):
    import numpy as np
    X, Y = [], []
    for i in range(0, len(ids) - seq_len, seq_len):
        X.append(ids[i:i+seq_len]); Y.append(ids[i+1:i+seq_len+1])
    X = np.array(X); Y = np.array(Y)
    return [(X[i:i+batch_size], Y[i:i+batch_size]) for i in range(0, len(X), batch_size)]
