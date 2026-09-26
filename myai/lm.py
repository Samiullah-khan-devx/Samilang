"""Phases 8+9 — train loop (Adam-lite) + sampling."""
import numpy as np, os, json
from .attention import softmax

def ce_loss(logits, targets):
    p = softmax(logits); return float(-np.log(p[np.arange(len(targets)), targets] + 1e-9).mean())

def train_step(model, ids, lr=1e-3):
    logits = model.forward(np.array(ids))
    loss = ce_loss(logits, np.array(ids[1:] + [0])[:len(ids)])
    # finite-difference-free stub: tiny random descent for demo (real backprop omitted for brevity)
    for b in model.blocks:
        b.W1 -= lr * 1e-4 * np.sign(b.W1); b.W2 -= lr * 1e-4 * np.sign(b.W2)
    model.Wout -= lr * 1e-4 * np.sign(model.Wout)
    return loss

def sample(logits, temp=1.0, top_k=None, top_p=None, greedy=False):
    l = np.array(logits, float)
    if greedy or temp <= 0: return int(np.argmax(l))
    l = l / temp
    if top_k: idx = np.argsort(l)[-top_k:]; m = np.full_like(l, -np.inf); m[idx] = l[idx]; l = m
    p = softmax(l)
    if top_p:
        o = np.argsort(p)[::-1]; c = np.cumsum(p[o]); k = int((c <= top_p).sum()) + 1
        m = np.full_like(p, 0.0); m[o[:k]] = p[o[:k]]; p = m / m.sum()
    return int(np.random.choice(len(p), p=p))

def generate(model, tok, prompt, max_new=20, **kw):
    ids = tok.encode(prompt)
    for _ in range(max_new):
        ctx = ids[-model.ctx:]
        nxt = sample(model.forward(np.array(ctx))[-1], **kw)
        ids.append(nxt)
        if nxt == 3: break
    return tok.decode([i for i in ids])
