"""Phase 6 — scaled dot-product + self-attention (NumPy)."""
import numpy as np

def softmax(x, axis=-1):
    e = np.exp(x - x.max(axis=axis, keepdims=True)); return e / e.sum(axis=axis, keepdims=True)

def scaled_attention(Q, K, V, mask=None):
    d = Q.shape[-1]
    s = Q @ K.transpose(0, 2, 1) / np.sqrt(d) if Q.ndim == 3 else Q @ K.T / np.sqrt(d)
    if mask is not None: s = np.where(mask, s, -1e9)
    w = softmax(s); return w @ V, w

class SelfAttention:
    def __init__(self, d_model, seed=0):
        r = np.random.default_rng(seed)
        self.Wq = r.normal(0, 0.5, (d_model, d_model)); self.Wk = r.normal(0, 0.5, (d_model, d_model))
        self.Wv = r.normal(0, 0.5, (d_model, d_model)); self.Wo = r.normal(0, 0.5, (d_model, d_model))
    def __call__(self, x):
        Q, K, V = x @ self.Wq, x @ self.Wk, x @ self.Wv
        n = x.shape[0]; mask = np.tril(np.ones((n, n), bool))  # causal
        o, w = scaled_attention(Q[None], K[None], V[None], mask)
        return (o[0] @ self.Wo), w[0]
