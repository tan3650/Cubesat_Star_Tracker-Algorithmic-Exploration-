import pandas as pd
import numpy as np

# --- Parameters ---
input_file = 'C:/Users/Test/triangle_features.csv'            # Your original CSV
       # Your original CSV
output_file = 'triangle_catalog_hash.csv'    # Output CSV with numeric hash
angle_round = 0.1                            # Round angular distances to nearest 0.1 deg

# --- Load CSV ---
df = pd.read_csv(input_file)

# --- Optionally rename columns for convenience ---
df.rename(columns={
    'ang_dist_AB(deg)': 'ang_dist_AB',
    'ang_dist_BC(deg)': 'ang_dist_BC',
    'ang_dist_CA(deg)': 'ang_dist_CA'
}, inplace=True)

# --- Round angular distances ---
distances = df[['ang_dist_AB', 'ang_dist_BC', 'ang_dist_CA']].values
distances_rounded = np.round(distances / angle_round).astype(int)

# --- Compute numeric hash ---
# Encode as a single integer: hash = A*1e8 + B*1e4 + C
hash_numeric = distances_rounded[:,0]*10**8 + distances_rounded[:,1]*10**4 + distances_rounded[:,2]

# --- Add hash to dataframe ---
df['HashKey'] = hash_numeric

# --- Save new CSV ---
df.to_csv(output_file, index=False)

print(f"Saved {len(df)} triangles with numeric hash to '{output_file}'")
