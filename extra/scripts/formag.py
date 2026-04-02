import pandas as pd
import numpy as np

input_file = "C:/Users/Test/filtered_stars_38.csv"
output_file = "hip_eci_new_38.csv"

# Load data
df = pd.read_csv(input_file)

# Convert DErad from degrees to radians
df["DErad_rad"] = np.deg2rad(df["DErad"])

# Compute ECI unit vectors
df["x"] = np.cos(df["DErad_rad"]) * np.cos(df["RArad"])
df["y"] = np.cos(df["DErad_rad"]) * np.sin(df["RArad"])
df["z"] = np.sin(df["DErad_rad"])

# Normalize (optional, just to be safe)
vecs = df[["x","y","z"]].to_numpy()
norms = np.linalg.norm(vecs, axis=1)
df["x"] /= norms
df["y"] /= norms
df["z"] /= norms

# Save final columns
df[["HIP","Hpmag","x","y","z"]].to_csv(output_file, index=False)
print("ECI unit vectors written to", output_file)
