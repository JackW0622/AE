#!/usr/bin/env python3
"""
inject_noise.py

Reads a numeric CSV, replaces zero-valued entries with mixed-distribution noise,
and writes out a new CSV with injected noise for richer audio output.
"""
import pandas as pd
import numpy as np
import os

# === User Parameters ===
input_csv  = '/Users/haoyangwang/Desktop/Barcode creation/test 2 (renewed).csv'    # Path to your numeric CSV
output_csv = '/Users/haoyangwang/Desktop/Barcode creation/test 2 (random).csv'      # Desired output path

# === Noise parameters ===
gauss_mean   = 0.0    # Mean for Gaussian component
gauss_std    = 0.2    # Std dev for Gaussian component
uniform_low  = -1.0   # Min for uniform component
uniform_high =  1.0   # Max for uniform component
mix_ratio    =  0.8   # Probability of Gaussian vs Uniform noise
random_seed  = 12345  # Seed for reproducibility

# Set seed
np.random.seed(random_seed)

# 1. Load your numeric CSV
df = pd.read_csv(input_csv)

# 2. Inject mixed-distribution noise into zero entries
df_noisy = df.copy()
for col in df_noisy.columns:
    # Identify zero entries
    mask = df_noisy[col] == 0
    n = mask.sum()
    if n == 0:
        continue

    # Generate mixed noise: choose Gaussian or Uniform per entry
    rand = np.random.rand(n)
    gaussian_noise = np.random.normal(loc=gauss_mean, scale=gauss_std, size=n)
    uniform_noise  = np.random.uniform(low=uniform_low, high=uniform_high, size=n)
    mixed_noise    = np.where(rand < mix_ratio, gaussian_noise, uniform_noise)

    # Clip to ensure within [-1, 1]
    mixed_noise = np.clip(mixed_noise, -1.0, 1.0)

    # Assign back into DataFrame
    df_noisy.loc[mask, col] = mixed_noise

# 3. Ensure output directory exists
os.makedirs(os.path.dirname(output_csv), exist_ok=True)

# 4. Write the noisy CSV
df_noisy.to_csv(output_csv, index=False)
print(f"✅ Written noisy CSV with mixed noise to: {output_csv}")
