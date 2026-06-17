---
layout: about
title: about
permalink: /
description: GPU systems, CUDA kernels, compiler engineering, ML infrastructure, and efficient LLM training.
subtitle: Senior Applied Scientist, AWS Bedrock DS3 and AWS AI Labs
profile:
  image: jiading-gai.jpg
---

I am a senior applied scientist and technical lead working on CUDA/GPU systems optimization, compiler engineering, machine learning infrastructure, and reinforcement learning systems for LLMs.

My recent work focuses on efficient LLM training and inference: FlashAttention-style kernels, shared-prompt attention for RL training, GPU kernel optimization agents, and compiler/runtime optimizations for AI accelerators. I have worked on production-scale ML systems at AWS Bedrock, AWS Q Developer, JP Morgan Chase, and Microsoft Research.

I am especially interested in systems that connect low-level performance engineering with large-scale learning workloads: CUDA, CUTLASS/CuTe, WGMMA/TMA, compiler scheduling, kernel autotuning, long-context inference, and RL training infrastructure.

## Current Highlights

- **DualKV shared-prompt FlashAttention.** Designed and implemented a CUDA forward/backward kernel and veRL data-pipeline redesign for large-rollout RL training.
- **Multi-agent CUDA kernel optimizer.** Built a kernel optimization framework using bottleneck analyzers for occupancy, memory behavior, SASS, NCU, roofline, and Hopper WGMMA/TMA diagnosis.
- **Compiler and accelerator systems.** Developed compiler transformations, scheduling optimizations, and backend code-generation improvements for AI accelerator workloads.

## Public Impact

Our high-frequency trading research was cited in the U.S. Senate hearing [*Computerized Trading: What Should the Rules of the Road Be?*](https://www.congress.gov/112/chrg/CHRG-112shrg80168/CHRG-112shrg80168.pdf#page=38).
