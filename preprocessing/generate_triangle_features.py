import pandas as pd
import numpy as np
import itertools
import math
import time

# ---------- CONFIG ----------
input_csv = r"C:\Users\Test\hip_eci_new.csv"
output_csv = r"C:\Users\Test\triangle_features.csv"

mag_limit = 3.81         # Only include stars brighter than this
max_stars = None       # Limit to this many brightest stars (set None to use all)
progress_update_interval = 5000  # Show progress every N triangles
# ----------------------------

# --- Read catalog (auto-detect delimiter) ---
df = pd.read_csv(input_csv, sep=None, engine='python')
print("✅ Columns found in file:", df.columns.tolist())

# Clean column names
df.columns = df.columns.str.strip()

# Ensure required columns exist
required = ['HIP', 'Hpmag', 'x', 'y', 'z']
for col in required:
    if col not in df.columns:
        raise ValueError(f"❌ Column '{col}' not found in file. Found columns: {df.columns.tolist()}")

# --- Filter by magnitude ---
bright_df = df[df['Hpmag'] < mag_limit].copy()
print(f"✅ Found {len(bright_df)} stars with Hpmag < {mag_limit}")

# --- Optional: limit number of stars ---
if max_stars is not None and len(bright_df) > max_stars:
    bright_df = bright_df.nsmallest(max_stars, 'Hpmag')  # pick brightest ones
    print(f"✅ Limited to {len(bright_df)} brightest stars (max_stars = {max_stars})")

if len(bright_df) < 3:
    raise ValueError("❌ Not enough stars to form triangles after filtering!")

stars = bright_df[['HIP', 'x', 'y', 'z']].values

# --- Geometry helper functions ---
def unit(v):
    return v / np.linalg.norm(v)

def angular_distance(v1, v2):
    v1, v2 = unit(v1), unit(v2)
    dot_val = np.clip(np.dot(v1, v2), -1.0, 1.0)
    return math.degrees(math.acos(dot_val))

def internal_angle(a, b, c):
    ab = b - a
    ac = c - a
    dot_val = np.dot(ab, ac) / (np.linalg.norm(ab) * np.linalg.norm(ac))
    return math.degrees(math.acos(np.clip(dot_val, -1.0, 1.0)))

# --- Compute invariant triangle features ---
rows = []
total_combinations = math.comb(len(stars), 3)
print(f"🔹 Generating {total_combinations:,} triangles from {len(stars)} stars...")

start_time = time.time()
for idx, combo in enumerate(itertools.combinations(enumerate(stars), 3), 1):
    (i, starA), (j, starB), (k, starC) = combo

    HIP_A, xA, yA, zA = starA
    HIP_B, xB, yB, zB = starB
    HIP_C, xC, yC, zC = starC

    A = np.array([xA, yA, zA])
    B = np.array([xB, yB, zB])
    C = np.array([xC, yC, zC])

    # Angular distances
    dAB = angular_distance(A, B)
    dBC = angular_distance(B, C)
    dCA = angular_distance(C, A)

    # Internal angles
    a = internal_angle(A, B, C)
    b = internal_angle(B, C, A)
    c = internal_angle(C, A, B)

    rows.append({
        'HIP_A': int(HIP_A),
        'HIP_B': int(HIP_B),
        'HIP_C': int(HIP_C),
        'ang_dist_AB(deg)': dAB,
        'ang_dist_BC(deg)': dBC,
        'ang_dist_CA(deg)': dCA,
        'angle_A(deg)': a,
        'angle_B(deg)': b,
        'angle_C(deg)': c
    })

    # Progress update
    if idx % progress_update_interval == 0:
        elapsed = time.time() - start_time
        percent = 100 * idx / total_combinations
        print(f"⏳ {idx:,}/{total_combinations:,} triangles ({percent:.2f}%) processed in {elapsed:.1f}s")

# --- Save to CSV ---
feature_df = pd.DataFrame(rows)
feature_df.to_csv(output_csv, index=False)

elapsed_total = time.time() - start_time
print(f"\n✅ Done! Generated {len(feature_df):,} triangles from {len(bright_df)} bright stars.")
print(f"📁 Saved to: {output_csv}")
print(f"⏱️ Total time: {elapsed_total:.2f} seconds") 