---
layout: page
title: DualKV
description: Shared-prompt FlashAttention for efficient RL training with large rollouts and long contexts.
importance: 1
category: systems
related_publications: true
---

DualKV removes redundant shared-prompt attention work in large-rollout RL training by combining a FlashAttention-style CUDA forward/backward kernel with a veRL data-pipeline redesign.

The project targets long-context, many-rollout training regimes where the prompt is shared but completions diverge. The result is better policy-update throughput and lower wasted computation while keeping exact attention semantics.

**Links:** [paper](https://arxiv.org/abs/2605.15422), [code](https://github.com/amazon-science/dualkv-flash-attn-for-rl).
