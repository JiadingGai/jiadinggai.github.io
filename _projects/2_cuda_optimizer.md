---
layout: page
title: Multi-Agent CUDA Kernel Optimizer
description: Bottleneck-analyzer agents for CUDA diagnosis and optimization.
importance: 2
category: systems
---

This project builds a multi-agent framework for autonomous CUDA kernel optimization. The key idea is to use bottleneck analyzers as expert surrogates that reason from occupancy, memory behavior, SASS, NCU metrics, roofline analysis, and Hopper WGMMA/TMA utilization.

The framework was applied to kernel-benchmark tasks and production Hopper grouped-GEMM optimization work.
