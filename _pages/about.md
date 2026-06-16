---
layout: about
title: about
permalink: /
subtitle: Senior Applied Scientist, AWS Bedrock DS3 and AWS AI Labs

profile:
  align: right
  image: jiading-gai.jpg
  image_circular: true
  more_info: >
    <p>Seattle, WA</p>
    <p>&lt;first&gt;.&lt;last&gt;@gmail.com</p>
    <p><a href="https://github.com/JiadingGai">GitHub</a> / <a href="https://scholar.google.com/citations?hl=en&user=B0OBVgsAAAAJ">Google Scholar</a></p>

selected_papers: true
social: true

announcements:
  enabled: true
  scrollable: false
  limit: 3

latest_posts:
  enabled: false
---

I am a senior applied scientist and technical lead working on CUDA/GPU systems optimization, compiler engineering, machine learning infrastructure, and reinforcement learning systems for LLMs.

My recent work focuses on efficient LLM training and inference: FlashAttention-style kernels, shared-prompt attention for RL training, GPU kernel optimization agents, and compiler/runtime optimizations for AI accelerators. I have worked on production-scale ML systems at AWS Bedrock, AWS Q Developer, JP Morgan Chase, and Microsoft Research.

I am especially interested in systems that connect low-level performance engineering with large-scale learning workloads: CUDA, CUTLASS/CuTe, WGMMA/TMA, compiler scheduling, kernel autotuning, long-context inference, and RL training infrastructure.

## Current Highlights

- **DualKV shared-prompt FlashAttention.** Designed and implemented a CUDA forward/backward kernel and veRL data-pipeline redesign for large-rollout RL training.
- **Multi-agent CUDA kernel optimizer.** Built a kernel optimization framework using bottleneck analyzers for occupancy, memory behavior, SASS, NCU, roofline, and Hopper WGMMA/TMA diagnosis.
- **Compiler and accelerator systems.** Developed compiler transformations, scheduling optimizations, and backend code-generation improvements for AI accelerator workloads.
