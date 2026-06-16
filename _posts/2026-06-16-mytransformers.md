---
layout: post
title: "transformer mt system: core math"
date: 2026-06-16 01:00:00 -0700
description: "Core Transformer math for a small German-to-English MT exercise."
tags: [nlp, pytorch, research]
categories: [notes]
related_posts: false
---

Design problem: learn $p(y \mid x)$ for German source tokens $x$ and English target tokens $y$. The implementation, [`mytransformers.py`](https://github.com/JiadingGai/exercise/blob/master/NLP/seq2seq/mytransformers.py), is adapted from Ben Trevett's ["6 - Attention is All You Need"](https://github.com/bentrevett/pytorch-seq2seq/blob/main/legacy/6%20-%20Attention%20is%20All%20You%20Need.ipynb).

Core model: tokenize [`bentrevett/multi30k`](https://github.com/JiadingGai/exercise/tree/master/NLP/seq2seq/data/multi30k), embed tokens plus positions, and train an encoder-decoder Transformer.

Embedding and masks.

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

Scaled dot-product and multi-head attention.

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

Encoder layer.

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

Encoder-decoder interaction. The encoder output $H_x=h_x^L$ becomes the decoder cross-attention memory.

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

Training minimizes teacher-forced token cross-entropy.

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

Validation uses `evaluate`, `calculate_bleu`, and local `corpus_bleu`; BLEU is an unsmoothed sanity check, not a standardized benchmark score.

```python
test_loss = evaluate(model, test_dataloader, criterion)
test_bleu = calculate_bleu(test_iter[:BLEU_EVAL_LIMIT], src_vocab, trg_vocab, model, device)
```
