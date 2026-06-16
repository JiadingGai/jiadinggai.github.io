---
layout: post
title: "Transformer MT System: Core Math"
date: 2026-06-16 01:00:00 -0700
description: "Core Transformer math for a small German-to-English MT exercise."
tags: [nlp, pytorch, research]
categories: [notes]
related_posts: false
---

Design problem: learn $p(y \mid x)$ for German source tokens $x$ and English target tokens $y$. The implementation, [`mytransformers.py`](https://github.com/JiadingGai/exercise/blob/master/NLP/seq2seq/mytransformers.py), is adapted from Ben Trevett's ["6 - Attention is All You Need"](https://github.com/bentrevett/pytorch-seq2seq/blob/main/legacy/6%20-%20Attention%20is%20All%20You%20Need.ipynb).

Core model: tokenize [`bentrevett/multi30k`](https://github.com/JiadingGai/exercise/tree/master/NLP/seq2seq/data/multi30k), embed tokens plus positions, and train an encoder-decoder Transformer.

## PROBLEM SCOPE

`mytransformers.py` implements a German-to-English sentence translation system on Multi30k. The scope is offline supervised training and local batch evaluation, not a hosted translation service: inputs are tokenized sentences, outputs are English token sequences, and the main constraints are vocabulary coverage, max decode length, validation loss, perplexity, and BLEU sanity checks.

## DATA PIPELINE

The script loads local mirrored `train`, `valid`, and `test` JSONL splits, tokenizes German and English with spaCy, builds source/target vocabularies from the training split, and reserves `<unk>`, `<pad>`, `<bos>`, and `<eos>`. `collate_fn` numericalizes each pair, adds BOS/EOS, pads variable-length sequences, and feeds padded tensors to `DataLoader`.

## MODEL CORE

The model core is an encoder-decoder Transformer built from token embeddings, learned positional embeddings, multi-head attention, position-wise feed-forward layers, residual connections, layer normalization, dropout, and source/target masks. The decoder combines causal self-attention with encoder-decoder cross-attention over the encoded German source sequence.

## EMBEDDING AND MASKS

```python
# Encoder.forward / Decoder.forward
h = self.tok_embedding(tokens) * self.scale + self.pos_embedding(pos)
h = self.dropout(h)

# Seq2Seq masks
src_mask = (src != self.src_pad_idx).unsqueeze(1).unsqueeze(2)
trg_mask = trg_pad_mask & torch.tril(torch.ones((trg_len, trg_len), device=self.device)).bool()
```

$$
h_x^0 = E_x[x]\sqrt{d_{\mathrm{model}}}+P_x,\qquad
h_y^0 = E_y[y]\sqrt{d_{\mathrm{model}}}+P_y
$$

$$
M_x(i)=1[x_i \ne \mathrm{pad}],\qquad
M_y(i,j)=1[y_i \ne \mathrm{pad}]\,1[j \le i]
$$

## SCALED DOT-PRODUCT AND MULTI-HEAD ATTENTION

```python
# MultiHeadAttentionLayer.forward
Q, K, V = self.fc_q(query), self.fc_k(key), self.fc_v(value)
energy = torch.matmul(Q, K.permute(0, 1, 3, 2)) / self.scale
energy = energy.masked_fill(mask == 0, -1e10)
attention = torch.softmax(energy, dim=-1)
x = torch.matmul(self.dropout(attention), V)
```

$$
\mathrm{Attn}(Q,K,V;M)=
\mathrm{softmax}\left(\frac{QK^\top}{\sqrt{d_k}}+M\right)V
$$

$$
\mathrm{MHA}(H_q,H_k,H_v)=
\mathrm{Concat}(A_1,\ldots,A_h)W^O,\qquad
A_r=\mathrm{Attn}(H_qW_r^Q,H_kW_r^K,H_vW_r^V;M)
$$

## ENCODER LAYER

```python
# EncoderLayer.forward
_src, _ = self.self_attention(src, src, src, src_mask)
src = self.self_attn_layer_norm(src + self.dropout(_src))
_src = self.positionwise_feedforward(src)
src = self.ff_layer_norm(src + self.dropout(_src))
```

$$
\tilde{h}_x^\ell=\mathrm{LN}\left(h_x^{\ell-1}+
\mathrm{MHA}(h_x^{\ell-1},h_x^{\ell-1},h_x^{\ell-1})\right)
$$

$$
h_x^\ell=\mathrm{LN}\left(\tilde{h}_x^\ell+
\mathrm{FFN}(\tilde{h}_x^\ell)\right),\qquad
\mathrm{FFN}(z)=\mathrm{ReLU}(zW_1+b_1)W_2+b_2
$$

## ENCODER-DECODER INTERACTION

The encoder output $H_x=h_x^L$ becomes the decoder cross-attention memory.

```python
# Seq2Seq.forward
enc_src = self.encoder(src, src_mask)
output, attention = self.decoder(trg, enc_src, trg_mask, src_mask)

# DecoderLayer.forward
_trg, _ = self.self_attention(trg, trg, trg, trg_mask)
trg = self.self_attn_layer_norm(trg + self.dropout(_trg))
_trg, attention = self.encoder_attention(trg, enc_src, enc_src, src_mask)
trg = self.enc_attn_layer_norm(trg + self.dropout(_trg))
```

$$
\tilde{h}_y^\ell=\mathrm{LN}\left(h_y^{\ell-1}+
\mathrm{MHA}(h_y^{\ell-1},h_y^{\ell-1},h_y^{\ell-1})\right)
$$

$$
\bar{h}_y^\ell=\mathrm{LN}\left(\tilde{h}_y^\ell+
\mathrm{MHA}(\tilde{h}_y^\ell,H_x,H_x)\right)
$$

$$
h_y^\ell=\mathrm{LN}\left(\bar{h}_y^\ell+
\mathrm{FFN}(\bar{h}_y^\ell)\right)
$$

## TRAINING OBJECTIVE

Training minimizes teacher-forced token cross-entropy. In `mytransformers.py`, the decoder consumes `trg[:, :-1]`, predicts the next token sequence `trg[:, 1:]`, ignores `<pad>` positions in `nn.CrossEntropyLoss`, clips gradients, and updates with Adam.

```python
output, _ = model(src, trg[:, :-1])
output = output.contiguous().view(-1, output_dim)
trg = trg[:, 1:].contiguous().view(-1)
loss = nn.CrossEntropyLoss(ignore_index=TRG_PAD_IDX)(output, trg)
```

$$
p_\theta(y_t \mid y_{1:t-1},x)=
\mathrm{softmax}(h_{y,t}^L W_{\mathrm{vocab}}+b)
$$

$$
\mathcal{L}=-\sum_t \log p_\theta(y_t \mid y_{1:t-1}, x),
\qquad
p_\theta(y\mid x)=\prod_t p_\theta(y_t \mid y_{1:t-1},x)
$$

## TRAINING SYSTEM

The implemented training system initializes weights with Xavier uniform, builds padded `DataLoader` batches, trains with Adam at `LEARNING_RATE = 0.0005`, and uses `nn.CrossEntropyLoss(ignore_index=TRG_PAD_IDX)`. Each train step zeroes gradients, runs teacher-forced decoding on `trg[:, :-1]`, flattens logits and targets, backpropagates, clips gradients with `CLIP = 1`, steps the optimizer, and optionally prints step loss plus running average loss through `LOSS_LOG_EVERY`.

The epoch loop reads `N_EPOCHS` from the environment, evaluates validation loss under `model.eval()` and `torch.no_grad()`, reports epoch time, train/validation loss, and perplexity, and saves `tut6-model.pt` whenever validation loss improves. For qualitative debugging, `SAMPLE_TRANSLATION_EVERY` controls printing a fixed German source sentence, the gold English target, and the current greedy translation. After training, the script reloads the best checkpoint and reports test loss, test perplexity, and test BLEU.

## GREEDY DECODING

Inference uses greedy decoding from `<bos>` until `<eos>`.

```python
# translate_sentence
output, attention = model.decoder(trg_tensor, enc_src, trg_mask, src_mask)
pred_token = output.argmax(2)[:, -1].item()
trg_indexes.append(pred_token)
```

$$
\hat{y}_t=\arg\max_v p_\theta(v \mid \hat{y}_{1:t-1},x)
$$

## INFERENCE SERVING

The script exposes local inference through `translate_sentence`, which tokenizes a sentence, encodes it once, then autoregressively appends the highest-probability target token up to `max_len=50`. A served system would wrap the same path with request batching, length limits, input validation, model versioning, and a clear policy for malformed or unsupported-language inputs.

## BLEU EVALUATION

Validation uses `evaluate`, `calculate_bleu`, and local `corpus_bleu`; BLEU is an unsmoothed sanity check, not a standardized benchmark score.

```python
test_loss = evaluate(model, test_dataloader, criterion)
test_bleu = calculate_bleu(test_iter[:BLEU_EVAL_LIMIT], src_vocab, trg_vocab, model, device)
```

For a dataset $D=\{(x_i,y_i)\}_{i=1}^{m}$, `calculate_bleu` greedily decodes candidates $\hat{C}_i$ and uses one reference set $R_i$ per candidate:

$$
C = \{\hat{C}_i\}_{i=1}^{m},\qquad
R = \{R_i\}_{i=1}^{m},\qquad
B_D = B(C,R)
$$

Here $B(C,R)$ is the local `corpus_bleu` calculation. For $N=4$ and uniform weights $w_n=\frac{1}{4}$, modified n-gram precision uses clipped counts:

$$
p_n =
\frac{
  \sum_i \sum_{g \in G_n(\hat{C}_i)}
    \min(N(g,\hat{C}_i), \max_{r \in R_i} N(g,r))
}{
  \sum_i \max(|\hat{C}_i| - n + 1, 0)
}
$$

With total candidate length $c$ and closest-reference total length $r$, the brevity penalty and BLEU score are:

$$
BP = \exp(\min(1 - \frac{r}{c}, 0)),
\qquad
c = \sum_i |\hat{C}_i|
$$

$$
BLEU =
BP \cdot \exp(\frac{1}{4}\sum_{n=1}^{4}\log p_n)
$$

Because the implementation is unsmoothed, it returns `0.0` when $c=0$ or when any clipped n-gram count is zero.

## MONITORING AND FAILURE MODES

The local script surfaces failures through validation loss, test perplexity, BLEU, and printed sample translations. Typical MT failures to watch are early `<eos>`, repeated words, unknown or copied names, wrong-language inputs, long sentences beyond the training distribution, tokenization mismatch, and quality drift when the data domain changes.
