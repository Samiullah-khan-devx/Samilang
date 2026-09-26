"""Phase 7 — tiny Transformer LM (NumPy). d_model=32, 1-2 layers."""
import numpy as np
from .attention import softmax, SelfAttention

def layernorm(x, eps=1e-5):
    return (x - x.mean(-1, keepdims=True)) / np.sqrt(x.var(-1, keepdims=True) + eps)

class Block:
    def __init__(self, d_model, d_ff, seed):
        r = np.random.default_rng(seed)
        self.attn = SelfAttention(d_model, seed)
        self.W1 = r.normal(0, 0.5, (d_model, d_ff)); self.b1 = np.zeros(d_ff)
        self.W2 = r.normal(0, 0.5, (d_ff, d_model)); self.b2 = np.zeros(d_model)
    def __call__(self, x):
        a, w = self.attn(layernorm(x))
        x = x + a
        h = np.maximum(0, layernorm(x) @ self.W1 + self.b1) @ self.W2 + self.b2
        return x + h, w

class TinyTransformer:
    def __init__(self, vocab=64, d_model=32, d_ff=64, layers=2, ctx=16, seed=0):
        r = np.random.default_rng(seed)
        self.ctx = ctx; self.d_model = d_model
        self.tok_emb = r.normal(0, 0.5, (vocab, d_model))
        self.pos = self._sinusoidal(ctx, d_model)
        self.blocks = [Block(d_model, d_ff, seed + i + 1) for i in range(layers)]
        self.Wout = r.normal(0, 0.5, (d_model, vocab))
    def _sinusoidal(self, n, d):
        p = np.zeros((n, d)); pos = np.arange(n)[:, None]
        div = np.exp(np.arange(0, d, 2) * -(np.log(10000.0) / d))
        p[:, 0::2] = np.sin(pos * div); p[:, 1::2] = np.cos(pos * div)
        return p
    def forward(self, ids):
        x = self.tok_emb[ids] + self.pos[:len(ids)]
        for b in self.blocks: x, _ = b(x)
        return layernorm(x) @ self.Wout  # (T, vocab) logits
    def n_params(self):
        n = self.tok_emb.size + self.Wout.size
        for b in self.blocks: n += b.attn.Wq.size * 4 + b.W1.size + b.W2.size
        return int(n)
